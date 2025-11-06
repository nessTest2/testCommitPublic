"""
Movies Controller
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::private void findMovies::}
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::private void getMovie::}

Handles all movie-related web requests.
"""
module MoviesController

using Genie, Genie.Renderer, Genie.Renderer.Html, Genie.Renderer.Json
using Genie.Requests
using ..MoviesApp
using ..MoviesApp.ConnectionManager
using ..MoviesApp.SearchPackage
using ..MoviesApp.Models

"""
    index()

Display the main search page.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::public Rennequinepolis()::}
"""
function index()
    html(:movies, :index)
end

"""
    search()

Perform movie search based on form parameters.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::private void findMovies::}
"""
function search()
    try
        # Get search parameters
        title = get(params(), :title, nothing)
        year = get(params(), :year, nothing)
        year_min = get(params(), :year_min, nothing)
        year_max = get(params(), :year_max, nothing)

        # Get actor list (comma-separated)
        actors_str = get(params(), :actors, "")
        actors = filter(!isempty, strip.(split(actors_str, ',')))

        # Get director list (comma-separated)
        directors_str = get(params(), :directors, "")
        directors = filter(!isempty, strip.(split(directors_str, ',')))

        # Get database connection
        conn = ConnectionManager.get_connection()

        # Perform search with retry on failover
        results = try
            SearchPackage.find_movies(conn, title, year, year_min, year_max,
                                     Vector{String}(actors), Vector{String}(directors))
        catch e
            if ConnectionManager.check_and_failover(e)
                # Retry with backup connection
                conn = ConnectionManager.get_connection()
                SearchPackage.find_movies(conn, title, year, year_min, year_max,
                                         Vector{String}(actors), Vector{String}(directors))
            else
                rethrow()
            end
        end

        # Return JSON response
        json(Dict("success" => true, "results" => results, "count" => length(results)))

    catch e
        @error "Search error" exception=e
        json(Dict("success" => false, "error" => string(e)), status = 500)
    end
end

"""
    get_movie()

Get detailed information about a specific movie.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::private void getMovie::}
"""
function get_movie()
    try
        # Get movie ID from parameter
        movie_id_str = get(params(), :id, nothing)
        if isnothing(movie_id_str)
            return json(Dict("success" => false, "error" => "Movie ID required"), status = 400)
        end

        movie_id = parse(Int, movie_id_str)

        # Get database connection
        conn = ConnectionManager.get_connection()

        # Fetch movie with retry on failover
        movie = try
            SearchPackage.get_movie_by_id(conn, movie_id)
        catch e
            if ConnectionManager.check_and_failover(e)
                # Retry with backup connection
                conn = ConnectionManager.get_connection()
                SearchPackage.get_movie_by_id(conn, movie_id)
            else
                rethrow()
            end
        end

        if isnothing(movie)
            return json(Dict("success" => false, "error" => "Movie not found"), status = 404)
        end

        # Return JSON response
        json(Dict("success" => true, "movie" => movie))

    catch e
        @error "Get movie error" exception=e
        json(Dict("success" => false, "error" => string(e)), status = 500)
    end
end

"""
    movie_details()

Display the movie details page.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogMovie.java::public class DialogMovie extends javax.swing.JDialog::}
"""
function movie_details()
    try
        movie_id = parse(Int, get(params(), :id, "0"))
        conn = ConnectionManager.get_connection()
        movie = SearchPackage.get_movie_by_id(conn, movie_id)

        if isnothing(movie)
            html(:movies, :error, error = "Movie not found")
        else
            html(:movies, :details, movie = movie)
        end
    catch e
        @error "Movie details error" exception=e
        html(:movies, :error, error = string(e))
    end
end

end # module MoviesController
