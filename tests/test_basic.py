"""
Tests básicos para el Proyecto Empathy.
"""

import pytest
import sys
from pathlib import Path

# Añadir src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def test_import_main_modules():
    """Prueba que los módulos principales se puedan importar."""
    from src.analysis.sentiment_analyzer import SentimentAnalyzer
    from src.analysis.collaboration_analyzer import CollaborationAnalyzer
    
    # Verificar que se pueden instanciar
    sentiment_analyzer = SentimentAnalyzer()
    collaboration_analyzer = CollaborationAnalyzer()
    
    assert sentiment_analyzer is not None
    assert collaboration_analyzer is not None

def test_sentiment_analyzer_basic():
    """Prueba básica del analizador de sentimientos."""
    from src.analysis.sentiment_analyzer import SentimentAnalyzer
    
    analyzer = SentimentAnalyzer()
    
    # Probar análisis de texto positivo
    result = analyzer._analyze_text("Great work! This is awesome!", "test")
    assert result.sentiment_score > 0
    assert result.sentiment_label == "positive"
    
    # Probar análisis de texto negativo
    result = analyzer._analyze_text("This is terrible and broken", "test")
    assert result.sentiment_score < 0
    assert result.sentiment_label == "negative"

def test_version_info():
    """Prueba que la información de versión esté disponible."""
    from src.__version__ import __version__, CREATOR, __author__
    
    assert __version__ == "1.1.1"
    assert CREATOR == "xk0dex"
    assert __author__ == "xk0dex"

def test_demo_data_generation():
    """Prueba que se puedan generar datos de demostración."""
    from demo import generate_demo_data
    
    data = generate_demo_data()
    
    assert 'commits' in data
    assert 'pull_requests' in data
    assert len(data['commits']) > 0
    assert len(data['pull_requests']) > 0

def test_github_collector_url_validation():
    """Prueba la validación de URLs del colector de GitHub."""
    from src.data_collection.github_collector import GitHubCollector
    
    # Crear una instancia mock
    config = {
        'github': {
            'token': 'test_token',
            'rate_limit_delay': 1
        }
    }
    
    # No podemos probar la inicialización completa sin token válido,
    # pero sí podemos probar el método de extracción
    collector = GitHubCollector.__new__(GitHubCollector)
    
    # Probar URLs válidas
    assert collector._extract_repo_name("owner/repo") == "owner/repo"
    assert collector._extract_repo_name("https://github.com/owner/repo") == "owner/repo"
    assert collector._extract_repo_name("https://github.com/owner/repo.git") == "owner/repo"
    
    # Probar URLs inválidas
    with pytest.raises(ValueError):
        collector._extract_repo_name("")
    
    with pytest.raises(ValueError):
        collector._extract_repo_name("invalid-format")
    
    with pytest.raises(ValueError):
        collector._extract_repo_name(None)

if __name__ == "__main__":
    pytest.main([__file__])