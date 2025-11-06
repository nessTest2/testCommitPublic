"""
Movies Database System - Evaluation Package
@SOURCE: movies_sql_procedures/cb/eval_movies/eval_movies.sql::CREATE OR REPLACE PACKAGE EVAL_PACKAGE AS::END EVAL_PACKAGE;
Migrated from Oracle PL/SQL to Julia
Original: Romain VINDERS - 2322

This module provides functionality for adding and managing user reviews.
"""
module EvalPackage

using LibPQ
using DataFrames
using ..LogPackage

export add_user_review

"""
    add_user_review(conn::LibPQ.Connection, login::String, movie_id::Int,
                    rating::Int, review::Union{String,Nothing})::Bool

Add or update a user review for a movie.
@SOURCE: movies_sql_procedures/cb/eval_movies/eval_movies.sql::PROCEDURE AddUserReview::END AddUserReview;

This function creates a new user if the login doesn't exist, then inserts
or updates the user's review for the specified movie.

# Arguments
- `conn`: Database connection
- `login`: User login name (case-insensitive, created if doesn't exist)
- `movie_id`: The movie ID to review
- `rating`: Rating score (0-10)
- `review`: Review text (optional, max 200 characters)

# Returns
- `true` if successful, `false` or throws on error

# Example
```julia
success = add_user_review(conn, "john_doe", 550, 9, "Amazing movie!")
```
"""
function add_user_review(conn::LibPQ.Connection,
                        login::String,
                        movie_id::Int,
                        rating::Int,
                        review::Union{String,Nothing})::Bool
    try
        # Start transaction
        execute(conn, "BEGIN")

        # Validate rating
        if rating < 0 || rating > 10
            error("Rating must be between 0 and 10")
        end

        # Prepare review text (limit to 200 characters, null if empty)
        review_text = nothing
        if !isnothing(review) && !isempty(strip(review))
            review_text = first(strip(review), 200)
        end

        # Get or create user ID
        user_id = nothing
        try
            # Try to find existing user (case-insensitive)
            user_query = "SELECT id_user FROM users WHERE UPPER(login) = UPPER(\$1)"
            user_result = execute(conn, user_query, [login])
            user_df = DataFrame(user_result)

            if nrow(user_df) > 0
                user_id = user_df[1, :id_user]
            else
                # Create new user
                insert_query = """
                    INSERT INTO users (login, sync_token)
                    VALUES (\$1, '0')
                    RETURNING id_user
                """
                insert_result = execute(conn, insert_query, [login])
                insert_df = DataFrame(insert_result)
                user_id = insert_df[1, :id_user]

                LogPackage.write_log("EvalPackage.add_user_review",
                                   "Created new user: $login")
            end
        catch e
            execute(conn, "ROLLBACK")
            LogPackage.write_error_log("EvalPackage.add_user_review", e)
            rethrow()
        end

        # Insert or update the review using UPSERT (INSERT ... ON CONFLICT)
        upsert_query = """
            INSERT INTO user_reviews (id_user, id_movie, rating, review, sync_token)
            VALUES (\$1, \$2, \$3, \$4, '0')
            ON CONFLICT (id_user, id_movie)
            DO UPDATE SET
                rating = EXCLUDED.rating,
                review = EXCLUDED.review,
                review_date = CURRENT_TIMESTAMP,
                sync_token = '1'
        """

        execute(conn, upsert_query, [user_id, movie_id, rating, review_text])

        # Commit transaction
        execute(conn, "COMMIT")

        LogPackage.write_log("EvalPackage.add_user_review",
                           "Review added/updated for user $login, movie $movie_id")
        return true

    catch e
        # Rollback on error
        try
            execute(conn, "ROLLBACK")
        catch rollback_error
            @error "Failed to rollback transaction" error=rollback_error
        end

        LogPackage.write_error_log("EvalPackage.add_user_review", e)
        rethrow()
    end
end

end # module EvalPackage
