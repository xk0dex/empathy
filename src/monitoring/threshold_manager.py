"""
Configurable thresholds and alerts system for team health monitoring.
Allows teams to set custom thresholds and receive notifications when metrics cross defined boundaries.
"""

import json
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests  # For Slack notifications

class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class MetricOperator(Enum):
    """Comparison operators for thresholds."""
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    GREATER_EQUAL = "gte"
    LESS_EQUAL = "lte"
    EQUALS = "eq"
    NOT_EQUALS = "ne"

@dataclass
class Threshold:
    """Individual threshold configuration."""
    metric_name: str
    operator: MetricOperator
    value: float
    alert_level: AlertLevel
    message: str
    enabled: bool = True
    cooldown_hours: int = 24  # Minimum hours between same alert

@dataclass
class AlertChannel:
    """Configuration for alert delivery channel."""
    type: str  # 'email', 'slack', 'webhook'
    config: Dict[str, Any]
    enabled: bool = True

@dataclass
class TeamConfiguration:
    """Team-specific configuration for thresholds and alerts."""
    team_id: str
    team_name: str
    thresholds: List[Threshold]
    alert_channels: List[AlertChannel]
    metric_weights: Dict[str, float]  # Custom weights for Team Health Score
    enabled: bool = True
    created_at: str = None
    updated_at: str = None

@dataclass
class Alert:
    """Individual alert instance."""
    id: str
    threshold_id: str
    team_id: str
    metric_name: str
    current_value: float
    threshold_value: float
    alert_level: AlertLevel
    message: str
    triggered_at: str
    resolved_at: Optional[str] = None
    acknowledged: bool = False
    notified_channels: List[str] = None

class ThresholdManager:
    """Manages threshold configurations and evaluations."""
    
    def __init__(self, config_path: str = "config/thresholds.yaml"):
        self.config_path = Path(config_path)
        self.teams: Dict[str, TeamConfiguration] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.load_configurations()
    
    def load_configurations(self) -> None:
        """Load team configurations from file."""
        if not self.config_path.exists():
            self._create_default_config()
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            for team_data in data.get('teams', []):
                team_config = self._parse_team_config(team_data)
                self.teams[team_config.team_id] = team_config
                
        except Exception as e:
            print(f"Error loading threshold configurations: {e}")
            self._create_default_config()
    
    def save_configurations(self) -> None:
        """Save current configurations to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'version': '1.0',
                'teams': [self._team_config_to_dict(team) for team in self.teams.values()]
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                
        except Exception as e:
            print(f"Error saving threshold configurations: {e}")
    
    def create_team_configuration(self, team_id: str, team_name: str) -> TeamConfiguration:
        """Create a new team configuration with default thresholds."""
        default_thresholds = [
            Threshold(
                metric_name="team_health_score",
                operator=MetricOperator.LESS_THAN,
                value=0.4,
                alert_level=AlertLevel.CRITICAL,
                message="🚨 La salud general del equipo está en nivel crítico (< 40%)"
            ),
            Threshold(
                metric_name="team_health_score",
                operator=MetricOperator.LESS_THAN,
                value=0.6,
                alert_level=AlertLevel.WARNING,
                message="⚠️ La salud del equipo necesita atención (< 60%)"
            ),
            Threshold(
                metric_name="sentiment_score",
                operator=MetricOperator.LESS_THAN,
                value=0.3,
                alert_level=AlertLevel.CRITICAL,
                message="😟 El sentimiento del equipo está muy bajo (< 30%)"
            ),
            Threshold(
                metric_name="collaboration_score",
                operator=MetricOperator.LESS_THAN,
                value=0.3,
                alert_level=AlertLevel.WARNING,
                message="👥 La colaboración del equipo está por debajo del mínimo (< 30%)"
            ),
            Threshold(
                metric_name="commit_count",
                operator=MetricOperator.LESS_THAN,
                value=5,
                alert_level=AlertLevel.INFO,
                message="📉 Actividad de commits muy baja esta semana (< 5 commits)"
            ),
            Threshold(
                metric_name="contributor_count",
                operator=MetricOperator.LESS_EQUAL,
                value=1,
                alert_level=AlertLevel.WARNING,
                message="👤 Solo una persona está contribuyendo (riesgo de bus factor)"
            )
        ]
        
        default_channels = [
            AlertChannel(
                type="email",
                config={
                    "recipients": ["team-lead@company.com"],
                    "smtp_server": "smtp.company.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": ""
                },
                enabled=False
            )
        ]
        
        default_weights = {
            "sentiment_score": 0.3,
            "collaboration_score": 0.3,
            "activity_score": 0.2,
            "knowledge_distribution": 0.2
        }
        
        team_config = TeamConfiguration(
            team_id=team_id,
            team_name=team_name,
            thresholds=default_thresholds,
            alert_channels=default_channels,
            metric_weights=default_weights,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self.teams[team_id] = team_config
        self.save_configurations()
        return team_config
    
    def update_team_configuration(self, team_id: str, **updates) -> Optional[TeamConfiguration]:
        """Update an existing team configuration."""
        if team_id not in self.teams:
            return None
        
        team_config = self.teams[team_id]
        
        if 'thresholds' in updates:
            team_config.thresholds = updates['thresholds']
        if 'alert_channels' in updates:
            team_config.alert_channels = updates['alert_channels']
        if 'metric_weights' in updates:
            team_config.metric_weights = updates['metric_weights']
        if 'enabled' in updates:
            team_config.enabled = updates['enabled']
        
        team_config.updated_at = datetime.now().isoformat()
        self.save_configurations()
        return team_config
    
    def evaluate_metrics(self, team_id: str, metrics: Dict[str, float]) -> List[Alert]:
        """Evaluate current metrics against configured thresholds."""
        if team_id not in self.teams:
            return []
        
        team_config = self.teams[team_id]
        if not team_config.enabled:
            return []
        
        new_alerts = []
        
        for threshold in team_config.thresholds:
            if not threshold.enabled:
                continue
            
            metric_value = metrics.get(threshold.metric_name)
            if metric_value is None:
                continue
            
            # Check if threshold is crossed
            if self._is_threshold_crossed(metric_value, threshold):
                # Check cooldown period
                if not self._is_in_cooldown(team_id, threshold.metric_name, threshold.cooldown_hours):
                    alert = Alert(
                        id=f"{team_id}_{threshold.metric_name}_{datetime.now().timestamp()}",
                        threshold_id=f"{threshold.metric_name}_{threshold.operator.value}_{threshold.value}",
                        team_id=team_id,
                        metric_name=threshold.metric_name,
                        current_value=metric_value,
                        threshold_value=threshold.value,
                        alert_level=threshold.alert_level,
                        message=threshold.message,
                        triggered_at=datetime.now().isoformat(),
                        notified_channels=[]
                    )
                    
                    new_alerts.append(alert)
                    self.active_alerts[alert.id] = alert
                    self.alert_history.append(alert)
        
        return new_alerts
    
    def send_alerts(self, alerts: List[Alert]) -> None:
        """Send alerts through configured channels."""
        for alert in alerts:
            team_config = self.teams.get(alert.team_id)
            if not team_config:
                continue
            
            for channel in team_config.alert_channels:
                if not channel.enabled:
                    continue
                
                try:
                    if channel.type == "email":
                        self._send_email_alert(alert, channel.config)
                    elif channel.type == "slack":
                        self._send_slack_alert(alert, channel.config)
                    elif channel.type == "webhook":
                        self._send_webhook_alert(alert, channel.config)
                    
                    alert.notified_channels.append(channel.type)
                    
                except Exception as e:
                    print(f"Error sending alert via {channel.type}: {e}")
    
    def calculate_custom_team_health_score(self, team_id: str, metrics: Dict[str, float]) -> float:
        """Calculate team health score using custom weights."""
        team_config = self.teams.get(team_id)
        if not team_config:
            # Use default weights
            weights = {
                "sentiment_score": 0.3,
                "collaboration_score": 0.3,
                "activity_score": 0.2,
                "knowledge_distribution": 0.2
            }
        else:
            weights = team_config.metric_weights
        
        score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
                total_weight += weight
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark an alert as acknowledged."""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved."""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved_at = datetime.now().isoformat()
            del self.active_alerts[alert_id]
            return True
        return False
    
    def get_alert_dashboard_data(self, team_id: str) -> Dict[str, Any]:
        """Get alert data for dashboard display."""
        team_alerts = [alert for alert in self.active_alerts.values() if alert.team_id == team_id]
        recent_history = [alert for alert in self.alert_history[-50:] if alert.team_id == team_id]
        
        return {
            "active_alerts": [asdict(alert) for alert in team_alerts],
            "recent_history": [asdict(alert) for alert in recent_history],
            "alert_counts": {
                "critical": len([a for a in team_alerts if a.alert_level == AlertLevel.CRITICAL]),
                "warning": len([a for a in team_alerts if a.alert_level == AlertLevel.WARNING]),
                "info": len([a for a in team_alerts if a.alert_level == AlertLevel.INFO])
            }
        }
    
    # Private methods
    def _create_default_config(self) -> None:
        """Create default configuration file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        default_config = {
            'version': '1.0',
            'teams': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False)
    
    def _parse_team_config(self, data: Dict[str, Any]) -> TeamConfiguration:
        """Parse team configuration from dictionary."""
        thresholds = []
        for t_data in data.get('thresholds', []):
            threshold = Threshold(
                metric_name=t_data['metric_name'],
                operator=MetricOperator(t_data['operator']),
                value=t_data['value'],
                alert_level=AlertLevel(t_data['alert_level']),
                message=t_data['message'],
                enabled=t_data.get('enabled', True),
                cooldown_hours=t_data.get('cooldown_hours', 24)
            )
            thresholds.append(threshold)
        
        channels = []
        for c_data in data.get('alert_channels', []):
            channel = AlertChannel(
                type=c_data['type'],
                config=c_data['config'],
                enabled=c_data.get('enabled', True)
            )
            channels.append(channel)
        
        return TeamConfiguration(
            team_id=data['team_id'],
            team_name=data['team_name'],
            thresholds=thresholds,
            alert_channels=channels,
            metric_weights=data.get('metric_weights', {}),
            enabled=data.get('enabled', True),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def _team_config_to_dict(self, team_config: TeamConfiguration) -> Dict[str, Any]:
        """Convert team configuration to dictionary."""
        return {
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
                    'config': c.config,
                    'enabled': c.enabled
                }
                for c in team_config.alert_channels
            ]
        }
    
    def _is_threshold_crossed(self, value: float, threshold: Threshold) -> bool:
        """Check if a metric value crosses the threshold."""
        if threshold.operator == MetricOperator.GREATER_THAN:
            return value > threshold.value
        elif threshold.operator == MetricOperator.LESS_THAN:
            return value < threshold.value
        elif threshold.operator == MetricOperator.GREATER_EQUAL:
            return value >= threshold.value
        elif threshold.operator == MetricOperator.LESS_EQUAL:
            return value <= threshold.value
        elif threshold.operator == MetricOperator.EQUALS:
            return abs(value - threshold.value) < 0.001
        elif threshold.operator == MetricOperator.NOT_EQUALS:
            return abs(value - threshold.value) >= 0.001
        return False
    
    def _is_in_cooldown(self, team_id: str, metric_name: str, cooldown_hours: int) -> bool:
        """Check if metric is in cooldown period."""
        cutoff_time = datetime.now() - timedelta(hours=cooldown_hours)
        
        for alert in self.alert_history:
            if (alert.team_id == team_id and 
                alert.metric_name == metric_name and
                datetime.fromisoformat(alert.triggered_at) > cutoff_time):
                return True
        
        return False
    
    def _send_email_alert(self, alert: Alert, config: Dict[str, Any]) -> None:
        """Send alert via email."""
        msg = MIMEMultipart()
        msg['From'] = config.get('from_email', 'empathy-alerts@company.com')
        msg['To'] = ', '.join(config['recipients'])
        msg['Subject'] = f"[Empathy Alert] {alert.alert_level.value.upper()}: {alert.metric_name}"
        
        body = f"""
        Alerta de Empathy Team Health Monitor
        
        Equipo: {alert.team_id}
        Métrica: {alert.metric_name}
        Valor actual: {alert.current_value:.3f}
        Umbral: {alert.threshold_value}
        Nivel: {alert.alert_level.value.upper()}
        
        Mensaje: {alert.message}
        
        Fecha: {alert.triggered_at}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['username'], config['password'])
        server.send_message(msg)
        server.quit()
    
    def _send_slack_alert(self, alert: Alert, config: Dict[str, Any]) -> None:
        """Send alert via Slack webhook."""
        color_map = {
            AlertLevel.INFO: "#36a64f",
            AlertLevel.WARNING: "#ff9f00", 
            AlertLevel.CRITICAL: "#ff0000"
        }
        
        payload = {
            "text": f"Empathy Alert: {alert.alert_level.value.upper()}",
            "attachments": [
                {
                    "color": color_map.get(alert.alert_level, "#808080"),
                    "fields": [
                        {"title": "Equipo", "value": alert.team_id, "short": True},
                        {"title": "Métrica", "value": alert.metric_name, "short": True},
                        {"title": "Valor Actual", "value": f"{alert.current_value:.3f}", "short": True},
                        {"title": "Umbral", "value": f"{alert.threshold_value}", "short": True},
                        {"title": "Mensaje", "value": alert.message, "short": False}
                    ],
                    "footer": "Empathy Team Health Monitor",
                    "ts": int(datetime.fromisoformat(alert.triggered_at).timestamp())
                }
            ]
        }
        
        response = requests.post(config['webhook_url'], json=payload)
        response.raise_for_status()
    
    def _send_webhook_alert(self, alert: Alert, config: Dict[str, Any]) -> None:
        """Send alert via generic webhook."""
        payload = asdict(alert)
        payload['alert_level'] = alert.alert_level.value
        
        headers = config.get('headers', {'Content-Type': 'application/json'})
        response = requests.post(config['url'], json=payload, headers=headers)
        response.raise_for_status()

# Example usage and testing
if __name__ == "__main__":
    # Initialize threshold manager
    manager = ThresholdManager()
    
    # Create a test team configuration
    team_config = manager.create_team_configuration("team-alpha", "Alpha Development Team")
    print(f"Created team configuration for: {team_config.team_name}")
    
    # Test metrics that would trigger alerts
    test_metrics = {
        "team_health_score": 0.35,  # Should trigger critical alert
        "sentiment_score": 0.25,    # Should trigger critical alert
        "collaboration_score": 0.45, # OK
        "commit_count": 3,          # Should trigger info alert
        "contributor_count": 1      # Should trigger warning alert
    }
    
    # Evaluate thresholds
    alerts = manager.evaluate_metrics("team-alpha", test_metrics)
    print(f"\nGenerated {len(alerts)} alerts:")
    
    for alert in alerts:
        print(f"- {alert.alert_level.value.upper()}: {alert.message}")
        print(f"  Metric: {alert.metric_name} = {alert.current_value} (threshold: {alert.threshold_value})")
    
    # Test custom team health score calculation
    custom_score = manager.calculate_custom_team_health_score("team-alpha", test_metrics)
    print(f"\nCustom team health score: {custom_score:.3f}")
    
    # Get dashboard data
    dashboard_data = manager.get_alert_dashboard_data("team-alpha")
    print(f"\nDashboard data: {dashboard_data['alert_counts']}")