#!/bin/bash

# Script de configuración inicial para Proyecto Empathy
# Este script configura el entorno de desarrollo

echo "🤝 Configurando Proyecto Empathy..."
echo "=================================="

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Descargar recursos de NLTK
echo "🧠 Descargando recursos de NLP..."
python3 -c "
import nltk
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    print('✅ Recursos de NLTK descargados')
except Exception as e:
    print(f'⚠️  Error descargando recursos de NLTK: {e}')
"

# Copiar archivo de configuración de ejemplo
if [ ! -f "config/.env" ]; then
    echo "⚙️  Configurando archivo de entorno..."
    cp config/config.example.env config/.env
    echo "✅ Archivo .env creado desde ejemplo"
    echo ""
    echo "🔑 IMPORTANTE: Debes configurar tu token de GitHub en config/.env"
    echo "   1. Ve a https://github.com/settings/tokens"
    echo "   2. Genera un nuevo token con permisos: repo, read:user, read:org"
    echo "   3. Edita config/.env y reemplaza 'ghp_tu_token_aqui' con tu token real"
    echo ""
else
    echo "⚙️  Archivo .env ya existe"
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p reports
mkdir -p exports
mkdir -p logs

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Edita config/.env con tu token de GitHub"
echo "   2. Activa el entorno virtual: source venv/bin/activate"
echo "   3. Ejecuta un análisis: python src/main.py --repo usuario/repositorio"
echo ""
echo "💡 Ejemplo de uso:"
echo "   python src/main.py --repo microsoft/vscode --days 7 --web"
echo ""
echo "📚 Para más información, consulta el README.md"