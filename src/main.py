"""
Proyecto Empathy - El smartwatch para la salud de tu equipo de desarrollo

Este módulo principal orquesta la recopilación de datos, análisis y visualización
para proporcionar insights sobre la salud y dinámicas de equipos de desarrollo.
"""

import argparse
import logging
from pathlib import Path
import sys

# Añadir el directorio src al path para importaciones
sys.path.append(str(Path(__file__).parent))

from data_collection.github_collector import GitHubCollector
from analysis.sentiment_analyzer import SentimentAnalyzer
from analysis.collaboration_analyzer import CollaborationAnalyzer
from visualization.dashboard import Dashboard
from config.settings import load_config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmpathyAnalyzer:
    """
    Clase principal que coordina todo el proceso de análisis de empathy del equipo.
    """
    
    def __init__(self, config_path: str = None):
        """
        Inicializa el analizador con la configuración especificada.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config = load_config(config_path)
        self.github_collector = GitHubCollector(self.config)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.collaboration_analyzer = CollaborationAnalyzer()
        self.dashboard = Dashboard()
        
    def analyze_repository(self, repo_url: str, days_back: int = 30):
        """
        Realiza un análisis completo de empathy para un repositorio.
        
        Args:
            repo_url: URL del repositorio de GitHub
            days_back: Número de días hacia atrás para analizar
            
        Returns:
            dict: Resultados del análisis
        """
        logger.info(f"🚀 Iniciando análisis de empathy para: {repo_url}")
        
        # 1. Recopilación de datos
        logger.info("📥 Recopilando datos de GitHub...")
        raw_data = self.github_collector.collect_repository_data(repo_url, days_back)
        
        if not raw_data:
            logger.error("❌ No se pudieron recopilar datos del repositorio")
            return None
            
        logger.info(f"✅ Datos recopilados: {len(raw_data.get('commits', []))} commits, "
                   f"{len(raw_data.get('pull_requests', []))} PRs")
        
        # 2. Análisis de sentimientos
        logger.info("🧠 Analizando sentimientos y comunicación...")
        sentiment_results = self.sentiment_analyzer.analyze(raw_data)
        
        # 3. Análisis de colaboración
        logger.info("🤝 Analizando patrones de colaboración...")
        collaboration_results = self.collaboration_analyzer.analyze(raw_data)
        
        # 4. Combinar resultados
        results = {
            'repository': repo_url,
            'analysis_period_days': days_back,
            'sentiment_analysis': sentiment_results,
            'collaboration_analysis': collaboration_results,
            'summary': self._generate_summary(sentiment_results, collaboration_results),
            'recommendations': self._generate_recommendations(sentiment_results, collaboration_results)
        }
        
        logger.info("📊 Análisis completado exitosamente")
        return results
    
    def _generate_summary(self, sentiment_results: dict, collaboration_results: dict) -> dict:
        """
        Genera un resumen ejecutivo de los resultados del análisis.
        """
        # Calcular métricas de salud del equipo
        communication_health = sentiment_results.get('overall_sentiment_score', 0)
        collaboration_health = collaboration_results.get('collaboration_score', 0)
        knowledge_distribution = collaboration_results.get('knowledge_distribution_score', 0)
        
        overall_health = (communication_health + collaboration_health + knowledge_distribution) / 3
        
        return {
            'overall_team_health': overall_health,
            'communication_health': communication_health,
            'collaboration_health': collaboration_health,
            'knowledge_distribution': knowledge_distribution,
            'health_status': self._get_health_status(overall_health)
        }
    
    def _get_health_status(self, score: float) -> str:
        """
        Convierte el score numérico en un estado de salud legible.
        """
        if score >= 0.8:
            return "🌟 Excelente"
        elif score >= 0.6:
            return "😊 Bueno"
        elif score >= 0.4:
            return "😐 Regular"
        elif score >= 0.2:
            return "😕 Necesita atención"
        else:
            return "🚨 Crítico"
    
    def _generate_recommendations(self, sentiment_results: dict, collaboration_results: dict) -> list:
        """
        Genera recomendaciones basadas en los resultados del análisis.
        """
        recommendations = []
        
        # Recomendaciones basadas en sentimientos
        if sentiment_results.get('overall_sentiment_score', 0) < 0.5:
            recommendations.append({
                'type': 'communication',
                'priority': 'high',
                'message': '💬 El tono de la comunicación podría mejorar. Considera fomentar más retroalimentación positiva.'
            })
        
        # Recomendaciones basadas en colaboración
        if collaboration_results.get('knowledge_silos_detected', False):
            recommendations.append({
                'type': 'knowledge_sharing',
                'priority': 'medium',
                'message': '🔍 Se detectaron silos de conocimiento. Considera implementar pair programming o code reviews cruzados.'
            })
        
        if collaboration_results.get('collaboration_score', 0) < 0.5:
            recommendations.append({
                'type': 'collaboration',
                'priority': 'medium',
                'message': '🤝 La colaboración entre miembros podría mejorar. Considera reuniones regulares de sincronización.'
            })
        
        return recommendations


def main():
    """
    Función principal del programa.
    """
    parser = argparse.ArgumentParser(description='Empathy - Analizador de salud de equipos')
    parser.add_argument('--repo', required=True, help='URL del repositorio de GitHub')
    parser.add_argument('--days', type=int, default=30, help='Días hacia atrás para analizar (default: 30)')
    parser.add_argument('--config', help='Ruta al archivo de configuración')
    parser.add_argument('--output', help='Archivo de salida para los resultados (JSON)')
    parser.add_argument('--web', action='store_true', help='Abrir dashboard web')
    
    args = parser.parse_args()
    
    try:
        # Inicializar analizador
        analyzer = EmpathyAnalyzer(args.config)
        
        # Realizar análisis
        results = analyzer.analyze_repository(args.repo, args.days)
        
        if not results:
            logger.error("❌ El análisis falló")
            sys.exit(1)
        
        # Mostrar resumen en consola
        print("\n" + "="*60)
        print("🤝 REPORTE DE SALUD DEL EQUIPO - EMPATHY")
        print("="*60)
        
        summary = results['summary']
        print(f"\n📊 MÉTRICAS GENERALES:")
        print(f"   Salud General del Equipo: {summary['health_status']} ({summary['overall_team_health']:.2f})")
        print(f"   Comunicación: {summary['communication_health']:.2f}")
        print(f"   Colaboración: {summary['collaboration_health']:.2f}")
        print(f"   Distribución de Conocimiento: {summary['knowledge_distribution']:.2f}")
        
        print(f"\n💡 RECOMENDACIONES:")
        for rec in results['recommendations']:
            print(f"   {rec['message']}")
        
        # Guardar resultados si se especifica
        if args.output:
            import json
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"📄 Resultados guardados en: {args.output}")
        
        # Abrir dashboard web si se solicita
        if args.web:
            logger.info("🌐 Abriendo dashboard web...")
            analyzer.dashboard.show(results)
        
        print("\n✅ Análisis completado exitosamente")
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Análisis interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error durante el análisis: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()