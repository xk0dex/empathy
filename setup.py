#!/usr/bin/env python3
"""
Setup script para Proyecto Empathy
Sistema de análisis de salud de equipos de desarrollo
"""

from setuptools import setup, find_packages
import os

# Leer versión desde archivo
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'src', '__version__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Buscar __version__ sin ejecutar código
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('__version__') and '=' in line:
                    version_part = line.split('=', 1)[1].strip()
                    # Remover comillas y espacios
                    return version_part.strip("'\"")
    return '1.0.0'

# Leer README para descripción larga
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Leer requirements
def get_requirements():
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        with open(req_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    return []

setup(
    name='empathy-analyzer',
    version=get_version(),
    description='Sistema de análisis de salud de equipos de desarrollo mediante NLP y análisis de colaboración',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='xk0dex',
    author_email='xk0dex@github.com',
    url='https://github.com/xk0dex/empathy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Communications',
    ],
    keywords='team-health nlp sentiment-analysis collaboration git-analysis',
    entry_points={
        'console_scripts': [
            'empathy=src.cli:main',
            'empathy-demo=demo:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/xk0dex/empathy/issues',
        'Documentation': 'https://github.com/xk0dex/empathy#readme',
        'Source': 'https://github.com/xk0dex/empathy',
        'Creator GitHub': 'https://github.com/xk0dex',
    },
    zip_safe=False,
)