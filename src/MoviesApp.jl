"""
Movies Database System - Main Application Module
@SOURCE: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java::public class Rennequinepolis extends javax.swing.JFrame::}
Migrated from Java Swing to Julia/Genie.jl Web Application
Original: Romain VINDERS - 2322

This module initializes the web application and loads all components.
"""
module MoviesApp

# Load all application modules
include("Models.jl")
include("LogPackage.jl")
include("SearchPackage.jl")
include("EvalPackage.jl")
include("BackupPackage.jl")
include("ConnectionManager.jl")

using .Models
using .LogPackage
using .SearchPackage
using .EvalPackage
using .BackupPackage
using .ConnectionManager

# Export for external use
export Models, LogPackage, SearchPackage, EvalPackage, BackupPackage, ConnectionManager

end # module MoviesApp
