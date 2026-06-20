import os
import json
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Config:
    """
    Centralized configuration management.
    Supports environment variables, config files, and defaults.
    """
    
    # ---------- DEFAULT CONFIGURATIONS ----------
    DEFAULTS = {
        # n8n Webhook Settings (Required)
        'N8N_WEBHOOK_URL': 'http://localhost:5678/webhook/assistant',
        
        # TTS Settings
        'TTS_VOICE': 'en-US-MichelleNeural',
        'TTS_RATE': 'medium',
        'TTS_VOLUME': 1.0,
        
        # STT Settings
        'STT_TIMEOUT': 8,
        'STT_PHRASE_TIME_LIMIT': 3,
        'STT_LANGUAGE': 'en-US',
        'STT_ENERGY_THRESHOLD': 300,
        'STT_PAUSE_THRESHOLD': 1.5,
        
        # Assistant Settings
        'ASSISTANT_NAME': 'Ashley',
        'LOG_LEVEL': 'INFO',
        
        # File Paths
        'LOG_FILE': 'assistant.log',
        'CONFIG_FILE': 'config.json',
        
        # Feature Flags
        'AUTO_CLEANUP_TTS': True,
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        """
        self._config: Dict[str, Any] = self.DEFAULTS.copy()
        self._config_file = config_file or self.DEFAULTS['CONFIG_FILE']
        
        self._load_from_file()
        self._load_from_env()
        
        logger.info("Configuration loaded successfully")
    
    def _load_from_file(self):
        """Load configuration from JSON file."""
        try:
            if os.path.exists(self._config_file):
                with open(self._config_file, 'r') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
                    logger.info(f"Loaded config from {self._config_file}")
        except Exception as e:
            logger.warning(f"Could not load config file: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'N8N_WEBHOOK_URL': 'N8N_WEBHOOK_URL',
            'TTS_VOICE': 'TTS_VOICE',
            'STT_LANGUAGE': 'STT_LANGUAGE',
            'ASSISTANT_NAME': 'ASSISTANT_NAME',
            'LOG_LEVEL': 'LOG_LEVEL',
        }
        
        for config_key, env_key in env_mappings.items():
            env_value = os.getenv(env_key)
            if env_value is not None:
                self._config[config_key] = env_value
                logger.debug(f"Loaded {config_key} from environment")
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        self._config[key] = value
    
    def save(self):
        """Save current configuration to file."""
        try:
            with open(self._config_file, 'w') as f:
                json.dump(self._config, f, indent=4)
                logger.info(f"Configuration saved to {self._config_file}")
        except Exception as e:
            logger.error(f"Could not save config file: {e}")
    
    def validate(self) -> bool:
        from error_handler import ConfigurationError
        warnings = []
        
        webhook_url = self.get('N8N_WEBHOOK_URL')
        if not webhook_url:
            raise ConfigurationError("N8N_WEBHOOK_URL is missing. Please set it in config.json or environment variables.")
        
        if webhook_url == 'http://localhost:5678/webhook/assistant':
            warnings.append("Using default n8n webhook URL. Ensure it matches your actual n8n setup.")
            
        for warning in warnings:
            logger.warning(warning)
            
        return len(warnings) == 0
    
    def __getitem__(self, key: str) -> Any:
        return self._config[key]
    
    def __setitem__(self, key: str, value: Any):
        self._config[key] = value
    
    def __contains__(self, key: str) -> bool:
        return key in self._config
    
    def to_dict(self) -> Dict[str, Any]:
        return self._config.copy()


# ---------- GLOBAL CONFIG INSTANCE ----------
_config_instance: Optional[Config] = None

def get_config() -> Config:
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance