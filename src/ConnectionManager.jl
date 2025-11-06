"""
Movies Database System - Connection Manager
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public class LoginSingleton::}
Migrated from Java Singleton to Julia module
Original: Romain VINDERS - 2322

This module manages database connections with automatic failover between
primary and backup databases.
"""
module ConnectionManager

using LibPQ
using ..LogPackage

export init_connections, get_connection, close_connections, set_current_user,
       get_current_user, is_using_secondary, ConnectionConfig

# Mutable struct to hold connection configuration
Base.@kwdef mutable struct ConnectionConfig
    primary_host::String = "localhost"
    primary_port::Int = 5432
    primary_dbname::String = "movies_db"
    primary_user::String = "movies_user"
    primary_password::String = "movies_pass"
    backup_host::String = "localhost"
    backup_port::Int = 5433  # Different port for backup
    backup_dbname::String = "movies_db_backup"
    backup_user::String = "movies_user"
    backup_password::String = "movies_pass"
end

# Global state
const PRIMARY_CONN = Ref{Union{LibPQ.Connection, Nothing}}(nothing)
const BACKUP_CONN = Ref{Union{LibPQ.Connection, Nothing}}(nothing)
const USING_SECONDARY = Ref{Bool}(false)
const CURRENT_USER = Ref{Union{String, Nothing}}(nothing)
const CONFIG = Ref{Union{ConnectionConfig, Nothing}}(nothing)

"""
    init_connections(config::ConnectionConfig)::Bool

Initialize database connections with the provided configuration.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public void startConnection()::}

# Arguments
- `config`: ConnectionConfig with database connection details

# Returns
- `true` if initialization successful

# Example
```julia
config = ConnectionConfig(
    primary_dbname = "movies_db",
    primary_user = "movies_user",
    primary_password = "secret"
)
init_connections(config)
```
"""
function init_connections(config::ConnectionConfig)::Bool
    try
        CONFIG[] = config

        # Connect to primary database
        primary_conn_string = """
            host=$(config.primary_host)
            port=$(config.primary_port)
            dbname=$(config.primary_dbname)
            user=$(config.primary_user)
            password=$(config.primary_password)
        """

        @info "Connecting to primary database..."
        PRIMARY_CONN[] = LibPQ.Connection(primary_conn_string)
        @info "Connected to primary database"

        # Set connection for logging
        LogPackage.set_connection(PRIMARY_CONN[])

        # Optionally connect to backup database
        try
            backup_conn_string = """
                host=$(config.backup_host)
                port=$(config.backup_port)
                dbname=$(config.backup_dbname)
                user=$(config.backup_user)
                password=$(config.backup_password)
            """

            @info "Connecting to backup database..."
            BACKUP_CONN[] = LibPQ.Connection(backup_conn_string)
            @info "Connected to backup database"
        catch e
            @warn "Failed to connect to backup database" error=e
            # Backup connection is optional
        end

        USING_SECONDARY[] = false
        return true

    catch e
        @error "Failed to initialize connections" error=e
        return false
    end
end

"""
    get_connection()::LibPQ.Connection

Get the current active database connection (primary or backup).
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public Connection getConnex()::}

Returns the backup connection if primary has failed, otherwise returns primary.

# Returns
- Active LibPQ.Connection

# Throws
- Error if no connection available
"""
function get_connection()::LibPQ.Connection
    if USING_SECONDARY[]
        if BACKUP_CONN[] !== nothing
            return BACKUP_CONN[]
        else
            error("Backup database connection not available")
        end
    else
        if PRIMARY_CONN[] !== nothing
            return PRIMARY_CONN[]
        else
            error("Primary database connection not available")
        end
    end
end

"""
    check_and_failover(e::Exception)::Bool

Check if an error requires database failover and perform it if needed.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public boolean checkCrash(SQLException exc)::}

# Arguments
- `e`: Exception that occurred

# Returns
- `true` if failover was performed, `false` otherwise

# Example
```julia
try
    # database operation
catch e
    if check_and_failover(e)
        # retry operation
    else
        rethrow()
    end
end
```
"""
function check_and_failover(e::Exception)::Bool
    # Check if this is a connection error
    error_msg = string(e)

    # Primary database failure
    if !USING_SECONDARY[] && contains(lowercase(error_msg), "connection")
        @warn "Primary database connection lost, failing over to backup"
        LogPackage.write_log("ConnectionManager.check_and_failover",
                           "Failing over from primary to backup")

        if BACKUP_CONN[] !== nothing
            USING_SECONDARY[] = true
            LogPackage.set_connection(BACKUP_CONN[])
            return true
        else
            @error "Cannot failover: backup connection not available"
            return false
        end
    end

    # Backup database signaling primary is restored
    if USING_SECONDARY[] && contains(lowercase(error_msg), "primary")
        @info "Primary database restored, failing back to primary"
        LogPackage.write_log("ConnectionManager.check_and_failover",
                           "Failing back to primary database")

        if PRIMARY_CONN[] !== nothing
            USING_SECONDARY[] = false
            LogPackage.set_connection(PRIMARY_CONN[])
            return true
        else
            @error "Cannot failback: primary connection not available"
            return false
        end
    end

    return false
end

"""
    is_using_secondary()::Bool

Check if currently using the backup (secondary) database.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public boolean getSecondaryServer()::}

# Returns
- `true` if using backup database, `false` if using primary
"""
function is_using_secondary()::Bool
    return USING_SECONDARY[]
end

"""
    set_current_user(login::String)

Set the current logged-in user.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public void setLogin(String login)::}

# Arguments
- `login`: User login name
"""
function set_current_user(login::String)
    CURRENT_USER[] = login
end

"""
    get_current_user()::Union{String, Nothing}

Get the current logged-in user.
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java::public String getLogin()::}

# Returns
- Current user login or nothing if not logged in
"""
function get_current_user()::Union{String, Nothing}
    return CURRENT_USER[]
end

"""
    close_connections()

Close all database connections.

# Example
```julia
close_connections()
```
"""
function close_connections()
    try
        if PRIMARY_CONN[] !== nothing
            close(PRIMARY_CONN[])
            PRIMARY_CONN[] = nothing
        end

        if BACKUP_CONN[] !== nothing
            close(BACKUP_CONN[])
            BACKUP_CONN[] = nothing
        end

        @info "All database connections closed"
    catch e
        @error "Error closing connections" error=e
    end
end

end # module ConnectionManager
