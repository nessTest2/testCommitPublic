"""
Movies Database System - Search Package
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::CREATE OR REPLACE PACKAGE SEARCH_PACKAGE AS::END SEARCH_PACKAGE;
Migrated from Oracle PL/SQL to Julia
Original: Romain VINDERS - 2322

This module provides movie search and retrieval functionality.
"""
module SearchPackage

using LibPQ
using DataFrames
using Dates
using ..Models
using ..LogPackage

export find_movies, get_movie_by_id, get_votes

"""
    find_movies(conn::LibPQ.Connection, title::Union{String,Nothing},
                year::Union{String,Nothing}, year_min::Union{String,Nothing},
                year_max::Union{String,Nothing}, actors::Vector{String},
                directors::Vector{String})::Vector{MovieSearchResult}

Find movies based on search criteria.
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::PROCEDURE FindMovies::END FindMovies;

# Arguments
- `conn`: Database connection
- `title`: Movie title to search for (partial match, case-insensitive)
- `year`: Exact year to filter by
- `year_min`: Minimum year (exclusive)
- `year_max`: Maximum year (exclusive)
- `actors`: List of actor names to filter by (all must match)
- `directors`: List of director names to filter by (all must match)

# Returns
- Vector of `MovieSearchResult` objects (max 30 results)

# Example
```julia
results = find_movies(conn, "Matrix", nothing, nothing, nothing,
                      ["Keanu Reeves"], ["Wachowski"])
```
"""
function find_movies(conn::LibPQ.Connection,
                     title::Union{String,Nothing},
                     year::Union{String,Nothing},
                     year_min::Union{String,Nothing},
                     year_max::Union{String,Nothing},
                     actors::Vector{String},
                     directors::Vector{String})::Vector{MovieSearchResult}
    try
        # Build base query
        query = """
            SELECT id_movie, title, EXTRACT(YEAR FROM release_date)::INTEGER AS year
            FROM movies
            WHERE 1=1
        """
        params = Any[]

        # Filter by year
        if !isnothing(year) && !isempty(year)
            query *= " AND release_date IS NOT NULL"
            query *= " AND EXTRACT(YEAR FROM release_date) = \$$(length(params)+1)"
            push!(params, parse(Int, year))
        else
            # Year range filtering
            if !isnothing(year_min) && !isempty(year_min)
                if !isnothing(year_max) && !isempty(year_max)
                    v_year_min = parse(Int, year_min) + 1
                    v_year_max = parse(Int, year_max) - 1
                    query *= " AND release_date IS NOT NULL"
                    query *= " AND EXTRACT(YEAR FROM release_date) BETWEEN \$$(length(params)+1) AND \$$(length(params)+2)"
                    push!(params, v_year_min, v_year_max)
                else
                    query *= " AND release_date IS NOT NULL"
                    query *= " AND EXTRACT(YEAR FROM release_date) > \$$(length(params)+1)"
                    push!(params, parse(Int, year_min))
                end
            elseif !isnothing(year_max) && !isempty(year_max)
                query *= " AND release_date IS NOT NULL"
                query *= " AND EXTRACT(YEAR FROM release_date) < \$$(length(params)+1)"
                push!(params, parse(Int, year_max))
            end
        end

        # Filter by title (case-insensitive, partial match, SQL injection protected)
        if !isnothing(title) && !isempty(title)
            # Remove single quotes for SQL injection protection
            safe_title = replace(title, "'" => "_")
            query *= " AND UPPER(title) LIKE UPPER(\$$(length(params)+1))"
            push!(params, "%$safe_title%")
        end

        # Filter by actors (all must match)
        for actor in actors
            if !isempty(actor)
                safe_actor = replace(actor, "'" => "_")
                query *= """
                    AND EXISTS(
                        SELECT 1 FROM movie_actors ma
                        INNER JOIN actors a ON ma.id_actor = a.id_actor
                        WHERE ma.id_movie = movies.id_movie
                        AND UPPER(a.name) LIKE UPPER(\$$(length(params)+1))
                    )
                """
                push!(params, "%$safe_actor%")
            end
        end

        # Filter by directors (all must match)
        for director in directors
            if !isempty(director)
                safe_director = replace(director, "'" => "_")
                query *= """
                    AND EXISTS(
                        SELECT 1 FROM movie_directors md
                        INNER JOIN directors d ON md.id_director = d.id_director
                        WHERE md.id_movie = movies.id_movie
                        AND UPPER(d.name) LIKE UPPER(\$$(length(params)+1))
                    )
                """
                push!(params, "%$safe_director%")
            end
        end

        # Limit results
        query *= " LIMIT 30"

        # Execute query
        result = execute(conn, query, params)
        df = DataFrame(result)

        # Convert to MovieSearchResult objects
        if nrow(df) == 0
            LogPackage.write_log("SearchPackage.find_movies", "No results found")
            return MovieSearchResult[]
        end

        movies = MovieSearchResult[]
        for row in eachrow(df)
            push!(movies, MovieSearchResult(
                id_movie = row[:id_movie],
                title = row[:title],
                year = ismissing(row[:year]) ? nothing : row[:year]
            ))
        end

        LogPackage.write_log("SearchPackage.find_movies", "Found $(length(movies)) movies")
        return movies

    catch e
        LogPackage.write_error_log("SearchPackage.find_movies", e)
        rethrow()
    end
end

"""
    get_movie_by_id(conn::LibPQ.Connection, movie_id::Int)::Union{MovieObj, Nothing}

Retrieve complete movie information by ID.
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::PROCEDURE GetMovieById::END GetMovieById;

# Arguments
- `conn`: Database connection
- `movie_id`: The movie ID to retrieve

# Returns
- `MovieObj` with all movie details, or `nothing` if not found

# Example
```julia
movie = get_movie_by_id(conn, 550)
```
"""
function get_movie_by_id(conn::LibPQ.Connection, movie_id::Int)::Union{MovieObj, Nothing}
    try
        # Fetch main movie data
        query = """
            SELECT m.id_movie, m.title, m.title_orig,
                   EXTRACT(YEAR FROM m.release_date)::INTEGER AS release_date,
                   ms.name AS status, c.name AS certification,
                   m.vote_average, m.vote_count, m.runtime, m.poster_path,
                   m.budget, m.revenue, m.overview
            FROM movies m
            LEFT JOIN movies_status ms ON m.id_status = ms.id_status
            LEFT JOIN certifications c ON m.id_certif = c.id_certif
            WHERE m.id_movie = \$1
        """

        result = execute(conn, query, [movie_id])
        df = DataFrame(result)

        if nrow(df) == 0
            LogPackage.write_log("SearchPackage.get_movie_by_id", "Movie $movie_id not found")
            return nothing
        end

        row = df[1, :]

        # Create MovieObj with main data
        movie = MovieObj(
            id_movie = row[:id_movie],
            title = row[:title],
            title_orig = row[:title_orig],
            release_date = ismissing(row[:release_date]) ? nothing : row[:release_date],
            vote_average_tmdb = ismissing(row[:vote_average]) ? nothing : Float64(row[:vote_average]),
            vote_count_tmdb = ismissing(row[:vote_count]) ? nothing : row[:vote_count],
            vote_average_app = 0.0,
            vote_count_app = 0,
            runtime = ismissing(row[:runtime]) ? nothing : row[:runtime],
            poster_path = ismissing(row[:poster_path]) ? nothing : row[:poster_path],
            budget = ismissing(row[:budget]) ? nothing : row[:budget],
            revenue = ismissing(row[:revenue]) ? nothing : row[:revenue],
            overview = ismissing(row[:overview]) ? nothing : row[:overview],
            status = ismissing(row[:status]) ? nothing : row[:status],
            certification = ismissing(row[:certification]) ? nothing : row[:certification]
        )

        # Get user reviews statistics
        votes_query = """
            SELECT COALESCE(AVG(rating), 0.0)::NUMERIC(3,1) AS avg_rating,
                   COUNT(*)::INTEGER AS vote_count
            FROM user_reviews
            WHERE id_movie = \$1
        """
        votes_result = execute(conn, votes_query, [movie_id])
        votes_df = DataFrame(votes_result)
        if nrow(votes_df) > 0
            movie.vote_average_app = Float64(votes_df[1, :avg_rating])
            movie.vote_count_app = votes_df[1, :vote_count]
        end

        # Get genres
        genres_query = "SELECT g.name FROM movie_genres mg INNER JOIN genres g ON mg.id_genre = g.id_genre WHERE mg.id_movie = \$1"
        genres_result = execute(conn, genres_query, [movie_id])
        movie.genres = String[row[:name] for row in Tables.rows(genres_result)]

        # Get actors and characters
        actors_query = """
            SELECT a.name, ma.character_name
            FROM movie_actors ma
            INNER JOIN actors a ON ma.id_actor = a.id_actor
            WHERE ma.id_movie = \$1
        """
        actors_result = execute(conn, actors_query, [movie_id])
        for row in Tables.rows(actors_result)
            push!(movie.actors, row[:name])
            push!(movie.characters, row[:character_name])
        end

        # Get directors
        directors_query = """
            SELECT d.name
            FROM movie_directors md
            INNER JOIN directors d ON md.id_director = d.id_director
            WHERE md.id_movie = \$1
        """
        directors_result = execute(conn, directors_query, [movie_id])
        movie.directors = String[row[:name] for row in Tables.rows(directors_result)]

        # Get production companies
        comps_query = """
            SELECT pc.name
            FROM movie_prod_comps mpc
            INNER JOIN prod_comps pc ON mpc.id_comp = pc.id_comp
            WHERE mpc.id_movie = \$1
        """
        comps_result = execute(conn, comps_query, [movie_id])
        movie.prod_comps = String[row[:name] for row in Tables.rows(comps_result)]

        # Get countries
        countries_query = """
            SELECT c.name
            FROM movie_countries mc
            INNER JOIN countries c ON mc.iso_country = c.iso_country
            WHERE mc.id_movie = \$1
        """
        countries_result = execute(conn, countries_query, [movie_id])
        movie.countries = String[row[:name] for row in Tables.rows(countries_result)]

        # Get languages
        languages_query = """
            SELECT l.name
            FROM movie_languages ml
            INNER JOIN languages l ON ml.iso_lang = l.iso_lang
            WHERE ml.id_movie = \$1
        """
        languages_result = execute(conn, languages_query, [movie_id])
        movie.languages = String[row[:name] for row in Tables.rows(languages_result)]

        LogPackage.write_log("SearchPackage.get_movie_by_id", "Movie $movie_id retrieved")
        return movie

    catch e
        LogPackage.write_error_log("SearchPackage.get_movie_by_id", e)
        rethrow()
    end
end

"""
    get_votes(conn::LibPQ.Connection, movie_id::Int, page::Int)::Vector{VoteListItem}

Retrieve a paginated list of votes/reviews for a movie.
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::PROCEDURE GetVotes::END GetVotes;

# Arguments
- `conn`: Database connection
- `movie_id`: The movie ID
- `page`: Page number (1-indexed, 5 reviews per page)

# Returns
- Vector of `VoteListItem` objects for the requested page

# Example
```julia
reviews = get_votes(conn, 550, 1)  # Get first 5 reviews
```
"""
function get_votes(conn::LibPQ.Connection, movie_id::Int, page::Int)::Vector{VoteListItem}
    try
        # Calculate pagination (5 items per page)
        v_end = page * 5
        v_start = v_end - 4

        # Query with pagination
        query = """
            SELECT * FROM (
                SELECT ROW_NUMBER() OVER (ORDER BY ur.review_date) AS id_vote,
                       u.login, ur.review_date, ur.rating, ur.review
                FROM user_reviews ur
                INNER JOIN users u ON ur.id_user = u.id_user
                WHERE ur.id_movie = \$1
            ) subquery
            WHERE id_vote BETWEEN \$2 AND \$3
        """

        result = execute(conn, query, [movie_id, v_start, v_end])
        df = DataFrame(result)

        if nrow(df) == 0
            LogPackage.write_log("SearchPackage.get_votes", "No results found for movie $movie_id page $page")
            return VoteListItem[]
        end

        # Convert to VoteListItem objects
        votes = VoteListItem[]
        for row in eachrow(df)
            push!(votes, VoteListItem(
                id_vote = row[:id_vote],
                login = row[:login],
                review_date = row[:review_date],
                rating = row[:rating],
                review = ismissing(row[:review]) ? nothing : row[:review]
            ))
        end

        return votes

    catch e
        LogPackage.write_error_log("SearchPackage.get_votes", e)
        rethrow()
    end
end

end # module SearchPackage
