# 📋 Guía de Uso - Proyecto Empathy

## 🎯 Uso Básico

### Análisis Simple

```bash
# Analizar un repositorio público
python src/main.py --repo microsoft/vscode

# Analizar últimos 7 días
python src/main.py --repo facebook/react --days 7

# Abrir dashboard web automáticamente
python src/main.py --repo golang/go --web
```

### Guardar Resultados

```bash
# Exportar a JSON
python src/main.py --repo netflix/zuul --output report.json

# Exportar reporte HTML estático
python demo.py --export report.html
```

## 🧠 Interpretando los Resultados

### Métricas de Salud del Equipo

- **🌟 Excelente (0.8-1.0)**: Equipo muy saludable
- **😊 Bueno (0.6-0.8)**: Funcionamiento sólido
- **😐 Regular (0.4-0.6)**: Necesita atención
- **😕 Pobre (0.2-0.4)**: Problemas significativos
- **🚨 Crítico (0.0-0.2)**: Requiere intervención inmediata

### Análisis de Sentimientos

#### Indicadores Positivos
- Alto porcentaje de sentimientos positivos (>60%)
- Comunicación constructiva en reviews
- Agradecimientos y reconocimientos frecuentes

#### Señales de Alerta
- Sentimientos negativos >30%
- Tono agresivo o frustrante en comentarios
- Falta de comunicación positiva

### Análisis de Colaboración

#### Buenas Señales
- Alta densidad de red de colaboración
- Participación activa en code reviews
- Distribución equilibrada del trabajo

#### Problemas Detectados
- **Silos de Conocimiento**: Una persona domina >80% de ciertos archivos
- **Miembros Aislados**: Sin colaboración con otros
- **Desbalance**: Algunos miembros muy activos, otros pasivos

## 🔧 Configuración Avanzada

### Personalizar Análisis

```python
# config/custom_analysis.py
from src.main import EmpathyAnalyzer

# Configuración personalizada
config = {
    'analysis': {
        'sentiment_model': 'hybrid',  # Usar múltiples modelos
        'language': 'es',             # Análisis en español
        'confidence_threshold': 0.7   # Mayor precisión
    },
    'metrics': {
        'knowledge_silo_threshold': 0.7,  # Más sensible a silos
        'collaboration_threshold': 0.6    # Estándar más alto
    }
}

analyzer = EmpathyAnalyzer(config)
results = analyzer.analyze_repository('mi-org/mi-repo', days_back=14)
```

### Filtros y Opciones

```bash
# Analizar solo commits (sin PRs)
python src/main.py --repo user/repo --commits-only

# Excluir ciertos usuarios
python src/main.py --repo user/repo --exclude-users bot,automation

# Analizar solo ciertos directorios
python src/main.py --repo user/repo --include-paths "src/,tests/"
```

## 📊 Dashboard Web Interactivo

### Funciones del Dashboard

1. **Vista General**: Métricas principales en tiempo real
2. **Análisis de Sentimientos**: Gráficos de distribución emocional
3. **Red de Colaboración**: Visualización de interacciones
4. **Miembros del Equipo**: Perfiles individuales de colaboración
5. **Alertas**: Notificaciones de problemas detectados

### Navegación

- **Actualizar**: Refresca los datos del análisis
- **Exportar**: Descarga reporte en PDF/HTML
- **Filtros**: Personaliza el periodo de análisis
- **Comparar**: Contrasta con análisis anteriores

## 🚨 Alertas y Recomendaciones

### Tipos de Alertas

#### 🔴 Críticas
- Silos de conocimiento con riesgo muy alto
- Sentimientos muy negativos sostenidos
- Miembros completamente aislados

#### 🟡 Advertencias
- Disminución en la colaboración
- Aumento de sentimientos negativos
- Concentración de conocimiento moderada

#### 🟢 Informativas
- Nuevos patrones de colaboración
- Mejoras en la comunicación
- Distribución más equilibrada

### Recomendaciones Típicas

#### Para Mejorar Colaboración
- Implementar pair programming
- Rotar responsabilidades en code reviews
- Organizar sesiones de knowledge sharing

#### Para Mejorar Comunicación
- Establecer guidelines para feedback constructivo
- Promover reconocimiento público
- Entrenar en comunicación efectiva

#### Para Reducir Silos
- Documentar conocimiento crítico
- Cross-training entre miembros
- Distribuir ownership de componentes

## 📈 Casos de Uso Avanzados

### Análisis Periódico

```bash
# Script para análisis semanal
#!/bin/bash
DATE=$(date +%Y-%m-%d)
python src/main.py --repo mi-org/mi-repo \
  --output "reports/weekly_$DATE.json" \
  --days 7
```

### Comparación Temporal

```python
# Comparar salud del equipo entre periodos
analyzer = EmpathyAnalyzer()

# Último mes
current = analyzer.analyze_repository('user/repo', days_back=30)

# Mes anterior
previous = analyzer.analyze_repository('user/repo', days_back=60)

# Comparar tendencias
trend = current['summary']['overall_team_health'] - previous['summary']['overall_team_health']
print(f"Tendencia: {'📈 Mejorando' if trend > 0 else '📉 Empeorando'}")
```

### Múltiples Repositorios

```python
# Analizar varios repos de la organización
repos = ['org/frontend', 'org/backend', 'org/mobile']
results = {}

for repo in repos:
    results[repo] = analyzer.analyze_repository(repo)
    
# Comparar salud entre equipos
for repo, data in results.items():
    health = data['summary']['overall_team_health']
    print(f"{repo}: {health:.2f}")
```

## 🔐 Consideraciones de Privacidad

### Datos Analizados
- Solo metadatos públicos de GitHub
- Contenido de commits y comentarios públicos
- Patrones de actividad temporal

### Datos NO Analizados
- Contenido de código fuente
- Información personal privada
- Repositorios privados sin permisos

### Buenas Prácticas
- Usar tokens con permisos mínimos necesarios
- Revisar resultados antes de compartir
- Respetar políticas de privacidad organizacionales

## 🤝 Integraciones

### CI/CD

```yaml
# .github/workflows/empathy.yml
name: Team Health Check
on:
  schedule:
    - cron: '0 9 * * 1'  # Lunes a las 9 AM

jobs:
  empathy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Empathy Analysis
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python src/main.py --repo ${{ github.repository }} \
            --output empathy-report.json
```

### Slack/Discord

```python
# Enviar alertas a Slack
if results['summary']['overall_team_health'] < 0.5:
    send_slack_alert(f"⚠️ Salud del equipo baja: {health:.2f}")
```

## 📚 Recursos Adicionales

- [API Reference](API.md)
- [Ejemplos Avanzados](examples/)
- [FAQ](FAQ.md)
- [Comunidad Discord](https://discord.gg/empathy)