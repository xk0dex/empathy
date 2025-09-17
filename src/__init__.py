"""
Proyecto Empathy - El smartwatch para la salud de tu equipo

Un analizador de dinámicas de equipo que proporciona insights sobre
la salud de la colaboración en equipos de desarrollo de software.

Creado por: xk0dex
GitHub: https://github.com/xk0dex
Repositorio: https://github.com/xk0dex/empathy
© 2025 xk0dex. All rights reserved.
"""

from .__version__ import __version__, get_version_info, print_version_info, print_banner, CREATOR, __author__, __github__
from .main import EmpathyAnalyzer
from .analysis.sentiment_analyzer import SentimentAnalyzer
from .analysis.collaboration_analyzer import CollaborationAnalyzer
from .data_collection.github_collector import GitHubCollector
from .visualization.dashboard import Dashboard

__author__ = "xk0dex"
__email__ = "xk0dex@github.com"
__creator__ = "xk0dex"
__github_profile__ = "https://github.com/xk0dex"
__repository__ = "https://github.com/xk0dex/empathy"

__all__ = [
    'EmpathyAnalyzer',
    'SentimentAnalyzer',
    'CollaborationAnalyzer', 
    'GitHubCollector',
    'Dashboard',
    '__version__',
    'get_version_info',
    'print_version_info',
    'print_banner',
    '__author__',
    '__creator__',
    '__github_profile__'
]

def get_version():
    """Retorna la versión actual del sistema"""
    return __version__

def get_author_info():
    """Retorna información del autor"""
    return {
        'creator': CREATOR,
        'github': __github_profile__,
        'repository': __repository__,
        'email': __email__
    }