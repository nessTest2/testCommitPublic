"""
Reviews Controller
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogWriteVote.java::public class DialogWriteVote extends javax.swing.JDialog::}
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogShowVotes.java::public class DialogShowVotes extends javax.swing.JDialog::}

Handles all review-related web requests.
"""
module ReviewsController

using Genie, Genie.Renderer, Genie.Renderer.Html, Genie.Renderer.Json
using Genie.Requests
using ..MoviesApp
using ..MoviesApp.ConnectionManager
using ..MoviesApp.SearchPackage
using ..MoviesApp.EvalPackage

"""
    submit_review()

Submit or update a movie review.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogWriteVote.java::private void jBtnSendActionPerformed::}
"""
function submit_review()
    try
        # Get parameters
        login = get(params(), :login, nothing)
        movie_id_str = get(params(), :movie_id, nothing)
        rating_str = get(params(), :rating, nothing)
        review_text = get(params(), :review, nothing)

        # Validate required fields
        if isnothing(login) || isempty(strip(login))
            return json(Dict("success" => false, "error" => "Login required"), status = 400)
        end

        if isnothing(movie_id_str)
            return json(Dict("success" => false, "error" => "Movie ID required"), status = 400)
        end

        if isnothing(rating_str)
            return json(Dict("success" => false, "error" => "Rating required"), status = 400)
        end

        # Parse parameters
        movie_id = parse(Int, movie_id_str)
        rating = parse(Int, rating_str)

        # Validate rating range
        if rating < 0 || rating > 10
            return json(Dict("success" => false, "error" => "Rating must be between 0 and 10"), status = 400)
        end

        # Get database connection
        conn = ConnectionManager.get_connection()

        # Submit review with retry on failover
        success = try
            EvalPackage.add_user_review(conn, login, movie_id, rating, review_text)
        catch e
            if ConnectionManager.check_and_failover(e)
                # Retry with backup connection
                conn = ConnectionManager.get_connection()
                EvalPackage.add_user_review(conn, login, movie_id, rating, review_text)
            else
                rethrow()
            end
        end

        if success
            json(Dict("success" => true, "message" => "Review submitted successfully"))
        else
            json(Dict("success" => false, "error" => "Failed to submit review"), status = 500)
        end

    catch e
        @error "Submit review error" exception=e
        json(Dict("success" => false, "error" => string(e)), status = 500)
    end
end

"""
    get_reviews()

Get paginated reviews for a movie.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogShowVotes.java::private void updateVotesList::}
"""
function get_reviews()
    try
        # Get parameters
        movie_id_str = get(params(), :movie_id, nothing)
        page_str = get(params(), :page, "1")

        if isnothing(movie_id_str)
            return json(Dict("success" => false, "error" => "Movie ID required"), status = 400)
        end

        movie_id = parse(Int, movie_id_str)
        page = parse(Int, page_str)

        # Get database connection
        conn = ConnectionManager.get_connection()

        # Fetch reviews with retry on failover
        reviews = try
            SearchPackage.get_votes(conn, movie_id, page)
        catch e
            if ConnectionManager.check_and_failover(e)
                # Retry with backup connection
                conn = ConnectionManager.get_connection()
                SearchPackage.get_votes(conn, movie_id, page)
            else
                rethrow()
            end
        end

        # Return JSON response
        json(Dict("success" => true, "reviews" => reviews, "count" => length(reviews), "page" => page))

    catch e
        @error "Get reviews error" exception=e
        json(Dict("success" => false, "error" => string(e)), status = 500)
    end
end

"""
    write_review_page()

Display the write review form.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogWriteVote.java::public DialogWriteVote::}
"""
function write_review_page()
    try
        movie_id = parse(Int, get(params(), :movie_id, "0"))
        conn = ConnectionManager.get_connection()
        movie = SearchPackage.get_movie_by_id(conn, movie_id)

        if isnothing(movie)
            html(:reviews, :error, error = "Movie not found")
        else
            html(:reviews, :write, movie = movie)
        end
    catch e
        @error "Write review page error" exception=e
        html(:reviews, :error, error = string(e))
    end
end

"""
    show_reviews_page()

Display the reviews list page.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/DialogShowVotes.java::public DialogShowVotes::}
"""
function show_reviews_page()
    try
        movie_id = parse(Int, get(params(), :movie_id, "0"))
        page = parse(Int, get(params(), :page, "1"))

        conn = ConnectionManager.get_connection()
        movie = SearchPackage.get_movie_by_id(conn, movie_id)
        reviews = SearchPackage.get_votes(conn, movie_id, page)

        if isnothing(movie)
            html(:reviews, :error, error = "Movie not found")
        else
            html(:reviews, :show, movie = movie, reviews = reviews, page = page)
        end
    catch e
        @error "Show reviews page error" exception=e
        html(:reviews, :error, error = string(e))
    end
end

end # module ReviewsController
