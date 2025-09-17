"""
Dashboard web para visualizar métricas de Proyecto Empathy.

Este módulo proporciona una interfaz web interactiva para:
- Visualizar métricas de salud del equipo
- Mostrar análisis de sentimientos
- Presentar patrones de colaboración
- Alertas y recomendaciones
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import webbrowser
import threading
import time

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

logger = logging.getLogger(__name__)


class Dashboard:
    """
    Dashboard web para visualizar resultados de análisis de Empathy.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el dashboard web.
        
        Args:
            config: Configuración del dashboard
        """
        self.config = config or {}
        self.app = Flask(__name__, 
                        template_folder=str(Path(__file__).parent / 'templates'),
                        static_folder=str(Path(__file__).parent / 'static'))
        CORS(self.app)
        
        self.analysis_results = {}
        self.setup_routes()
        
        # Configuración del servidor
        self.host = self.config.get('web', {}).get('host', '127.0.0.1')
        self.port = self.config.get('web', {}).get('port', 8080)
        self.debug = self.config.get('web', {}).get('debug', False)
    
    def setup_routes(self):
        """Configura las rutas del dashboard."""
        
        @self.app.route('/')
        def index():
            """Página principal del dashboard."""
            return render_template('dashboard.html')
        
        @self.app.route('/api/data')
        def get_data():
            """API endpoint para obtener datos de análisis."""
            return jsonify(self.analysis_results)
        
        @self.app.route('/api/health')
        def health_check():
            """Health check del dashboard."""
            from ..__version__ import CREATOR, __github__, __version__
            return jsonify({
                'status': 'healthy', 
                'version': __version__,
                'created_by': CREATOR,
                'github': __github__,
                'repository': 'https://github.com/xk0dex/empathy'
            })
        
        @self.app.route('/api/summary')
        def get_summary():
            """Obtiene resumen ejecutivo de las métricas."""
            if not self.analysis_results:
                return jsonify({'error': 'No data available'})
            
            summary = self.analysis_results.get('summary', {})
            return jsonify(summary)
        
        @self.app.route('/api/sentiment')
        def get_sentiment_data():
            """Obtiene datos específicos de análisis de sentimientos."""
            if not self.analysis_results:
                return jsonify({'error': 'No data available'})
            
            sentiment_data = self.analysis_results.get('sentiment_analysis', {})
            return jsonify(sentiment_data)
        
        @self.app.route('/api/collaboration')
        def get_collaboration_data():
            """Obtiene datos específicos de análisis de colaboración."""
            if not self.analysis_results:
                return jsonify({'error': 'No data available'})
            
            collaboration_data = self.analysis_results.get('collaboration_analysis', {})
            return jsonify(collaboration_data)
        
        @self.app.route('/api/recommendations')
        def get_recommendations():
            """Obtiene recomendaciones para el equipo."""
            if not self.analysis_results:
                return jsonify({'error': 'No data available'})
            
            recommendations = self.analysis_results.get('recommendations', [])
            return jsonify(recommendations)
    
    def show(self, analysis_results: Dict[str, Any], auto_open: bool = True):
        """
        Muestra el dashboard con los resultados del análisis.
        
        Args:
            analysis_results: Resultados del análisis de Empathy
            auto_open: Si abrir automáticamente el navegador
        """
        self.analysis_results = analysis_results
        
        logger.info(f"🌐 Iniciando dashboard en http://{self.host}:{self.port}")
        
        # Abrir navegador automáticamente si se solicita
        if auto_open:
            def open_browser():
                time.sleep(1.5)  # Esperar a que el servidor arranque
                webbrowser.open(f'http://{self.host}:{self.port}')
            
            threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            self.app.run(host=self.host, port=self.port, debug=self.debug)
        except KeyboardInterrupt:
            logger.info("🛑 Dashboard detenido por el usuario")
        except Exception as e:
            logger.error(f"❌ Error ejecutando dashboard: {e}")
    
    def export_static_report(self, output_path: str) -> bool:
        """
        Exporta un reporte estático HTML.
        
        Args:
            output_path: Ruta donde guardar el reporte
            
        Returns:
            True si se exportó exitosamente
        """
        try:
            # Generar HTML estático con los datos embebidos
            html_content = self._generate_static_html()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"📄 Reporte estático exportado a: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error exportando reporte: {e}")
            return False
    
    def _generate_static_html(self) -> str:
        """Genera HTML estático con datos embebidos."""
        # Template básico para reporte estático
        template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto Empathy - Reporte de Salud del Equipo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .health-score {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            padding: 20px;
        }
        .excellent { color: #27ae60; }
        .good { color: #2ecc71; }
        .fair { color: #f39c12; }
        .poor { color: #e74c3c; }
        .critical { color: #c0392b; }
        .recommendations {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
        }
        .silos-warning {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 20px;
            margin: 20px 0;
        }
        .member-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        .member-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #007bff;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤝 Proyecto Empathy</h1>
        <h2>Reporte de Salud del Equipo</h2>
        <p>Generado el: {timestamp}</p>
    </div>
    
    {content}
    
    <footer style="text-align: center; margin-top: 50px; color: #666;">
        <p>Generado por Proyecto Empathy - El smartwatch para la salud de tu equipo</p>
    </footer>
</body>
</html>
        """
        
        # Generar contenido del reporte
        content = self._generate_report_content()
        
        # Obtener timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        return template.format(content=content, timestamp=timestamp)
    
    def _generate_report_content(self) -> str:
        """Genera el contenido del reporte."""
        if not self.analysis_results:
            return "<p>No hay datos disponibles para generar el reporte.</p>"
        
        summary = self.analysis_results.get('summary', {})
        sentiment_analysis = self.analysis_results.get('sentiment_analysis', {})
        collaboration_analysis = self.analysis_results.get('collaboration_analysis', {})
        recommendations = self.analysis_results.get('recommendations', [])
        
        content_parts = []
        
        # Métricas generales
        content_parts.append(self._generate_summary_section(summary))
        
        # Análisis de sentimientos
        content_parts.append(self._generate_sentiment_section(sentiment_analysis))
        
        # Análisis de colaboración
        content_parts.append(self._generate_collaboration_section(collaboration_analysis))
        
        # Recomendaciones
        content_parts.append(self._generate_recommendations_section(recommendations))
        
        return '\n'.join(content_parts)
    
    def _generate_summary_section(self, summary: Dict[str, Any]) -> str:
        """Genera la sección de resumen."""
        if not summary:
            return ""
        
        health_status = summary.get('health_status', '😐 Regular')
        overall_health = summary.get('overall_team_health', 0.0)
        
        # Determinar clase CSS basada en el score
        if overall_health >= 0.8:
            css_class = 'excellent'
        elif overall_health >= 0.6:
            css_class = 'good'
        elif overall_health >= 0.4:
            css_class = 'fair'
        else:
            css_class = 'poor'
        
        return f"""
        <div class="metric-card">
            <h2>📊 Resumen Ejecutivo</h2>
            <div class="health-score {css_class}">
                {health_status}
            </div>
            <div class="metric-grid">
                <div class="metric-card">
                    <h3>💬 Comunicación</h3>
                    <p><strong>{summary.get('communication_health', 0.0):.2f}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>🤝 Colaboración</h3>
                    <p><strong>{summary.get('collaboration_health', 0.0):.2f}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>🧠 Distribución de Conocimiento</h3>
                    <p><strong>{summary.get('knowledge_distribution', 0.0):.2f}</strong></p>
                </div>
            </div>
        </div>
        """
    
    def _generate_sentiment_section(self, sentiment_analysis: Dict[str, Any]) -> str:
        """Genera la sección de análisis de sentimientos."""
        if not sentiment_analysis:
            return ""
        
        overall_metrics = sentiment_analysis.get('overall_metrics', {})
        
        return f"""
        <div class="metric-card">
            <h2>💭 Análisis de Sentimientos</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <h3>😊 Sentimientos Positivos</h3>
                    <p><strong>{overall_metrics.get('positive_ratio', 0.0):.1%}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>😕 Sentimientos Negativos</h3>
                    <p><strong>{overall_metrics.get('negative_ratio', 0.0):.1%}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>😐 Sentimientos Neutrales</h3>
                    <p><strong>{overall_metrics.get('neutral_ratio', 0.0):.1%}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>🎯 Confianza Promedio</h3>
                    <p><strong>{overall_metrics.get('average_confidence', 0.0):.2f}</strong></p>
                </div>
            </div>
        </div>
        """
    
    def _generate_collaboration_section(self, collaboration_analysis: Dict[str, Any]) -> str:
        """Genera la sección de análisis de colaboración."""
        if not collaboration_analysis:
            return ""
        
        team_metrics = collaboration_analysis.get('team_health_metrics', {})
        silos = collaboration_analysis.get('knowledge_silos', [])
        network = collaboration_analysis.get('collaboration_network', {})
        
        content = f"""
        <div class="metric-card">
            <h2>🤝 Análisis de Colaboración</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <h3>👥 Tamaño del Equipo</h3>
                    <p><strong>{team_metrics.get('team_size', 0)}</strong> miembros</p>
                </div>
                <div class="metric-card">
                    <h3>⚡ Contributors Activos</h3>
                    <p><strong>{team_metrics.get('active_contributors', 0)}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>🔍 Participación en Reviews</h3>
                    <p><strong>{team_metrics.get('review_participation_rate', 0.0):.1%}</strong></p>
                </div>
                <div class="metric-card">
                    <h3>🌐 Densidad de Red</h3>
                    <p><strong>{network.get('network_density', 0.0):.2f}</strong></p>
                </div>
            </div>
        </div>
        """
        
        # Agregar advertencias sobre silos si existen
        if silos:
            silos_html = "<ul>"
            for silo in silos[:5]:  # Mostrar máximo 5 silos
                silos_html += f"<li><strong>{silo.primary_owner}</strong>: {len(silo.files)} archivos ({silo.ownership_percentage:.1%} ownership)</li>"
            silos_html += "</ul>"
            
            content += f"""
            <div class="silos-warning">
                <h3>🚨 Silos de Conocimiento Detectados</h3>
                <p>Se detectaron {len(silos)} silos de conocimiento que podrían representar riesgos:</p>
                {silos_html}
            </div>
            """
        
        return content
    
    def _generate_recommendations_section(self, recommendations: list) -> str:
        """Genera la sección de recomendaciones."""
        if not recommendations:
            return ""
        
        recs_html = "<ul>"
        for rec in recommendations:
            recs_html += f"<li>{rec.get('message', '')}</li>"
        recs_html += "</ul>"
        
        return f"""
        <div class="recommendations">
            <h2>💡 Recomendaciones</h2>
            <p>Basado en el análisis, estas son las recomendaciones para mejorar la salud del equipo:</p>
            {recs_html}
        </div>
        """