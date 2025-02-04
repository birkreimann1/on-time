import logging
import colorlog

GLOBAL_LOG_LEVEL = "INFO"  # Default log level. Can be updated from the main program.

def create_colored_logger():
    """Test"""
    logger = logging.getLogger(__name__)

    if not logger.hasHandlers():
        log_format = "%(log_color)s%(asctime)s - [%(category)s][%(levelname)s] - %(message)s"
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            log_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)  # Default to DEBUG level (for internal handling)

    return logger

def set_global_log_level(level):
    global GLOBAL_LOG_LEVEL
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    if level not in valid_levels:
        raise ValueError(f"Invalid log level: {level}. Choose from: {', '.join(valid_levels)}")
    
    GLOBAL_LOG_LEVEL = level

def get_global_log_level():
    global GLOBAL_LOG_LEVEL
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    return log_levels.get(GLOBAL_LOG_LEVEL, logging.INFO)

def log_with_category_and_priority(logger, category, priority, message):
    log_format = "%(log_color)s%(asctime)s - [%(category)s][%(levelname)s] - %(message)s"

    log_colors = {
        'INFO': 'green',
        'ERROR': 'red',
        'DEBUG': 'blue',
        'WARNING': 'yellow',
        'CRITICAL': 'bold_red',
    }

    category_color = 'cyan'

    final_log_colors = {
        'DEBUG': log_colors['DEBUG'],
        'INFO': log_colors['INFO'],
        'WARNING': log_colors['WARNING'],
        'ERROR': log_colors['ERROR'],
        'CRITICAL': log_colors['CRITICAL'],
    }

    final_log_colors['CATEGORY'] = category_color

    formatter = colorlog.ColoredFormatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors=final_log_colors
    )

    for handler in logger.handlers:
        handler.setFormatter(formatter)

    logger.log(getattr(logging, priority), message, extra={"category": category})

def log(message, category="SERVER", priority="INFO"):
    logger = create_colored_logger()
    level = get_global_log_level()  # Fetch the global log level
    
    if getattr(logging, priority) < level:
        return  # If the priority is lower than the global level, don't log it
    
    log_with_category_and_priority(logger, category=category, priority=priority, message=message)
