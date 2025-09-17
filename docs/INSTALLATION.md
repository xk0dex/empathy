# 📖 Guía de Instalación - Proyecto Empathy

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.8 o superior
- Git
- Token de acceso personal de GitHub

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/empathy.git
cd empathy
```

### 2. Ejecutar Script de Configuración

```bash
# En Linux/macOS
./setup.sh

# En Windows
setup.bat
```

### 3. Configurar Token de GitHub

1. Ve a [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Genera un nuevo token con estos permisos:
   - `repo` (acceso completo a repositorios)
   - `read:user` (leer información del usuario)
   - `read:org` (leer información de organizaciones)
3. Edita el archivo `config/.env`:
   ```
   GITHUB_TOKEN=ghp_tu_token_real_aqui
   ```

## 🎯 Instalación Manual

Si prefieres configurar manualmente:

### 1. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows
```

### 2. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar Entorno

```bash
cp config/config.example.env config/.env
# Editar config/.env con tu token de GitHub
```

### 4. Descargar Recursos NLP

```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

## 🧪 Verificar Instalación

### Ejecutar Demo

```bash
python demo.py
```

### Ejecutar Análisis Real

```bash
python src/main.py --repo microsoft/vscode --days 7
```

### Abrir Dashboard Web

```bash
python demo.py --web
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Puedes personalizar el comportamiento editando `config/.env`:

```env
# Configuración de análisis
SENTIMENT_MODEL=vader              # vader, textblob, hybrid
ANALYSIS_LANGUAGE=en               # en, es, auto
CONFIDENCE_THRESHOLD=0.5           # 0.0 - 1.0

# Configuración web
WEB_HOST=127.0.0.1
WEB_PORT=8080
WEB_DEBUG=false

# Configuración de umbrales
COLLABORATION_THRESHOLD=0.5
SENTIMENT_THRESHOLD=0.3
KNOWLEDGE_SILO_THRESHOLD=0.8
```

### Base de Datos

Por defecto, Empathy usa SQLite, pero puedes configurar PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost/empathy
```

## 🚨 Solución de Problemas

### Error: "No module named 'github'"

```bash
pip install PyGithub
```

### Error: "GITHUB_TOKEN requerido"

Verifica que hayas configurado correctamente el token en `config/.env`.

### Error: "Rate limit exceeded"

Aumenta el delay entre llamadas:

```env
GITHUB_RATE_LIMIT_DELAY=2
```

### Error al instalar dependencias

Actualiza pip y setuptools:

```bash
pip install --upgrade pip setuptools wheel
```

## 🐳 Instalación con Docker

```bash
# Construir imagen
docker build -t empathy .

# Ejecutar contenedor
docker run -e GITHUB_TOKEN=tu_token empathy --repo usuario/repo
```

## 🔄 Actualización

Para actualizar a la última versión:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📚 Próximos Pasos

1. Lee la [Guía de Uso](USAGE.md)
2. Consulta los [Ejemplos](examples/)
3. Revisa la [API Reference](API.md)
4. Únete a la [Comunidad](https://discord.gg/empathy)