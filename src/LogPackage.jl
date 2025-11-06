"""
Movies Database System - Logging Module
@SOURCE: movies_sql_procedures/create_log.sql::CREATE OR REPLACE PACKAGE LOG_PACKAGE AS::END LOG_PACKAGE;
Migrated from Oracle PL/SQL to Julia
Original: Romain VINDERS - 2322

This module provides logging functionality for the Movies Database System.
It writes informational and error messages to the log_messages table.
"""
module LogPackage

using LibPQ
using Dates

export write_log, write_error_log, get_connection

# Global connection pool (to be set by main application)
const DB_CONNECTION = Ref{Union{LibPQ.Connection, Nothing}}(nothing)

"""
    set_connection(conn::LibPQ.Connection)

Set the database connection for logging operations.
"""
function set_connection(conn::LibPQ.Connection)
    DB_CONNECTION[] = conn
end

"""
    get_connection()::LibPQ.Connection

Get the current database connection or throw an error if not set.
"""
function get_connection()::LibPQ.Connection
    if DB_CONNECTION[] === nothing
        error("Database connection not initialized. Call LogPackage.set_connection() first.")
    end
    return DB_CONNECTION[]
end

"""
    write_log(origin::String, message::String)

Write an informational log message to the database.
@SOURCE: movies_sql_procedures/create_log.sql::PROCEDURE WriteLog::END WriteLog;

# Arguments
- `origin::String`: The source of the log message (e.g., "ModuleName.FunctionName")
- `message::String`: The log message content

# Example
```julia
write_log("SearchPackage.find_movies", "Search completed successfully")
```
"""
function write_log(origin::String, message::String)
    try
        conn = get_connection()

        # Execute insert with parameters
        result = execute(conn,
            "INSERT INTO log_messages (origin, code, message) VALUES (\$1, 0, \$2)",
            [isempty(origin) ? "unknown" : origin, message])

        # Commit is implicit in LibPQ for non-transaction blocks
        return true
    catch e
        # If logging fails, print to stderr but don't throw
        @error "Failed to write log message" origin=origin message=message error=e
        return false
    end
end

"""
    write_error_log(origin::String, error::Exception)

Write an error log message to the database.
@SOURCE: movies_sql_procedures/create_log.sql::PROCEDURE WriteErrorLog::END WriteErrorLog;

# Arguments
- `origin::String`: The source of the error (e.g., "ModuleName.FunctionName")
- `error::Exception`: The exception that occurred

# Example
```julia
try
    # some operation
catch e
    write_error_log("SearchPackage.find_movies", e)
    rethrow()
end
```
"""
function write_error_log(origin::String, error::Exception)
    try
        conn = get_connection()

        # Extract error information
        error_code = -1  # Generic error code
        error_message = string(typeof(error)) * ": " * string(error)
        error_message = first(error_message, 120)  # Limit to 120 characters

        # Execute insert with parameters
        result = execute(conn,
            "INSERT INTO log_messages (origin, code, message) VALUES (\$1, \$2, \$3)",
            [isempty(origin) ? "unknown" : origin, error_code, error_message])

        return true
    catch log_error
        # If logging fails, print to stderr but don't throw
        @error "Failed to write error log" origin=origin error=error log_error=log_error
        return false
    end
end

"""
    write_error_log(origin::String)

Write an error log message to the database (catches current exception).
@SOURCE: movies_sql_procedures/create_log.sql::PROCEDURE WriteErrorLog::END WriteErrorLog;

# Arguments
- `origin::String`: The source of the error (e.g., "ModuleName.FunctionName")

# Example
```julia
try
    # some operation
catch
    write_error_log("SearchPackage.find_movies")
    rethrow()
end
```
"""
function write_error_log(origin::String)
    if current_exceptions() |> isempty
        write_log(origin, "Error logged but no active exception")
        return false
    end

    # Get the current exception
    exc = current_exceptions()[end]
    write_error_log(origin, exc.exception)
end

end # module LogPackage
