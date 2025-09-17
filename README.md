# 🤝 Empathy - Team Health Analyzer

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/xk0dex/empathy/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-audited-brightgreen.svg)](#security)

> **El smartwatch para la salud de tu equipo de desarrollo**

Empathy es un sistema de análisis de dinámicas de equipo que proporciona insights sobre la salud de la colaboración en equipos de desarrollo de software mediante NLP y análisis de datos.

![Empathy Demo](https://via.placeholder.com/800x400/2E8B57/FFFFFF?text=Empathy+Dashboard+Demo)

## 🌟 Características Principales

- 🧠 **Análisis de Sentimientos con NLP** - Evalúa el tono de comunicación en commits y PRs
- 🔍 **Detección de Silos de Conocimiento** - Identifica concentración de expertise
- 🤝 **Métricas de Colaboración** - Mide participación en reviews e interacciones
- 📊 **Dashboard Web Interactivo** - Visualización en tiempo real para demos
- 🎯 **Sistema de Recomendaciones** - Sugerencias automáticas para mejorar team health
- 📈 **Team Health Score** - Métrica integral de salud del equipo (0.0-1.0)
- 🔄 **Integración con GitHub** - Conecta directamente con repositorios

## 🚀 Demo Rápido

```bash
# Clonar repositorio
git clone https://github.com/xk0dex/empathy.git
cd empathy

# Instalación automática
chmod +x setup.sh
./setup.sh

# Demo básico
python demo.py

# Demo web interactivo
python demo.py --web
```

## 📊 Ejemplo de Resultados

```
🤝 REPORTE DE EMPATHY - TEAM HEALTH
================================================

📊 MÉTRICAS GENERALES:
   Salud General del Equipo: 😊 Buena (0.73)
   Comunicación: 0.65
   Colaboración: 0.85
   Distribución de Conocimiento: 0.70

💭 ANÁLISIS DE SENTIMIENTOS:
   Sentimientos Positivos: 62.4%
   Sentimientos Negativos: 8.2%
   Sentimientos Neutrales: 29.4%

👥 MÉTRICAS DEL EQUIPO:
   Tamaño del Equipo: 6 miembros
   Contributors Activos: 6
   Participación en Reviews: 94.2%

💡 RECOMENDACIONES:
   ✅ Excelente colaboración general
   💬 Considera fomentar más feedback positivo
   🔄 Implementar rotación de conocimiento en auth module
```

## 🛠️ Instalación

### Opción 1: Script Automático (Recomendado)
```bash
git clone https://github.com/xk0dex/empathy.git
cd empathy
chmod +x setup.sh
./setup.sh
```

### Opción 2: Manual
```bash
git clone https://github.com/xk0dex/empathy.git
cd empathy

# Crear entorno virtual
python -m venv empathy_env
source empathy_env/bin/activate  # Linux/Mac
# empathy_env\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp config/config.example.env config/.env
# Editar config/.env con tu GitHub token
```

## ⚙️ Configuración

1. **Obtener GitHub Token:**
   - Ve a [GitHub Settings > Tokens](https://github.com/settings/tokens)
   - Genera un token con permisos: `repo`, `read:user`, `read:org`

2. **Configurar variables:**
   ```bash
   cp config/config.example.env config/.env
   ```
   
3. **Editar config/.env:**
   ```env
   GITHUB_TOKEN=ghp_tu_token_aqui
   GITHUB_REPO=usuario/repositorio
   ```

## 🎯 Uso

### Análisis Básico
```bash
python demo.py                    # Demo con datos simulados
python demo.py --version          # Información de versión
python demo.py --help            # Ayuda completa
```

### Dashboard Web
```bash
python demo.py --web             # Lanza dashboard en localhost:8080
```

### Análisis de Repositorio Real
```python
from src.main import EmpathyAnalyzer

config = {
    'github': {
        'token': 'tu_token_aqui',
        'repo': 'usuario/repositorio'
    }
}

analyzer = EmpathyAnalyzer(config)
results = analyzer.analyze()
print(f"Team Health Score: {results['summary']['team_health_score']}")
```

## 📁 Estructura del Proyecto

```
empathy/
├── src/                          # Código fuente principal
│   ├── analysis/                 # Módulos de análisis
│   │   ├── sentiment_analyzer.py # Análisis de sentimientos
│   │   └── collaboration_analyzer.py # Análisis de colaboración
│   ├── data_collection/          # Recopilación de datos
│   │   └── github_collector.py   # Connector GitHub API
│   ├── visualization/            # Dashboard web
│   │   └── dashboard.py          # Flask dashboard
│   └── config/                   # Configuración
├── presentation/                 # Material de presentación
├── docs/                         # Documentación
├── tests/                        # Tests unitarios
├── demo.py                       # Script de demostración
├── setup.sh                      # Instalación automática
└── requirements.txt              # Dependencias Python
```

## 🧪 Tests

```bash
# Ejecutar tests
python -m pytest tests/

# Con coverage
python -m pytest tests/ --cov=src --cov-report=html

# Verificar sistema
python verify.py
```

## 📈 Métricas Disponibles

| Métrica | Descripción | Rango |
|---------|-------------|-------|
| **Team Health Score** | Puntuación integral de salud | 0.0 - 1.0 |
| **Sentiment Score** | Análisis de tono comunicacional | -1.0 - 1.0 |
| **Collaboration Score** | Nivel de colaboración del equipo | 0.0 - 1.0 |
| **Knowledge Distribution** | Distribución de conocimiento | 0.0 - 1.0 |
| **Review Participation** | Participación en code reviews | 0.0 - 1.0 |

## 🛡️ Seguridad

- ✅ **Código auditado** con Safety y Bandit
- ✅ **Sin vulnerabilidades conocidas**
- ✅ **Gestión segura de secretos**
- ✅ **Validación de entradas**
- ✅ **Sin credenciales hardcodeadas**

## 🤝 Contribuir

1. Fork el proyecto
2. Crea un branch para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🎤 Presentaciones

En la carpeta `presentation/` encontrarás material completo para presentar Empathy:

- **PITCH_DECK.md** - Presentación ejecutiva
- **DEMO_SCRIPT.md** - Script técnico para demos
- **ONE_PAGER.md** - Resumen ejecutivo
- **ESTRATEGIAS_PRESENTACION.md** - 5 enfoques diferentes

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/xk0dex/empathy/issues)
- 📧 **Email**: empathy@team.dev
- 📖 **Docs**: [Documentación completa](docs/)

## 🏆 Reconocimientos

Empathy utiliza las siguientes tecnologías:

- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) para análisis de sentimientos
- [PyGithub](https://pygithub.readthedocs.io/) para integración con GitHub
- [Flask](https://flask.palletsprojects.com/) para el dashboard web
- [scikit-learn](https://scikit-learn.org/) para análisis de datos

---

<div align="center">

**¿Te gusta Empathy? ¡Dale una ⭐ y compártelo!**

[Reportar Bug](https://github.com/xk0dex/empathy/issues) • [Solicitar Feature](https://github.com/xk0dex/empathy/issues) • [Contribuir](CONTRIBUTING.md)

</div>