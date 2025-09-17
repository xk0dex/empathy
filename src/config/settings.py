"""
Configuración y ajustes para el Proyecto Empathy.
"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Carga la configuración desde archivos de entorno y YAML.
    
    Args:
        config_path: Ruta al archivo de configuración YAML
        
    Returns:
        Diccionario con la configuración completa
    """
    # Cargar variables de entorno
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    config = {
        # Configuración de GitHub API
        'github': {
            'token': os.getenv('GITHUB_TOKEN'),
            'api_url': os.getenv('GITHUB_API_URL', 'https://api.github.com'),
            'rate_limit_delay': int(os.getenv('GITHUB_RATE_LIMIT_DELAY', '1')),
        },
        
        # Configuración de análisis
        'analysis': {
            'sentiment_model': os.getenv('SENTIMENT_MODEL', 'vader'),
            'language': os.getenv('ANALYSIS_LANGUAGE', 'en'),
            'confidence_threshold': float(os.getenv('CONFIDENCE_THRESHOLD', '0.5')),
        },
        
        # Configuración de base de datos
        'database': {
            'url': os.getenv('DATABASE_URL', 'sqlite:///empathy.db'),
            'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
        },
        
        # Configuración de dashboard web
        'web': {
            'host': os.getenv('WEB_HOST', '127.0.0.1'),
            'port': int(os.getenv('WEB_PORT', '8080')),
            'debug': os.getenv('WEB_DEBUG', 'False').lower() == 'true',
        },
        
        # Configuración de logging
        'logging': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'format': os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s'),
        },
        
        # Configuración de métricas
        'metrics': {
            'collaboration_threshold': float(os.getenv('COLLABORATION_THRESHOLD', '0.5')),
            'sentiment_threshold': float(os.getenv('SENTIMENT_THRESHOLD', '0.3')),
            'knowledge_silo_threshold': float(os.getenv('KNOWLEDGE_SILO_THRESHOLD', '0.8')),
        }
    }
    
    # Cargar configuración adicional desde YAML si se proporciona
    if config_path and Path(config_path).exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            yaml_config = yaml.safe_load(f)
            config.update(yaml_config)
    
    # Validar configuración crítica
    _validate_config(config)
    
    return config


def _validate_config(config: Dict[str, Any]) -> None:
    """
    Valida que la configuración tenga los valores requeridos.
    
    Args:
        config: Diccionario de configuración a validar
        
    Raises:
        ValueError: Si falta configuración crítica
    """
    # Validar token de GitHub
    if not config['github']['token']:
        raise ValueError(
            "❌ TOKEN DE GITHUB REQUERIDO: "
            "Por favor configura GITHUB_TOKEN en tu archivo .env o variables de entorno. "
            "Puedes generar un token en: https://github.com/settings/tokens"
        )
    
    # Validar que el token tenga el formato correcto
    github_token = config['github']['token']
    if not (github_token.startswith('ghp_') or github_token.startswith('github_pat_')):
        print("⚠️  ADVERTENCIA: El token de GitHub podría no tener el formato esperado")


# Configuraciones por defecto para diferentes entornos
DEFAULT_CONFIGS = {
    'development': {
        'web': {'debug': True},
        'logging': {'level': 'DEBUG'},
    },
    'production': {
        'web': {'debug': False},
        'logging': {'level': 'INFO'},
        'github': {'rate_limit_delay': 2},
    },
    'testing': {
        'database': {'url': 'sqlite:///:memory:'},
        'logging': {'level': 'WARNING'},
    }
}


def get_environment_config(env: str = None) -> Dict[str, Any]:
    """
    Obtiene configuración específica para un entorno.
    
    Args:
        env: Nombre del entorno ('development', 'production', 'testing')
        
    Returns:
        Configuración específica del entorno
    """
    if not env:
        env = os.getenv('EMPATHY_ENV', 'development')
    
    return DEFAULT_CONFIGS.get(env, DEFAULT_CONFIGS['development'])