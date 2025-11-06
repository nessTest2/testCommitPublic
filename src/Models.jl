"""
Movies Database System - Data Models
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::CREATE OR REPLACE TYPE MovieObj_t AS OBJECT::Languages     StringArray_t
Migrated from Oracle SQL custom types to Julia structs
Original: Romain VINDERS - 2322

This module defines the data structures used throughout the application.
"""
module Models

using Dates
using StructTypes

export MovieObj, VoteListItem, StringArray

# Type alias for arrays of strings (equivalent to StringArray_t in Oracle)
const StringArray = Vector{String}

"""
    VoteListItem

Represents a single user review/vote.
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::CREATE OR REPLACE TYPE VoteListItem_t AS OBJECT::Review      VARCHAR2(200)
"""
Base.@kwdef mutable struct VoteListItem
    id_vote::Int
    login::String
    review_date::DateTime
    rating::Int
    review::Union{String, Nothing}
end

# Register struct for JSON serialization
StructTypes.StructType(::Type{VoteListItem}) = StructTypes.Mutable()

"""
    MovieObj

Complete movie object with all related data.
@SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::CREATE OR REPLACE TYPE MovieObj_t AS OBJECT::Languages     StringArray_t

This struct contains all movie information including metadata, ratings, and
related entities (actors, directors, genres, etc.).
"""
Base.@kwdef mutable struct MovieObj
    id_movie::Int
    title::String
    title_orig::String
    release_date::Union{Int, Nothing}  # Year as integer
    vote_average_tmdb::Union{Float64, Nothing}
    vote_count_tmdb::Union{Int, Nothing}
    vote_average_app::Union{Float64, Nothing}
    vote_count_app::Int
    runtime::Union{Int, Nothing}
    poster_path::Union{String, Nothing}
    budget::Union{Int, Nothing}
    revenue::Union{Int, Nothing}
    overview::Union{String, Nothing}
    status::Union{String, Nothing}
    certification::Union{String, Nothing}
    genres::StringArray = String[]
    actors::StringArray = String[]
    characters::StringArray = String[]
    directors::StringArray = String[]
    prod_comps::StringArray = String[]
    countries::StringArray = String[]
    languages::StringArray = String[]
end

# Register struct for JSON serialization
StructTypes.StructType(::Type{MovieObj}) = StructTypes.Mutable()

"""
    MovieSearchResult

Simple movie search result with ID, title, and year.
"""
Base.@kwdef struct MovieSearchResult
    id_movie::Int
    title::String
    year::Union{Int, Nothing}
end

# Register struct for JSON serialization
StructTypes.StructType(::Type{MovieSearchResult}) = StructTypes.Struct()

end # module Models
