#!/usr/bin/env python3
"""
Script de demostración de Proyecto Empathy.

Este script ejecuta un análisis de ejemplo con datos simulados
para mostrar las capacidades del sistema.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import argparse

# Añadir src al path
sys.path.append(str(Path(__file__).parent / 'src'))

from main import EmpathyAnalyzer
from data_collection.github_collector import CommitData, PullRequestData
from __version__ import get_version_info, print_version_info, __version__, print_banner, CREATOR, __github__


def generate_demo_data():
    """Genera datos de demostración para mostrar las capacidades de Empathy."""
    
    # Simular commits
    commits = []
    authors = ['alice', 'bob', 'charlie', 'diana']
    commit_messages = [
        "Fix critical bug in authentication module",
        "Add new feature for user dashboard",
        "Refactor payment processing logic", 
        "Update documentation and README",
        "Implement unit tests for API endpoints",
        "Fix typo in error message",
        "Optimize database queries for performance",
        "Add validation for user input forms"
    ]
    
    for i in range(30):
        author = random.choice(authors)
        message = random.choice(commit_messages)
        
        commit = CommitData(
            sha=f"abc123{i:03d}",
            author=author,
            author_email=f"{author}@example.com",
            message=message,
            timestamp=datetime.now() - timedelta(days=random.randint(1, 30)),
            files_changed=[f"src/{random.choice(['auth', 'api', 'ui'])}/{random.choice(['main', 'utils', 'test'])}.py"],
            additions=random.randint(5, 50),
            deletions=random.randint(0, 20)
        )
        commits.append(commit)
    
    # Simular pull requests
    pull_requests = []
    pr_titles = [
        "Implement new authentication system",
        "Add dashboard analytics features", 
        "Fix security vulnerability in API",
        "Improve user experience in checkout",
        "Add comprehensive test coverage",
        "Update dependencies and fix deprecations"
    ]
    
    positive_comments = [
        "Great work! This looks good to me.",
        "Nice implementation, thanks for the fix!",
        "Excellent solution to this problem.",
        "Well done, the code is clean and readable."
    ]
    
    negative_comments = [
        "This approach doesn't seem right to me.",
        "I think there might be a bug in this logic.",
        "This could be implemented more efficiently.",
        "Please add more error handling here."
    ]
    
    for i in range(10):
        author = random.choice(authors)
        title = random.choice(pr_titles)
        
        # Generar comentarios
        comments = []
        for j in range(random.randint(1, 5)):
            commenter = random.choice([a for a in authors if a != author])
            comment_text = random.choice(positive_comments + negative_comments)
            comments.append({
                'author': commenter,
                'body': comment_text,
                'created_at': datetime.now() - timedelta(days=random.randint(1, 15))
            })
        
        # Generar reviews
        reviews = []
        for reviewer in random.sample([a for a in authors if a != author], random.randint(1, 3)):
            review_text = random.choice(positive_comments)
            reviews.append({
                'author': reviewer,
                'state': random.choice(['APPROVED', 'COMMENTED', 'CHANGES_REQUESTED']),
                'body': review_text,
                'submitted_at': datetime.now() - timedelta(days=random.randint(1, 10))
            })
        
        pr = PullRequestData(
            number=i + 1,
            title=title,
            author=author,
            state=random.choice(['open', 'closed', 'merged']),
            created_at=datetime.now() - timedelta(days=random.randint(1, 20)),
            merged_at=datetime.now() - timedelta(days=random.randint(1, 15)) if random.choice([True, False]) else None,
            comments=comments,
            reviews=reviews,
            files_changed=[f"src/{random.choice(['auth', 'api', 'ui'])}.py"]
        )
        pull_requests.append(pr)
    
    # Simular contributors
    contributors = []
    for author in authors:
        contributors.append({
            'login': author,
            'contributions': random.randint(10, 100),
            'type': 'User',
            'avatar_url': f'https://github.com/{author}.png'
        })
    
    return {
        'repository_info': {
            'name': 'demo-project',
            'full_name': 'empathy/demo-project',
            'description': 'Proyecto de demostración para Empathy',
            'language': 'Python',
            'stars': 42,
            'forks': 7,
            'created_at': datetime.now() - timedelta(days=365),
            'updated_at': datetime.now(),
            'default_branch': 'main'
        },
        'commits': commits,
        'pull_requests': pull_requests,
        'contributors': contributors,
        'collection_metadata': {
            'collected_at': datetime.now(),
            'days_analyzed': 30,
            'since_date': datetime.now() - timedelta(days=30)
        }
    }


class DemoAnalyzer(EmpathyAnalyzer):
    """Analizador de demostración que usa datos simulados."""
    
    def __init__(self):
        """Inicializa el analizador de demo sin configuración externa."""
        # Configuración mínima para demo
        self.config = {
            'analysis': {
                'sentiment_model': 'vader',
                'language': 'en',
                'confidence_threshold': 0.5,
            },
            'metrics': {
                'collaboration_threshold': 0.5,
                'sentiment_threshold': 0.3,
                'knowledge_silo_threshold': 0.8,
            }
        }
        
        # Importar módulos de análisis
        from analysis.sentiment_analyzer import SentimentAnalyzer
        from analysis.collaboration_analyzer import CollaborationAnalyzer
        from visualization.dashboard import Dashboard
        
        self.sentiment_analyzer = SentimentAnalyzer()
        self.collaboration_analyzer = CollaborationAnalyzer()
        self.dashboard = Dashboard(self.config)
    
    def analyze_demo_data(self):
        """Ejecuta análisis con datos de demostración."""
        # Mostrar banner con marca de agua
        print(print_banner())
        print(f"🚀 Ejecutando demostración de Proyecto Empathy v{__version__}...")
        print("=" * 60)
        
        # Generar datos de demo
        print("📊 Generando datos de demostración...")
        raw_data = generate_demo_data()
        
        print(f"✅ Datos generados: {len(raw_data['commits'])} commits, "
              f"{len(raw_data['pull_requests'])} PRs")
        
        # Análizar sentimientos
        print("🧠 Analizando sentimientos...")
        sentiment_results = self.sentiment_analyzer.analyze(raw_data)
        
        # Analizar colaboración
        print("🤝 Analizando colaboración...")
        collaboration_results = self.collaboration_analyzer.analyze(raw_data)
        
        # Combinar resultados
        results = {
            'repository': 'empathy/demo-project',
            'analysis_period_days': 30,
            'sentiment_analysis': sentiment_results,
            'collaboration_analysis': collaboration_results,
            'summary': self._generate_summary(sentiment_results, collaboration_results),
            'recommendations': self._generate_recommendations(sentiment_results, collaboration_results)
        }
        
        # Mostrar resumen
        self._show_demo_summary(results)
        
        return results
    
    def _show_demo_summary(self, results):
        """Muestra un resumen de los resultados de la demo."""
        print("\n" + "=" * 60)
        print("🤝 REPORTE DE DEMOSTRACIÓN - EMPATHY")
        print("=" * 60)
        
        summary = results['summary']
        print(f"\n📊 MÉTRICAS GENERALES:")
        print(f"   Salud General del Equipo: {summary['health_status']} ({summary['overall_team_health']:.2f})")
        print(f"   Comunicación: {summary['communication_health']:.2f}")
        print(f"   Colaboración: {summary['collaboration_health']:.2f}")
        print(f"   Distribución de Conocimiento: {summary['knowledge_distribution']:.2f}")
        
        # Mostrar algunos detalles del análisis
        sentiment_metrics = results['sentiment_analysis']['overall_metrics']
        print(f"\n💭 ANÁLISIS DE SENTIMIENTOS:")
        print(f"   Sentimientos Positivos: {sentiment_metrics['positive_ratio']:.1%}")
        print(f"   Sentimientos Negativos: {sentiment_metrics['negative_ratio']:.1%}")
        print(f"   Sentimientos Neutrales: {sentiment_metrics['neutral_ratio']:.1%}")
        
        team_metrics = results['collaboration_analysis']['team_health_metrics']
        print(f"\n👥 MÉTRICAS DEL EQUIPO:")
        print(f"   Tamaño del Equipo: {team_metrics['team_size']} miembros")
        print(f"   Contributors Activos: {team_metrics['active_contributors']}")
        print(f"   Participación en Reviews: {team_metrics['review_participation_rate']:.1%}")
        
        silos = results['collaboration_analysis']['knowledge_silos']
        if silos:
            print(f"\n🚨 SILOS DE CONOCIMIENTO:")
            for silo in silos[:3]:  # Mostrar máximo 3
                print(f"   {silo.primary_owner}: {len(silo.files)} archivos ({silo.ownership_percentage:.1%})")
        
        print(f"\n💡 RECOMENDACIONES:")
        for rec in results['recommendations']:
            print(f"   {rec['message']}")
        
        print(f"\n🌐 Para ver el dashboard interactivo, ejecuta:")
        print(f"   python demo.py --web")
        print()
        print("✅ Demostración completada exitosamente")
        print(f"📧 Creado por: {CREATOR} | 🔗 {__github__}")
        print("⭐ Si te gusta, danos una estrella en GitHub!")


def main():
    """Función principal de la demostración."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Demo de Proyecto Empathy')
    parser.add_argument('--web', action='store_true', help='Mostrar dashboard web')
    parser.add_argument('--export', help='Exportar reporte a archivo HTML')
    
    args = parser.parse_args()
    
    try:
        # Crear analizador de demo
        analyzer = DemoAnalyzer()
        
        # Ejecutar análisis
        results = analyzer.analyze_demo_data()
        
        # Exportar si se solicita
        if args.export:
            analyzer.dashboard.export_static_report(args.export)
            print(f"\n📄 Reporte exportado a: {args.export}")
        
        # Mostrar dashboard si se solicita
        if args.web:
            print("\n🌐 Abriendo dashboard web...")
            analyzer.dashboard.show(results)
        
        print("\n✅ Demostración completada exitosamente")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error durante la demo: {str(e)}")
        sys.exit(1)


def web_demo():
    """Lanza dashboard web para demo"""
    print("🌐 Iniciando dashboard web para demostración...")
    
    # Generar datos de demostración
    demo_data = generate_demo_data()
    commit_data = demo_data['commits']
    pr_data = demo_data['pull_requests']
    
    # Crear datos de análisis mock para el dashboard
    analysis_results = {
        'summary': {
            'team_health_score': 0.65,
            'sentiment_distribution': {
                'positive': 58.8,
                'negative': 10.6,
                'neutral': 30.6
            },
            'collaboration_score': 0.75,
            'knowledge_distribution_score': 0.60,
            'total_commits': len(commit_data),
            'total_pull_requests': len(pr_data),
            'team_size': 4,
            'active_contributors': 4
        },
        'sentiment_analysis': {
            'overall_sentiment': 0.24,
            'sentiment_distribution': {
                'positive': 58.8,
                'negative': 10.6,
                'neutral': 30.6
            },
            'sentiment_trends': [],
            'toxic_patterns': []
        },
        'collaboration_analysis': {
            'collaboration_score': 0.75,
            'knowledge_silos': [
                {'contributor': 'alice', 'files': 1, 'isolation_score': 1.0},
                {'contributor': 'bob', 'files': 1, 'isolation_score': 0.8}
            ],
            'review_participation': 1.0,
            'cross_team_interactions': 0.6
        },
        'recommendations': [
            "💬 El tono de la comunicación podría mejorar. Considera fomentar más retroalimentación positiva.",
            "🔍 Se detectaron silos de conocimiento. Considera implementar pair programming o code reviews cruzados.",
            "🤝 Excelente participación en reviews. ¡Sigue así!",
            "📊 El team health está en nivel bueno. Mantén las prácticas actuales."
        ]
    }
    
    # Inicializar dashboard
    from src.visualization.dashboard import Dashboard
    dashboard = Dashboard()
    
    # Lanzar servidor
    print("📊 Dashboard disponible en: http://localhost:8080")
    print("🎯 Perfecto para demos en vivo!")
    print("🚀 Presiona Ctrl+C para detener el servidor")
    
    try:
        dashboard.show(analysis_results, auto_open=False)
    except KeyboardInterrupt:
        print("\n✅ Demo web finalizada exitosamente")

def parse_arguments():
    """Parsea argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Demo de Proyecto Empathy - Analizador de salud de equipos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Ejemplos:
  {sys.argv[0]}            # Demo básico en terminal
  {sys.argv[0]} --web      # Demo con dashboard web
  {sys.argv[0]} --version  # Mostrar información de versión
        """
    )
    
    parser.add_argument(
        '--web', 
        action='store_true',
        help='Lanzar demo con dashboard web interactivo'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true', 
        help='Mostrar información de versión'
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.version:
        print_version_info()
        sys.exit(0)
    elif args.web:
        web_demo()
    else:
        main()