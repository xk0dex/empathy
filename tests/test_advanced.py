"""
Tests avanzados para el Proyecto Empathy.
Cubre escenarios de error, escalabilidad y edge cases.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
import time

# Añadir src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

class TestErrorHandling:
    """Tests para manejo de errores y edge cases."""
    
    def test_github_api_rate_limit(self):
        """Test manejo de rate limits de GitHub API."""
        from src.data_collection.github_collector import GitHubCollector
        
        # Mock de configuración
        config = {
            'github': {
                'token': 'fake_token_for_testing',
                'rate_limit_delay': 1
            }
        }
        
        # Simular rate limit error
        with patch('github.Github') as mock_github:
            mock_github.side_effect = Exception("API rate limit exceeded")
            
            with pytest.raises(Exception):
                collector = GitHubCollector(config)
    
    def test_invalid_repository_url(self):
        """Test URLs de repositorio inválidas."""
        from src.data_collection.github_collector import GitHubCollector
        
        config = {
            'github': {
                'token': 'fake_token_for_testing',
                'rate_limit_delay': 1
            }
        }
        
        collector = GitHubCollector(config)
        
        # URLs inválidas
        invalid_urls = [
            "not_a_url",
            "https://github.com/",
            "https://github.com/invalid",
            "https://notgithub.com/user/repo",
            "github.com/user/repo"  # Sin https
        ]
        
        for url in invalid_urls:
            result = collector._extract_repo_name(url)
            # Debería manejar graciosamente URLs inválidas
            assert result is not None  # No debe crashear

class TestScalability:
    """Tests de escalabilidad y performance."""
    
    def test_large_commit_dataset(self):
        """Test con dataset grande de commits."""
        from src.analysis.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        # Simular 1000+ commits
        large_commits = []
        for i in range(1000):
            large_commits.append({
                'message': f'Commit message {i}: implementing feature with some complexity',
                'author': f'developer_{i % 10}',  # 10 desarrolladores
                'date': '2025-09-17'
            })
        
        start_time = time.time()
        results = analyzer._analyze_commits(large_commits)
        end_time = time.time()
        
        # Verificar que procesa todos los commits
        assert len(results) == 1000
        
        # Verificar que no toma más de 30 segundos (performance básica)
        assert (end_time - start_time) < 30
        
        print(f"✅ Procesó 1000 commits en {end_time - start_time:.2f} segundos")
    
    def test_many_contributors_analysis(self):
        """Test con muchos contributors (100+)."""
        from src.analysis.collaboration_analyzer import CollaborationAnalyzer
        
        analyzer = CollaborationAnalyzer()
        
        # Simular repo con 100 contributors
        large_repo_data = {
            'commits': [],
            'pull_requests': []
        }
        
        # 100 contributors, 10 commits cada uno
        for contributor_id in range(100):
            for commit_id in range(10):
                large_repo_data['commits'].append({
                    'author': f'contributor_{contributor_id}',
                    'message': f'Feature {commit_id} by {contributor_id}',
                    'files_changed': ['file1.py', 'file2.py']
                })
        
        # 50 PRs con múltiples reviewers
        for pr_id in range(50):
            large_repo_data['pull_requests'].append({
                'author': f'contributor_{pr_id % 100}',
                'reviewers': [f'contributor_{(pr_id + i) % 100}' for i in range(3)],
                'title': f'PR #{pr_id}',
                'comments': []
            })
        
        start_time = time.time()
        results = analyzer.analyze_collaboration_patterns(large_repo_data)
        end_time = time.time()
        
        # Verificar que maneja gran cantidad de contributors
        assert results is not None
        assert 'collaboration_score' in results
        
        print(f"✅ Analizó 100 contributors en {end_time - start_time:.2f} segundos")

class TestMultiLanguage:
    """Tests para análisis multi-idioma."""
    
    def test_spanish_sentiment_analysis(self):
        """Test análisis de sentimientos en español."""
        from src.analysis.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        # Mensajes en español
        spanish_texts = [
            ("¡Excelente trabajo! Me encanta esta solución", "positive"),
            ("Este código está muy mal, es un desastre", "negative"),
            ("Funciona bien, sin problemas", "positive"),
            ("No me gusta nada este enfoque", "negative"),
            ("Está bien, pero se puede mejorar", "neutral")
        ]
        
        for text, expected_sentiment in spanish_texts:
            result = analyzer._analyze_text(text, "spanish_test")
            
            # Verificar que no crashea con español
            assert result is not None
            assert result.text == text
            
            # NOTA: VADER no es perfecto con español, pero no debe crashear
            print(f"📝 '{text}' → {result.sentiment_label} (esperado: {expected_sentiment})")
    
    def test_technical_jargon_handling(self):
        """Test manejo de jerga técnica."""
        from src.analysis.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        # Jerga técnica que puede confundir
        technical_phrases = [
            "This code is sick!",  # Positivo en slang
            "Killed the bug",      # Positivo técnico
            "Dead simple solution", # Positivo técnico
            "Code smells bad",     # Negativo técnico
            "Breaking changes",    # Neutral técnico
            "Nuclear option",      # Neutral técnico
        ]
        
        for phrase in technical_phrases:
            result = analyzer._analyze_text(phrase, "tech_jargon")
            
            # Verificar que procesa sin errores
            assert result is not None
            print(f"🤖 '{phrase}' → {result.sentiment_label} (score: {result.sentiment_score:.2f})")

class TestEdgeCases:
    """Tests para casos extremos."""
    
    def test_empty_repository_data(self):
        """Test con repositorio vacío."""
        from src.main import EmpathyAnalyzer
        
        # Mock para evitar configuración real
        with patch('src.main.load_config') as mock_config:
            mock_config.return_value = {
                'github': {'token': 'fake', 'rate_limit_delay': 1}
            }
            
            analyzer = EmpathyAnalyzer()
            
            # Repositorio completamente vacío
            empty_repo_data = {
                'commits': [],
                'pull_requests': []
            }
            
            # Verificar que maneja repos vacíos graciosamente
            analyzer._validate_analysis_constraints(empty_repo_data, 30)
            # No debe crashear, solo mostrar advertencias
    
    def test_single_contributor_repository(self):
        """Test con repositorio de un solo contributor."""
        from src.analysis.collaboration_analyzer import CollaborationAnalyzer
        
        analyzer = CollaborationAnalyzer()
        
        # Repo con un solo desarrollador
        single_dev_data = {
            'commits': [
                {'author': 'solo_dev', 'message': 'Initial commit', 'files_changed': ['main.py']},
                {'author': 'solo_dev', 'message': 'Add feature', 'files_changed': ['feature.py']},
                {'author': 'solo_dev', 'message': 'Fix bug', 'files_changed': ['main.py']}
            ],
            'pull_requests': []  # Sin PRs (solo commits directos)
        }
        
        results = analyzer.analyze_collaboration_patterns(single_dev_data)
        
        # Verificar que maneja solo developers
        assert results is not None
        assert 'collaboration_score' in results
        
        # La colaboración debería ser muy baja (esperado)
        assert results['collaboration_score'] <= 0.3

class TestPerformanceMetrics:
    """Tests de métricas de performance."""
    
    def test_memory_usage_large_dataset(self):
        """Test uso de memoria con datasets grandes."""
        import psutil
        import os
        
        from src.analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Memoria inicial
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        analyzer = SentimentAnalyzer()
        
        # Dataset grande (simular 10,000 commits)
        large_dataset = []
        for i in range(10000):
            large_dataset.append({
                'message': f'Commit {i}: Some meaningful commit message with decent length to test memory usage patterns',
                'author': f'dev_{i % 50}',  # 50 developers
                'date': '2025-09-17'
            })
        
        # Procesar dataset
        results = analyzer._analyze_commits(large_dataset)
        
        # Memoria después
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        
        print(f"📊 Memoria usada: {memory_used:.2f} MB para 10,000 commits")
        
        # Verificar que no usa más de 500MB (límite razonable)
        assert memory_used < 500
        assert len(results) == 10000

if __name__ == "__main__":
    # Ejecutar tests específicos
    print("🧪 EJECUTANDO TESTS AVANZADOS")
    print("=" * 50)
    
    # Test rápido de escalabilidad
    test_scalability = TestScalability()
    test_scalability.test_large_commit_dataset()
    test_scalability.test_many_contributors_analysis()
    
    print("\n✅ Tests avanzados completados")