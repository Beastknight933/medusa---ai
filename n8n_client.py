import requests
import logging
from datetime import datetime
import platform
from config import get_config
from error_handler import retry, NetworkCommunicationError

logger = logging.getLogger(__name__)

class N8nClient:
    def __init__(self):
        self.config = get_config()
        self.webhook_url = self.config.get('N8N_WEBHOOK_URL')

    @retry(max_attempts=3, delay=1.0, exceptions=(requests.exceptions.RequestException,))
    def send_query(self, text: str) -> dict:
        """
        Sends the transcribed text and system context to the n8n webhook.
        Returns a dictionary containing the n8n response instructions.
        Expected n8n response format:
        {
            "speech": "Text for the TTS to speak",
            "action": "open_app" | "close_app" | null,
            "target": "app_name" | null
        }
        """
        if not text:
            return {"speech": "", "action": None, "target": None}

        payload = {
            "text": text,
            "context": {
                "timestamp": datetime.now().isoformat(),
                "system": platform.system(),
                "assistant_name": self.config.get('ASSISTANT_NAME')
            }
        }

        try:
            logger.info(f"Sending to n8n: '{text}'")
            response = requests.post(self.webhook_url, json=payload, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Received from n8n: {data}")
            
            return {
                "speech": data.get("speech", ""),
                "action": data.get("action"),
                "target": data.get("target")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to communicate with n8n webhook: {e}")
            raise NetworkCommunicationError(f"Failed to communicate with n8n webhook: {e}")
        except ValueError:
            logger.error("Failed to parse JSON response from n8n.")
            raise NetworkCommunicationError("Failed to parse JSON response from n8n.")

