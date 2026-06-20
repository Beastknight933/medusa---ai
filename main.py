import logging
from config import get_config
from stt import take_command, calibrate_microphone, get_microphone_source
from tts import speak, cleanup as tts_cleanup
from n8n_client import N8nClient
import Dictapp
from error_handler import handle_errors, NetworkCommunicationError

# Setup logging
config = get_config()
logging.basicConfig(
    level=getattr(logging, config.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.get('LOG_FILE', 'assistant.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def execute_local_action(action: str, target: str):
    """Executes a local action commanded by n8n."""
    if not action or not target:
        return

    logger.info(f"Executing local action: {action} on target: {target}")
    
    if action == "open_app":
        success = Dictapp.openappweb(target)
        if not success:
            logger.warning(f"Failed to open {target}. Sending failure notification to n8n could be implemented here.")
            # Optional: send a failure message back to n8n silently
            
    elif action == "close_app":
        Dictapp.closeappweb(target)
    
    else:
        logger.warning(f"Unknown action received from n8n: {action}")

@handle_errors(log_traceback=True)
def assistant_loop():
    """Main assistant loop connecting STT -> n8n -> TTS + Local Actions."""
    logger.info("Starting assistant loop")
    
    n8n = N8nClient()
    assistant_name = config.get('ASSISTANT_NAME')
    speak(f"Hello! I am {assistant_name}, online and ready.")
    
    with get_microphone_source() as source:
        try:
            calibrate_microphone(source)
        except Exception as e:
            logger.error(f"Microphone calibration failed: {e}")
            speak("I'm having trouble with my audio input, but I will try to continue.")
        
        while True:
            try:
                # 1. Listen
                query = take_command(source)
                
                if not query:
                    continue
                
                query = query.lower().strip()
                logger.info(f"User heard: {query}")
                
                # Check for local emergency exit
                if query in ["exit", "stop", "shutdown system", "goodbye"]:
                    speak("Shutting down. Goodbye, sir.")
                    break

                # 2. Communicate with n8n
                response = n8n.send_query(query)
                
                # 3. Respond with TTS
                speech = response.get("speech")
                if speech:
                    speak(speech)
                
                # 4. Execute Local Actions
                action = response.get("action")
                target = response.get("target")
                if action:
                    execute_local_action(action, target)
                    
            except KeyboardInterrupt:
                logger.info("User interrupted with Ctrl+C")
                speak("Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                speak("I encountered an internal error. Resuming operations.")

def cleanup():
    """Cleanup resources before exit."""
    logger.info("Cleaning up resources")
    try:
        tts_cleanup()
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("J.A.R.V.I.S. Architecture Assistant Starting")
    logger.info("=" * 50)
    
    if not config.validate():
        logger.warning("Configuration has warnings - check your n8n Webhook URL.")
    
    try:
        assistant_loop()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
    finally:
        cleanup()
        logger.info("Assistant Stopped")
