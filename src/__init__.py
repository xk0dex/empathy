"""
Proyecto Empathy - El smartwatch para la salud de tu equipo

Un analizador de dinámicas de equipo que proporciona insights sobre
la salud de la colaboración en equipos de desarrollo de software.
"""

from .__version__ import __version__, get_version_info, print_version_info
from .main import EmpathyAnalyzer
from .analysis.sentiment_analyzer import SentimentAnalyzer
from .analysis.collaboration_analyzer import CollaborationAnalyzer
from .data_collection.github_collector import GitHubCollector
from .visualization.dashboard import Dashboard

__author__ = "Proyecto Empathy Team"
__email__ = "empathy@ejemplo.com"

__all__ = [
    'EmpathyAnalyzer',
    'SentimentAnalyzer',
    'CollaborationAnalyzer', 
    'GitHubCollector',
    'Dashboard',
    '__version__',
    'get_version_info',
    'print_version_info'
]

def get_version():
    """Retorna la versión actual del sistema"""
    return __version__