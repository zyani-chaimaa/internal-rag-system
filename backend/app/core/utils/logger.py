import sys
from loguru import logger
from backend.app.core.config import LOGS_DIR

def setup_logger():
    
    # Remove default handler
    logger.remove()
   
    # Console: colored, human-readable 
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level="INFO",
        colorize=True
    )
   
    # File: detailed, machine-readable 
    logger.add(
        LOGS_DIR / "rag_system.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",     # New file every 10 MB
        retention="7 days",   # Keep 7 days of logs
        compression="zip"     # Compress old logs
    )
    return logger

# Create a global logger instance
log = setup_logger()