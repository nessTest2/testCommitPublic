"""
Movies Database System - Server Entry Point
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::public static void main(String args[])::}

Main server file to start the Genie.jl web application.
"""

using Genie
using Genie.Renderer.Html

# Load application modules
include("src/MoviesApp.jl")
using .MoviesApp

# Initialize database connection
using .MoviesApp.ConnectionManager

# Load configuration
const CONFIG = ConnectionManager.ConnectionConfig(
    primary_host = get(ENV, "DB_PRIMARY_HOST", "localhost"),
    primary_port = parse(Int, get(ENV, "DB_PRIMARY_PORT", "5432")),
    primary_dbname = get(ENV, "DB_PRIMARY_NAME", "movies_db"),
    primary_user = get(ENV, "DB_PRIMARY_USER", "movies_user"),
    primary_password = get(ENV, "DB_PRIMARY_PASSWORD", "movies_pass"),
    backup_host = get(ENV, "DB_BACKUP_HOST", "localhost"),
    backup_port = parse(Int, get(ENV, "DB_BACKUP_PORT", "5433")),
    backup_dbname = get(ENV, "DB_BACKUP_NAME", "movies_db_backup"),
    backup_user = get(ENV, "DB_BACKUP_USER", "movies_user"),
    backup_password = get(ENV, "DB_BACKUP_PASSWORD", "movies_pass")
)

# Initialize connections
println("Initializing database connections...")
if !ConnectionManager.init_connections(CONFIG)
    error("Failed to initialize database connections")
end
println("Database connections initialized successfully")

# Load routes
include("routes.jl")

# Start server
const PORT = parse(Int, get(ENV, "PORT", "8000"))
const HOST = get(ENV, "HOST", "0.0.0.0")

println("Starting Movies Database Web Application...")
println("Server will be available at http://$(HOST):$(PORT)")
println("Press Ctrl+C to stop the server")

# Configure Genie
Genie.config.server_port = PORT
Genie.config.server_host = HOST
Genie.config.run_as_server = true

# Start the server
up()
