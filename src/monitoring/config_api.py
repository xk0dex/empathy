"""
Configuration management API for thresholds and alerts.
Provides REST endpoints for managing team configurations from the dashboard.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from typing import Dict, Any, List
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from monitoring.threshold_manager import ThresholdManager, Threshold, AlertChannel, MetricOperator, AlertLevel

app = Flask(__name__)
CORS(app)

# Initialize threshold manager
threshold_manager = ThresholdManager()

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get list of all teams."""
    teams = []
    for team_id, team_config in threshold_manager.teams.items():
        teams.append({
            'team_id': team_config.team_id,
            'team_name': team_config.team_name,
            'enabled': team_config.enabled,
            'threshold_count': len(team_config.thresholds),
            'channel_count': len(team_config.alert_channels)
        })
    
    return jsonify({'teams': teams})

@app.route('/api/teams/<team_id>/configuration', methods=['GET'])
def get_team_configuration(team_id: str):
    """Get detailed configuration for a specific team."""
    if team_id not in threshold_manager.teams:
        return jsonify({'error': 'Team not found'}), 404
    
    team_config = threshold_manager.teams[team_id]
    
    # Convert to serializable format
    config_data = {
        'team_id': team_config.team_id,
        'team_name': team_config.team_name,
        'enabled': team_config.enabled,
        'created_at': team_config.created_at,
        'updated_at': team_config.updated_at,
        'metric_weights': team_config.metric_weights,
        'thresholds': [
            {
                'metric_name': t.metric_name,
                'operator': t.operator.value,
                'value': t.value,
                'alert_level': t.alert_level.value,
                'message': t.message,
                'enabled': t.enabled,
                'cooldown_hours': t.cooldown_hours
            }
            for t in team_config.thresholds
        ],
        'alert_channels': [
            {
                'type': c.type,
                'enabled': c.enabled,
                'config': {k: '***' if 'password' in k.lower() or 'token' in k.lower() else v 
                          for k, v in c.config.items()}  # Hide sensitive data
            }
            for c in team_config.alert_channels
        ]
    }
    
    return jsonify(config_data)

@app.route('/api/teams/<team_id>/configuration', methods=['PUT'])
def update_team_configuration(team_id: str):
    """Update team configuration."""
    try:
        data = request.get_json()
        
        # Parse thresholds
        thresholds = []
        for t_data in data.get('thresholds', []):
            threshold = Threshold(
                metric_name=t_data['metric_name'],
                operator=MetricOperator(t_data['operator']),
                value=float(t_data['value']),
                alert_level=AlertLevel(t_data['alert_level']),
                message=t_data['message'],
                enabled=t_data.get('enabled', True),
                cooldown_hours=int(t_data.get('cooldown_hours', 24))
            )
            thresholds.append(threshold)
        
        # Parse alert channels
        channels = []
        for c_data in data.get('alert_channels', []):
            channel = AlertChannel(
                type=c_data['type'],
                config=c_data['config'],
                enabled=c_data.get('enabled', True)
            )
            channels.append(channel)
        
        # Update configuration
        updates = {
            'thresholds': thresholds,
            'alert_channels': channels,
            'metric_weights': data.get('metric_weights', {}),
            'enabled': data.get('enabled', True)
        }
        
        updated_config = threshold_manager.update_team_configuration(team_id, **updates)
        
        if updated_config:
            return jsonify({'success': True, 'message': 'Configuration updated successfully'})
        else:
            return jsonify({'error': 'Team not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Error updating configuration: {str(e)}'}), 400

@app.route('/api/teams', methods=['POST'])
def create_team():
    """Create a new team configuration."""
    try:
        data = request.get_json()
        team_id = data.get('team_id')
        team_name = data.get('team_name')
        
        if not team_id or not team_name:
            return jsonify({'error': 'team_id and team_name are required'}), 400
        
        if team_id in threshold_manager.teams:
            return jsonify({'error': 'Team already exists'}), 400
        
        team_config = threshold_manager.create_team_configuration(team_id, team_name)
        
        return jsonify({
            'success': True, 
            'message': 'Team created successfully',
            'team_id': team_config.team_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error creating team: {str(e)}'}), 400

@app.route('/api/teams/<team_id>/alerts', methods=['GET'])
def get_team_alerts(team_id: str):
    """Get alerts for a specific team."""
    dashboard_data = threshold_manager.get_alert_dashboard_data(team_id)
    return jsonify(dashboard_data)

@app.route('/api/teams/<team_id>/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(team_id: str, alert_id: str):
    """Acknowledge an alert."""
    success = threshold_manager.acknowledge_alert(alert_id)
    if success:
        return jsonify({'success': True, 'message': 'Alert acknowledged'})
    else:
        return jsonify({'error': 'Alert not found'}), 404

@app.route('/api/teams/<team_id>/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(team_id: str, alert_id: str):
    """Resolve an alert."""
    success = threshold_manager.resolve_alert(alert_id)
    if success:
        return jsonify({'success': True, 'message': 'Alert resolved'})
    else:
        return jsonify({'error': 'Alert not found'}), 404

@app.route('/api/teams/<team_id>/test-thresholds', methods=['POST'])
def test_thresholds(team_id: str):
    """Test current thresholds against provided metrics."""
    try:
        data = request.get_json()
        metrics = data.get('metrics', {})
        
        alerts = threshold_manager.evaluate_metrics(team_id, metrics)
        
        return jsonify({
            'alerts_generated': len(alerts),
            'alerts': [
                {
                    'metric_name': alert.metric_name,
                    'current_value': alert.current_value,
                    'threshold_value': alert.threshold_value,
                    'alert_level': alert.alert_level.value,
                    'message': alert.message
                }
                for alert in alerts
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'Error testing thresholds: {str(e)}'}), 400

@app.route('/api/teams/<team_id>/health-score', methods=['POST'])
def calculate_custom_health_score(team_id: str):
    """Calculate custom team health score with team-specific weights."""
    try:
        data = request.get_json()
        metrics = data.get('metrics', {})
        
        custom_score = threshold_manager.calculate_custom_team_health_score(team_id, metrics)
        
        return jsonify({
            'custom_team_health_score': custom_score,
            'metrics_used': list(metrics.keys())
        })
        
    except Exception as e:
        return jsonify({'error': f'Error calculating health score: {str(e)}'}), 400

@app.route('/api/metric-definitions', methods=['GET'])
def get_metric_definitions():
    """Get available metrics and their definitions."""
    metrics = {
        'team_health_score': {
            'name': 'Salud General del Equipo',
            'description': 'Métrica combinada que incluye comunicación, colaboración y distribución de conocimiento',
            'range': '0.0 - 1.0',
            'higher_is_better': True
        },
        'sentiment_score': {
            'name': 'Puntuación de Sentimiento',
            'description': 'Análisis de sentimiento en commits, PRs y reviews',
            'range': '0.0 - 1.0',
            'higher_is_better': True
        },
        'collaboration_score': {
            'name': 'Puntuación de Colaboración',
            'description': 'Mide interacción entre miembros del equipo',
            'range': '0.0 - 1.0',
            'higher_is_better': True
        },
        'activity_score': {
            'name': 'Puntuación de Actividad',
            'description': 'Nivel de actividad de desarrollo del equipo',
            'range': '0.0 - 1.0',
            'higher_is_better': True
        },
        'commit_count': {
            'name': 'Número de Commits',
            'description': 'Total de commits en el período',
            'range': '0+',
            'higher_is_better': True
        },
        'contributor_count': {
            'name': 'Número de Contribuidores',
            'description': 'Número de personas que contribuyeron',
            'range': '0+',
            'higher_is_better': True
        },
        'knowledge_distribution': {
            'name': 'Distribución de Conocimiento',
            'description': 'Qué tan distribuido está el conocimiento en el equipo',
            'range': '0.0 - 1.0',
            'higher_is_better': True
        }
    }
    
    operators = {
        'gt': 'Mayor que (>)',
        'lt': 'Menor que (<)',
        'gte': 'Mayor o igual que (>=)',
        'lte': 'Menor o igual que (<=)',
        'eq': 'Igual a (=)',
        'ne': 'No igual a (!=)'
    }
    
    alert_levels = {
        'info': 'Información',
        'warning': 'Advertencia',
        'critical': 'Crítico'
    }
    
    return jsonify({
        'metrics': metrics,
        'operators': operators,
        'alert_levels': alert_levels
    })

@app.route('/api/teams/<team_id>/export-config', methods=['GET'])
def export_team_config(team_id: str):
    """Export team configuration as JSON."""
    if team_id not in threshold_manager.teams:
        return jsonify({'error': 'Team not found'}), 404
    
    team_config = threshold_manager.teams[team_id]
    config_dict = threshold_manager._team_config_to_dict(team_config)
    
    return jsonify(config_dict)

@app.route('/api/teams/<team_id>/import-config', methods=['POST'])
def import_team_config(team_id: str):
    """Import team configuration from JSON."""
    try:
        data = request.get_json()
        
        # Validate and parse the configuration
        parsed_config = threshold_manager._parse_team_config(data)
        parsed_config.team_id = team_id  # Ensure correct team ID
        
        threshold_manager.teams[team_id] = parsed_config
        threshold_manager.save_configurations()
        
        return jsonify({'success': True, 'message': 'Configuration imported successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Error importing configuration: {str(e)}'}), 400

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5001)