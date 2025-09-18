# ⚙️ Configurabilidad Avanzada - Empathy Enterprise

## ✅ **SISTEMA COMPLETO DE CONFIGURACIÓN IMPLEMENTADO**

Empathy incluye un **sistema completo de configuración avanzada** con thresholds personalizables, alertas automáticas y API REST para gestión empresarial.

## 🎯 **Configuración por Equipos**

### **📝 Archivo de Configuración YAML**
```yaml
# config/thresholds.yaml
teams:
  - team_id: "frontend-team"
    team_name: "Frontend Squad"
    enabled: true
    thresholds:
      - metric_name: "team_health_score"
        operator: "lt"  # less than
        value: 0.7
        alert_level: "warning"
        message: "Team health below acceptable threshold"
        cooldown_hours: 24
        
      - metric_name: "sentiment_score"
        operator: "lt"
        value: -0.3
        alert_level: "critical"
        message: "Critical: Negative sentiment detected"
        cooldown_hours: 12
        
    alert_channels:
      - type: "email"
        config:
          recipients: ["lead@company.com", "manager@company.com"]
          smtp_server: "smtp.company.com"
        enabled: true
        
      - type: "slack"
        config:
          webhook_url: "https://hooks.slack.com/services/..."
          channel: "#team-health"
        enabled: true
```

### **🔧 Thresholds Configurables**
```python
# Métricas monitoreables:
✅ team_health_score (0.0 - 1.0)
✅ sentiment_score (-1.0 - 1.0)  
✅ collaboration_score (0.0 - 1.0)
✅ activity_score (0.0 - 1.0)
✅ commit_frequency (commits/day)
✅ review_participation (0.0 - 1.0)
✅ knowledge_distribution (entropy)

# Operadores disponibles:
✅ Greater than (gt)
✅ Less than (lt) 
✅ Greater or equal (gte)
✅ Less or equal (lte)
✅ Equals (eq)
✅ Not equals (ne)
```

## 🚨 **Sistema de Alertas Multi-Canal**

### **📧 Email Notifications**
```python
# Configuración SMTP empresarial
email_config = {
    "recipients": ["team-lead@company.com"],
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "username": "alerts@company.com", 
    "password": "app_password",
    "use_tls": True
}
```

### **💬 Slack Integration**
```python
# Webhook de Slack para notificaciones
slack_config = {
    "webhook_url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    "channel": "#team-health",
    "username": "EmpathyBot",
    "icon_emoji": ":health_worker:"
}
```

### **🌐 Webhook Genérico**
```python
# Para sistemas custom (Microsoft Teams, Discord, etc.)
webhook_config = {
    "url": "https://company.com/api/alerts",
    "method": "POST",
    "headers": {"Authorization": "Bearer token"},
    "payload_template": {
        "alert_level": "{alert_level}",
        "metric": "{metric_name}",
        "value": "{current_value}",
        "threshold": "{threshold_value}",
        "team": "{team_name}"
    }
}
```

## 🎛️ **REST API para Configuración**

### **📊 Gestión de Equipos**
```bash
# Obtener todos los equipos
GET /api/teams

# Configuración específica de equipo  
GET /api/teams/frontend-team/configuration

# Actualizar configuración
PUT /api/teams/frontend-team/configuration
{
    "thresholds": [...],
    "alert_channels": [...]
}

# Crear nuevo equipo
POST /api/teams
{
    "team_id": "backend-team",
    "team_name": "Backend Squad", 
    "enabled": true
}
```

### **⚡ Gestión de Alertas**
```bash
# Ver alertas activas
GET /api/teams/frontend-team/alerts

# Marcar alerta como confirmada
POST /api/teams/frontend-team/alerts/alert-123/acknowledge

# Resolver alerta  
POST /api/teams/frontend-team/alerts/alert-123/resolve

# Probar thresholds contra datos actuales
POST /api/teams/frontend-team/test-thresholds
```

### **📈 Configuración de Métricas**
```bash
# Ver métricas disponibles
GET /api/metric-definitions

# Configurar pesos personalizados
PUT /api/teams/frontend-team/metric-weights
{
    "sentiment_weight": 0.3,
    "collaboration_weight": 0.4, 
    "activity_weight": 0.3
}

# Activar/desactivar módulos
PUT /api/teams/frontend-team/modules
{
    "sentiment_analysis": true,
    "knowledge_silo_detection": true,
    "trend_analysis": false
}
```

## 🎨 **Dashboard de Configuración**

### **Web UI para Configuración**
```bash
# Interfaz web completa disponible en:
python3 demo.py --web
# → http://localhost:8080/config

# Funcionalidades:
✅ Configurar thresholds con sliders
✅ Probar alertas en tiempo real
✅ Visualizar alertas históricas
✅ Gestionar canales de notificación
✅ Importar/exportar configuraciones
```

### **Configuración Visual**
```javascript
// Ejemplo de configuración visual en dashboard:
{
    "Team Health Score": {
        "current": 0.85,
        "threshold": 0.70,
        "status": "healthy",
        "trend": "+5.2%"
    },
    "Sentiment Score": {
        "current": -0.15,
        "threshold": -0.30,
        "status": "warning", 
        "trend": "-12.1%"
    }
}
```

## 🔧 **Casos de Uso Empresariales**

### **Startup (5-15 personas)**
```yaml
# Configuración simple y efectiva
thresholds:
  - metric: team_health_score
    value: 0.6
    alert: warning
    channel: slack
    
  - metric: sentiment_score  
    value: -0.4
    alert: critical
    channel: email
```

### **Empresa Mediana (50-200 personas)**
```yaml
# Múltiples equipos, alertas granulares
teams:
  - frontend-team:
      thresholds: [...] 
      channels: [slack, email]
  - backend-team:
      thresholds: [...]
      channels: [slack, webhook]
  - devops-team:
      thresholds: [...]
      channels: [pagerduty, email]
```

### **Enterprise (500+ personas)**
```yaml
# Configuración avanzada con integrations
teams:
  - team_alpha:
      custom_metrics: true
      escalation_rules: 
        - level_1: slack
        - level_2: email_manager  
        - level_3: pagerduty
      sla_monitoring: true
      compliance_reporting: true
```

## 📊 **Ejemplos de Alertas Reales**

### **Warning Alerts**
```json
{
    "alert_level": "warning",
    "metric": "team_health_score", 
    "current_value": 0.68,
    "threshold": 0.70,
    "message": "Team health slightly below target",
    "recommendations": [
        "Schedule team building activity",
        "Review recent workload distribution",
        "Check for individual stress indicators"
    ]
}
```

### **Critical Alerts**  
```json
{
    "alert_level": "critical",
    "metric": "sentiment_score",
    "current_value": -0.45,
    "threshold": -0.30, 
    "message": "CRITICAL: Significant negative sentiment detected",
    "immediate_actions": [
        "Schedule emergency team meeting",
        "Conduct individual 1:1s",
        "Review recent changes/stressors",
        "Consider workload adjustment"
    ]
}
```

## 🚀 **Demo de Configuración**

### **Setup Básico (2 minutos)**
```bash
# 1. Configurar threshold básico
python3 -c "
from src.monitoring.threshold_manager import ThresholdManager, Threshold
from src.monitoring.threshold_manager import MetricOperator, AlertLevel

tm = ThresholdManager()
threshold = Threshold(
    metric_name='team_health_score',
    operator=MetricOperator.LESS_THAN,
    value=0.7,
    alert_level=AlertLevel.WARNING,
    message='Team health needs attention'
)
print('✅ Threshold configurado:', threshold)
"

# 2. Probar API
curl -X GET http://localhost:5001/api/teams

# 3. Ver dashboard de configuración
python3 demo.py --web
# → http://localhost:8080/config
```

### **Configuración Avanzada (5 minutos)**
```python
# Script completo de configuración empresarial
from src.monitoring.threshold_manager import ThresholdManager
from src.monitoring.config_api import app

# Crear equipo con configuración completa
team_config = {
    "team_id": "my-team",
    "team_name": "My Development Team",
    "thresholds": [
        {
            "metric_name": "team_health_score",
            "operator": "lt",
            "value": 0.7,
            "alert_level": "warning"
        }
    ],
    "alert_channels": [
        {
            "type": "slack",
            "config": {"webhook_url": "https://..."}
        }
    ]
}

# Aplicar configuración vía API
response = requests.post('http://localhost:5001/api/teams', json=team_config)
print('✅ Equipo configurado:', response.json())
```

## 🎯 **Beneficios Empresariales**

### **Para CTOs/VPs Engineering**
- ✅ **Configuración centralizada** para múltiples equipos
- ✅ **Alertas proactivas** antes de que los problemas escalen
- ✅ **Dashboards ejecutivos** con métricas configurables
- ✅ **Compliance reporting** automático

### **Para Engineering Managers**
- ✅ **Thresholds personalizados** por equipo y contexto
- ✅ **Notificaciones inteligentes** sin spam
- ✅ **Escalation automática** basada en severidad
- ✅ **Historical tracking** de alertas y resoluciones

### **Para DevOps Teams**
- ✅ **API REST completa** para integración con herramientas existentes
- ✅ **Webhook support** para sistemas custom  
- ✅ **Configuración como código** (YAML)
- ✅ **Monitoring de monitoreo** (meta-alerts)

---

## 📝 **Configuración Paso a Paso**

### **1. Archivo de Configuración**
```bash
# Editar config/thresholds.yaml
# Agregar tu equipo y thresholds
```

### **2. Configurar Canales de Alerta**
```bash
# Slack: Crear webhook en Slack admin
# Email: Configurar SMTP credentials
# Webhook: Setup endpoint en tu sistema
```

### **3. Probar Configuración**
```bash
# API test
curl -X POST http://localhost:5001/api/teams/tu-equipo/test-thresholds

# Demo con alertas
python3 demo.py --enable-alerts
```

### **4. Monitorear y Ajustar**
```bash
# Ver alertas en dashboard
http://localhost:8080/alerts

# Ajustar thresholds basado en falsos positivos
# Configurar cooldowns apropiados
```

**Empathy ofrece configurabilidad de nivel empresarial desde el día 1.** ⚙️