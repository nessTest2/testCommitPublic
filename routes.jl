"""
Movies Database System - Routes
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::public static void main(String args[])::}

Defines all application routes.
"""
using Genie, Genie.Router, Genie.Renderer.Html

# Include controllers
include("app/resources/MoviesController.jl")
include("app/resources/ReviewsController.jl")

using .MoviesController
using .ReviewsController

# Main routes
route("/") do
    redirect(:get_index)
end

route("/index", MoviesController.index, named = :get_index)

# Movie search routes
route("/movies/search", MoviesController.search, method = POST, named = :search_movies)
route("/movies/:id", MoviesController.movie_details, named = :movie_details)
route("/api/movies/:id", MoviesController.get_movie, named = :api_get_movie)

# Review routes
route("/movies/:movie_id/reviews/write", ReviewsController.write_review_page, named = :write_review_page)
route("/movies/:movie_id/reviews", ReviewsController.show_reviews_page, named = :show_reviews_page)
route("/api/movies/:movie_id/reviews", ReviewsController.submit_review, method = POST, named = :api_submit_review)
route("/api/movies/:movie_id/reviews/list", ReviewsController.get_reviews, named = :api_get_reviews)

# Static files
route("/css/*", Genie.Assets.asset_file)
route("/js/*", Genie.Assets.asset_file)
route("/img/*", Genie.Assets.asset_file)
