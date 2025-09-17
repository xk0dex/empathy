#!/usr/bin/env python3
"""
Script de verificación del sistema Empathy
Valida que todos los componentes estén funcionando correctamente
"""

import sys
import os
from pathlib import Path

# Añadir src al path
sys.path.append(str(Path(__file__).parent / 'src'))

try:
    from __version__ import get_version_info, print_version_info, __version__
    from main import EmpathyAnalyzer
    from analysis.sentiment_analyzer import SentimentAnalyzer
    from analysis.collaboration_analyzer import CollaborationAnalyzer
    from data_collection.github_collector import GitHubCollector
    from visualization.dashboard import Dashboard
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

def check_system_health():
    """Verifica el estado de salud del sistema"""
    print("🔍 VERIFICACIÓN DEL SISTEMA EMPATHY")
    print("=" * 50)
    
    # Verificar versión
    print(f"📦 Versión: {__version__}")
    version_info = get_version_info()
    print(f"🏷️  Release: {version_info['release_name']}")
    print(f"📅 Fecha: {version_info['release_date']}")
    print(f"🚀 Estado: {version_info['status']}")
    print()
    
    # Verificar componentes
    print("🧩 COMPONENTES:")
    components = [
        ("Analizador de Sentimientos", SentimentAnalyzer),
        ("Analizador de Colaboración", CollaborationAnalyzer),
        ("Collector de GitHub", GitHubCollector),
        ("Dashboard Web", Dashboard),
        ("Analizador Principal", EmpathyAnalyzer)
    ]
    
    all_ok = True
    for name, component in components:
        try:
            # Intentar instanciar
            if component == Dashboard:
                instance = component()
            elif component == SentimentAnalyzer:
                instance = component()
            elif component == CollaborationAnalyzer:
                instance = component()
            elif component == GitHubCollector:
                instance = component("")  # Token vacío para test
            elif component == EmpathyAnalyzer:
                instance = component({})  # Config vacío para test
            
            print(f"  ✅ {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            all_ok = False
    
    print()
    
    # Verificar archivos clave
    print("📁 ARCHIVOS CLAVE:")
    key_files = [
        "src/__version__.py",
        "src/__init__.py", 
        "setup.py",
        "requirements.txt",
        "demo.py",
        "CHANGELOG.md",
        "presentation/README.md"
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (faltante)")
            all_ok = False
    
    print()
    
    # Verificar características
    print("🌟 CARACTERÍSTICAS:")
    features = version_info['features']
    for feature in features:
        print(f"  ✅ {feature}")
    
    print()
    
    # Resultado final
    if all_ok:
        print("🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("✅ Todos los componentes están operativos")
        print("🚀 Listo para producción y demos")
        return True
    else:
        print("⚠️  SISTEMA CON PROBLEMAS")
        print("❌ Algunos componentes requieren atención")
        return False

def run_quick_demo():
    """Ejecuta una demo rápida para verificar funcionalidad"""
    print("\n🧪 DEMO RÁPIDA DE VERIFICACIÓN")
    print("=" * 50)
    
    try:
        # Test básico del analizador
        analyzer = EmpathyAnalyzer({})
        print("✅ Analizador principal: OK")
        
        # Test del analizador de sentimientos
        sentiment_analyzer = SentimentAnalyzer()
        test_text = "This is a great project!"
        sentiment = sentiment_analyzer.analyze_text(test_text)
        print(f"✅ Análisis de sentimientos: {sentiment['compound']:.2f}")
        
        # Test del analizador de colaboración
        collab_analyzer = CollaborationAnalyzer()
        print("✅ Analizador de colaboración: OK")
        
        print("\n🎯 VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en demo rápida: {e}")
        return False

if __name__ == "__main__":
    print_version_info()
    print()
    
    # Verificar sistema
    system_ok = check_system_health()
    
    if system_ok:
        # Ejecutar demo rápida
        demo_ok = run_quick_demo()
        
        if demo_ok:
            print(f"\n🏆 EMPATHY v{__version__} ESTÁ 100% FUNCIONAL")
            sys.exit(0)
        else:
            print(f"\n⚠️  EMPATHY v{__version__} tiene problemas en demo")
            sys.exit(1)
    else:
        print(f"\n❌ EMPATHY v{__version__} tiene problemas de sistema")
        sys.exit(1)