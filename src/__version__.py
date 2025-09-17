"""
Información de versión para Proyecto Empathy
Creado por: xk0dex
GitHub: https://github.com/xk0dex
"""

__version__ = '1.0.0'
__version_info__ = (1, 0, 0)
__author__ = 'xk0dex'
__author_email__ = 'xk0dex@github.com'
__github__ = 'https://github.com/xk0dex'
__repository__ = 'https://github.com/xk0dex/empathy'

# Información adicional de la versión
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_STATUS = 'stable'  # stable, beta, alpha, rc

# Nombre del release
RELEASE_NAME = 'Genesis'  # Primer release estable

# Fecha de release
RELEASE_DATE = '2025-09-17'

# Autor y créditos
CREATOR = 'xk0dex'
COPYRIGHT = f'© 2025 {CREATOR}. All rights reserved.'
LICENSE = 'MIT License'

# Características principales de esta versión
FEATURES = [
    'Análisis de sentimientos con VADER',
    'Detección de silos de conocimiento',
    'Dashboard web interactivo',
    'Análisis de colaboración',
    'Sistema de recomendaciones',
    'Demo interactivo completo',
    'Material de presentación profesional'
]

# Changelog resumido
CHANGELOG = {
    '1.0.0': {
        'date': '2025-09-17',
        'features': [
            'Sistema completo de análisis de team health',
            'Análisis de sentimientos con NLP',
            'Dashboard web con Flask',
            'Detección automática de knowledge silos',
            'Generación de recomendaciones inteligentes',
            'Kit completo de presentación'
        ],
        'fixes': [],
        'breaking_changes': []
    }
}

def get_version_string():
    """Retorna la versión como string"""
    return __version__

def get_version_info():
    """Retorna información detallada de la versión"""
    return {
        'version': __version__,
        'version_info': __version_info__,
        'release_name': RELEASE_NAME,
        'release_date': RELEASE_DATE,
        'status': VERSION_STATUS,
        'features': FEATURES
    }

def print_version_info():
    """Imprime información de la versión con créditos del autor"""
    info = get_version_info()
    print(f"Empathy Analyzer v{info['version']} '{info['release_name']}'")
    print(f"Created by: {CREATOR}")
    print(f"GitHub: {__github__}")
    print(f"Release Date: {info['release_date']}")
    print(f"Status: {info['status']}")
    print(f"Features: {len(info['features'])} características principales")
    print(f"{COPYRIGHT}")
    
def print_banner():
    """Imprime banner con marca de agua del autor"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🤝 EMPATHY v{__version__}                     ║
║              Team Health Analyzer & Insights                ║
║                                                              ║
║  Created by: {CREATOR:<47} ║
║  GitHub: {__github__:<50} ║
║  License: {LICENSE:<49} ║
║                                                              ║
║  © 2025 {CREATOR}. All rights reserved.                      ║
╚══════════════════════════════════════════════════════════════╝
"""
    return banner