import logging
import functools
import traceback
import time
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)

# ---------- CUSTOM EXCEPTIONS ----------
class AssistantError(Exception):
    """Base exception for all assistant errors."""
    pass

class SpeechRecognitionError(AssistantError):
    """Raised when speech recognition fails."""
    pass

class TTSError(AssistantError):
    """Raised when text-to-speech fails."""
    pass

class NetworkCommunicationError(AssistantError):
    """Raised when webhook/n8n communication fails."""
    pass

class ConfigurationError(AssistantError):
    """Raised when the application is misconfigured."""
    pass

# ---------- RETRY DECORATOR ----------
def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions: tuple = (Exception,)):
    """
    Retry decorator for operations that may fail temporarily (e.g., network requests).
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for the delay after each failed attempt
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"[{func.__name__}] failed after {max_attempts} attempts: {e}")
                        raise
                    
                    logger.warning(f"[{func.__name__}] attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator

# ---------- UNIFIED ERROR HANDLER ----------
def handle_errors(
    default_return: Any = None,
    log_traceback: bool = False
):
    """
    Decorator for unified error handling to ensure the main loop never crashes.
    
    Args:
        default_return: Value to return on error
        log_traceback: Whether to log the full traceback
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except SpeechRecognitionError as e:
                logger.warning(f"Speech recognition error in {func.__name__}: {e}")
                return default_return
            
            except TTSError as e:
                logger.error(f"TTS error in {func.__name__}: {e}")
                return default_return
            
            except NetworkCommunicationError as e:
                logger.error(f"Network error in {func.__name__}: {e}")
                return default_return
                
            except ConfigurationError as e:
                logger.critical(f"Configuration error: {e}")
                raise # Critical errors should bubble up
            
            except KeyboardInterrupt:
                logger.info(f"User interrupted {func.__name__}")
                raise  # Re-raise to allow graceful shutdown
            
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                if log_traceback:
                    logger.error(traceback.format_exc())
                return default_return
        
        return wrapper
    return decorator