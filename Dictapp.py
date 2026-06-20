import os
import shutil
import logging

logger = logging.getLogger(__name__)

# Core application dictionary mapping common names to executable names
basic_app_dict = {
    "commandprompt": "cmd",
    "cmd": "cmd",
    "paint": "paint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "code": "code",
    "powerpoint": "powerpnt",
    "notepad": "notepad",
    "spotify": "spotify",
}

def openappweb(target: str) -> bool:
    """
    Attempts to open a local application or website based on the target string provided by n8n.
    Returns True if successful, False otherwise.
    """
    if not target:
        logger.warning("No target provided to open.")
        return False
        
    target = target.lower().strip()
    logger.info(f"Attempting to open: {target}")

    # Check if it's a website
    if target.startswith("http") or target.startswith("www."):
        import webbrowser
        if not target.startswith("http"):
            target = f"https://{target}"
        webbrowser.open(target)
        return True

    # Check dictionary mapping
    if target in basic_app_dict:
        exe = basic_app_dict[target]
        logger.info(f"Found {target} in dict, launching {exe}")
        os.system(f"start {exe}")
        return True

    # Fallback: check if executable exists in PATH
    if shutil.which(target):
        logger.info(f"Found {target} in PATH, launching")
        os.system(f"start {target}")
        return True

    # Last resort: just try to start it, Windows might resolve it
    logger.info(f"Target {target} not explicitly found, attempting generic start")
    # Using 'start "" "target"' to avoid issues with spaces or command prompt hijacking
    result = os.system(f'start "" "{target}"')
    
    if result == 0:
        return True
    else:
        logger.error(f"Failed to open {target}")
        return False

def closeappweb(target: str) -> bool:
    """
    Attempts to close a local application based on the target string provided by n8n.
    Returns True if successful, False otherwise.
    """
    if not target:
        logger.warning("No target provided to close.")
        return False

    target = target.lower().strip()
    logger.info(f"Attempting to close: {target}")

    exe_name = basic_app_dict.get(target, target)
    
    # taskkill requires .exe extension usually
    if not exe_name.endswith(".exe"):
        exe_name += ".exe"

    result = os.system(f"taskkill /f /im {exe_name}")
    
    if result == 0:
        logger.info(f"Successfully closed {exe_name}")
        return True
    else:
        logger.error(f"Failed to close {exe_name}")
        return False
