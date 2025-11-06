"""
Movies Database System - Backup & Restore Package
@SOURCE: movies_sql_procedures/cb/cb_backup.sql::CREATE OR REPLACE PACKAGE BACKUP_PACKAGE AS::END BACKUP_PACKAGE;
@SOURCE: movies_sql_procedures/cbb/cbb_restore.sql::CREATE OR REPLACE PACKAGE RESTORE_PACKAGE AS::END RESTORE_PACKAGE;
Migrated from Oracle PL/SQL to Julia
Original: Romain VINDERS - 2322

This module provides backup and restore functionality for the dual-database architecture.
In the original system, triggers automatically backed up data from CB to CBB.
In this Julia version, we implement application-level backup through event handlers.
"""
module BackupPackage

using LibPQ
using Dates
using ..LogPackage

export backup_review, restore_reviews, sync_pending_reviews

"""
    backup_review(primary_conn::LibPQ.Connection, backup_conn::LibPQ.Connection,
                  user_id::Int, movie_id::Int)::Bool

Backup a single user review from primary to backup database.
@SOURCE: movies_sql_procedures/cb/cb_backup.sql::PROCEDURE BackupInsertedReview::END BackupInsertedReview;

# Arguments
- `primary_conn`: Connection to primary database
- `backup_conn`: Connection to backup database
- `user_id`: User ID
- `movie_id`: Movie ID

# Returns
- `true` if successful
"""
function backup_review(primary_conn::LibPQ.Connection,
                      backup_conn::LibPQ.Connection,
                      user_id::Int,
                      movie_id::Int)::Bool
    try
        # Fetch review from primary
        query = """
            SELECT id_user, id_movie, review_date, rating, review, sync_token
            FROM user_reviews
            WHERE id_user = \$1 AND id_movie = \$2
        """
        result = execute(primary_conn, query, [user_id, movie_id])
        df = DataFrame(result)

        if nrow(df) == 0
            LogPackage.write_log("BackupPackage.backup_review",
                               "Review not found: user=$user_id, movie=$movie_id")
            return false
        end

        row = df[1, :]

        # Insert or update in backup database
        upsert_query = """
            INSERT INTO user_reviews (id_user, id_movie, review_date, rating, review, sync_token)
            VALUES (\$1, \$2, \$3, \$4, \$5, '0')
            ON CONFLICT (id_user, id_movie)
            DO UPDATE SET
                review_date = EXCLUDED.review_date,
                rating = EXCLUDED.rating,
                review = EXCLUDED.review,
                sync_token = '0'
        """

        execute(backup_conn, upsert_query, [
            row[:id_user],
            row[:id_movie],
            row[:review_date],
            row[:rating],
            ismissing(row[:review]) ? nothing : row[:review]
        ])

        # Update sync token in primary
        update_query = """
            UPDATE user_reviews
            SET sync_token = '0'
            WHERE id_user = \$1 AND id_movie = \$2
        """
        execute(primary_conn, update_query, [user_id, movie_id])

        LogPackage.write_log("BackupPackage.backup_review",
                           "Review backed up: user=$user_id, movie=$movie_id")
        return true

    catch e
        LogPackage.write_error_log("BackupPackage.backup_review", e)
        return false
    end
end

"""
    sync_pending_reviews(primary_conn::LibPQ.Connection,
                        backup_conn::LibPQ.Connection)::Int

Synchronize all pending reviews (sync_token='1') from primary to backup.
@SOURCE: movies_sql_procedures/cb/cb_backup.sql::PROCEDURE BackupAllPendingReviews::END BackupAllPendingReviews;

# Arguments
- `primary_conn`: Connection to primary database
- `backup_conn`: Connection to backup database

# Returns
- Number of reviews synchronized
"""
function sync_pending_reviews(primary_conn::LibPQ.Connection,
                              backup_conn::LibPQ.Connection)::Int
    try
        # Get all pending reviews
        query = """
            SELECT id_user, id_movie, review_date, rating, review
            FROM user_reviews
            WHERE sync_token = '1'
        """
        result = execute(primary_conn, query)
        df = DataFrame(result)

        if nrow(df) == 0
            LogPackage.write_log("BackupPackage.sync_pending_reviews", "No pending reviews")
            return 0
        end

        count = 0
        for row in eachrow(df)
            try
                # Backup each review
                if backup_review(primary_conn, backup_conn, row[:id_user], row[:id_movie])
                    count += 1
                end
            catch e
                LogPackage.write_error_log("BackupPackage.sync_pending_reviews", e)
            end
        end

        LogPackage.write_log("BackupPackage.sync_pending_reviews",
                           "Synchronized $count reviews")
        return count

    catch e
        LogPackage.write_error_log("BackupPackage.sync_pending_reviews", e)
        return 0
    end
end

"""
    restore_reviews(backup_conn::LibPQ.Connection,
                   primary_conn::LibPQ.Connection)::Int

Restore all reviews from backup to primary database.
@SOURCE: movies_sql_procedures/cbb/cbb_restore.sql::PROCEDURE RestoreAllReviews::END RestoreAllReviews;

# Arguments
- `backup_conn`: Connection to backup database
- `primary_conn`: Connection to primary database (being restored)

# Returns
- Number of reviews restored
"""
function restore_reviews(backup_conn::LibPQ.Connection,
                        primary_conn::LibPQ.Connection)::Int
    try
        # Get all reviews from backup
        query = """
            SELECT id_user, id_movie, review_date, rating, review
            FROM user_reviews
        """
        result = execute(backup_conn, query)
        df = DataFrame(result)

        if nrow(df) == 0
            LogPackage.write_log("BackupPackage.restore_reviews", "No reviews to restore")
            return 0
        end

        count = 0
        for row in eachrow(df)
            try
                # Insert or update in primary database
                upsert_query = """
                    INSERT INTO user_reviews (id_user, id_movie, review_date, rating, review, sync_token)
                    VALUES (\$1, \$2, \$3, \$4, \$5, '0')
                    ON CONFLICT (id_user, id_movie)
                    DO UPDATE SET
                        review_date = EXCLUDED.review_date,
                        rating = EXCLUDED.rating,
                        review = EXCLUDED.review,
                        sync_token = '0'
                """

                execute(primary_conn, upsert_query, [
                    row[:id_user],
                    row[:id_movie],
                    row[:review_date],
                    row[:rating],
                    ismissing(row[:review]) ? nothing : row[:review]
                ])

                count += 1
            catch e
                LogPackage.write_error_log("BackupPackage.restore_reviews", e)
            end
        end

        LogPackage.write_log("BackupPackage.restore_reviews",
                           "Restored $count reviews")
        return count

    catch e
        LogPackage.write_error_log("BackupPackage.restore_reviews", e)
        return 0
    end
end

end # module BackupPackage
