"""
Recopilador de datos de GitHub para el Proyecto Empathy.

Este módulo se conecta a la API de GitHub para obtener información sobre:
- Commits y mensajes de commit
- Pull requests y comentarios
- Issues y discusiones
- Patrones de actividad temporal
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

import requests
from github import Github, GithubException
from github.Repository import Repository

logger = logging.getLogger(__name__)


@dataclass
class CommitData:
    """Estructura de datos para información de commits."""
    sha: str
    author: str
    author_email: str
    message: str
    timestamp: datetime
    files_changed: List[str]
    additions: int
    deletions: int


@dataclass
class PullRequestData:
    """Estructura de datos para información de pull requests."""
    number: int
    title: str
    author: str
    state: str
    created_at: datetime
    merged_at: Optional[datetime]
    comments: List[Dict[str, Any]]
    reviews: List[Dict[str, Any]]
    files_changed: List[str]


class GitHubCollector:
    """
    Recopilador de datos de repositorios de GitHub.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el recopilador con configuración.
        
        Args:
            config: Diccionario de configuración con token de GitHub
        """
        self.config = config
        self.github_token = config['github']['token']
        self.rate_limit_delay = config['github'].get('rate_limit_delay', 1)
        
        # Inicializar cliente de GitHub
        self.github = Github(self.github_token)
        
        # Verificar autenticación
        try:
            user = self.github.get_user()
            logger.info(f"✅ Autenticado como: {user.login}")
        except GithubException as e:
            logger.error(f"❌ Error de autenticación: {e}")
            raise
    
    def collect_repository_data(self, repo_url: str, days_back: int = 30) -> Dict[str, Any]:
        """
        Recopila datos completos de un repositorio.
        
        Args:
            repo_url: URL del repositorio (formato: owner/repo)
            days_back: Días hacia atrás para analizar
            
        Returns:
            Diccionario con todos los datos recopilados
        """
        try:
            # Extraer owner/repo de la URL
            repo_name = self._extract_repo_name(repo_url)
            repo = self.github.get_repo(repo_name)
            
            logger.info(f"📁 Analizando repositorio: {repo.full_name}")
            
            # Calcular fecha límite
            since_date = datetime.now() - timedelta(days=days_back)
            
            # Recopilar datos
            data = {
                'repository_info': self._get_repository_info(repo),
                'commits': self._collect_commits(repo, since_date),
                'pull_requests': self._collect_pull_requests(repo, since_date),
                'contributors': self._collect_contributors(repo),
                'collection_metadata': {
                    'collected_at': datetime.now(),
                    'days_analyzed': days_back,
                    'since_date': since_date
                }
            }
            
            logger.info(f"📊 Datos recopilados: "
                       f"{len(data['commits'])} commits, "
                       f"{len(data['pull_requests'])} PRs, "
                       f"{len(data['contributors'])} contributors")
            
            return data
            
        except GithubException as e:
            logger.error(f"❌ Error accediendo al repositorio: {e}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            return {}
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """
        Extrae el nombre del repositorio de diferentes formatos de URL.
        
        Args:
            repo_url: URL del repositorio
            
        Returns:
            Nombre en formato 'owner/repo'
            
        Raises:
            ValueError: Si el formato de URL es inválido
        """
        if not repo_url or not isinstance(repo_url, str):
            raise ValueError("La URL del repositorio debe ser una cadena no vacía")
        
        repo_url = repo_url.strip()
        
        # Limpiar URL y extraer owner/repo
        if 'github.com/' in repo_url:
            parts = repo_url.split('github.com/')[-1].strip('/').split('/')
            if len(parts) >= 2 and parts[0] and parts[1]:
                # Remover .git si existe
                repo_name = parts[1].replace('.git', '')
                return f"{parts[0]}/{repo_name}"
        
        # Si ya está en formato owner/repo
        if '/' in repo_url and len(repo_url.split('/')) == 2:
            owner, repo = repo_url.split('/')
            if owner.strip() and repo.strip():
                return f"{owner.strip()}/{repo.strip()}"
        
        raise ValueError(f"Formato de URL de repositorio inválido: {repo_url}. "
                        f"Use: 'owner/repo' o 'https://github.com/owner/repo'")
    
    def _get_repository_info(self, repo: Repository) -> Dict[str, Any]:
        """
        Obtiene información general del repositorio.
        """
        return {
            'name': repo.name,
            'full_name': repo.full_name,
            'description': repo.description,
            'language': repo.language,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'created_at': repo.created_at,
            'updated_at': repo.updated_at,
            'default_branch': repo.default_branch
        }
    
    def _collect_commits(self, repo: Repository, since_date: datetime) -> List[CommitData]:
        """
        Recopila información de commits desde una fecha específica.
        """
        commits_data = []
        
        try:
            commits = repo.get_commits(since=since_date)
            
            for commit in commits:
                try:
                    # Información básica del commit
                    commit_data = CommitData(
                        sha=commit.sha,
                        author=commit.author.login if commit.author else 'Unknown',
                        author_email=commit.commit.author.email,
                        message=commit.commit.message,
                        timestamp=commit.commit.author.date,
                        files_changed=[file.filename for file in commit.files],
                        additions=commit.stats.additions,
                        deletions=commit.stats.deletions
                    )
                    
                    commits_data.append(commit_data)
                    
                    # Control de rate limiting
                    time.sleep(self.rate_limit_delay)
                    
                except Exception as e:
                    logger.warning(f"⚠️  Error procesando commit {commit.sha}: {e}")
                    continue
                    
        except GithubException as e:
            logger.error(f"❌ Error obteniendo commits: {e}")
        
        return commits_data
    
    def _collect_pull_requests(self, repo: Repository, since_date: datetime) -> List[PullRequestData]:
        """
        Recopila información de pull requests desde una fecha específica.
        """
        prs_data = []
        
        try:
            # Obtener PRs recientes
            pulls = repo.get_pulls(state='all', sort='updated', direction='desc')
            
            for pr in pulls:
                # Filtrar por fecha
                if pr.updated_at < since_date:
                    break
                
                try:
                    # Recopilar comentarios
                    comments = []
                    for comment in pr.get_issue_comments():
                        comments.append({
                            'author': comment.user.login,
                            'body': comment.body,
                            'created_at': comment.created_at
                        })
                    
                    # Recopilar reviews
                    reviews = []
                    for review in pr.get_reviews():
                        reviews.append({
                            'author': review.user.login,
                            'state': review.state,
                            'body': review.body or '',
                            'submitted_at': review.submitted_at
                        })
                    
                    pr_data = PullRequestData(
                        number=pr.number,
                        title=pr.title,
                        author=pr.user.login,
                        state=pr.state,
                        created_at=pr.created_at,
                        merged_at=pr.merged_at,
                        comments=comments,
                        reviews=reviews,
                        files_changed=[file.filename for file in pr.get_files()]
                    )
                    
                    prs_data.append(pr_data)
                    
                    # Control de rate limiting
                    time.sleep(self.rate_limit_delay)
                    
                except Exception as e:
                    logger.warning(f"⚠️  Error procesando PR #{pr.number}: {e}")
                    continue
                    
        except GithubException as e:
            logger.error(f"❌ Error obteniendo pull requests: {e}")
        
        return prs_data
    
    def _collect_contributors(self, repo: Repository) -> List[Dict[str, Any]]:
        """
        Recopila información de contributors del repositorio.
        """
        contributors_data = []
        
        try:
            contributors = repo.get_contributors()
            
            for contributor in contributors:
                try:
                    contributor_data = {
                        'login': contributor.login,
                        'contributions': contributor.contributions,
                        'type': contributor.type,
                        'avatar_url': contributor.avatar_url
                    }
                    
                    contributors_data.append(contributor_data)
                    
                except Exception as e:
                    logger.warning(f"⚠️  Error procesando contributor: {e}")
                    continue
                    
        except GithubException as e:
            logger.error(f"❌ Error obteniendo contributors: {e}")
        
        return contributors_data
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el rate limit actual.
        """
        try:
            rate_limit = self.github.get_rate_limit()
            return {
                'core': {
                    'limit': rate_limit.core.limit,
                    'remaining': rate_limit.core.remaining,
                    'reset_time': rate_limit.core.reset
                },
                'search': {
                    'limit': rate_limit.search.limit,
                    'remaining': rate_limit.search.remaining,
                    'reset_time': rate_limit.search.reset
                }
            }
        except Exception as e:
            logger.error(f"❌ Error obteniendo rate limit: {e}")
            return {}