"""
Analizador de colaboración para el Proyecto Empathy.

Este módulo analiza patrones de colaboración y detecta:
- Silos de conocimiento
- Redes de colaboración
- Distribución de trabajo
- Patrones de interacción entre miembros del equipo
"""

import logging
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import networkx as nx

logger = logging.getLogger(__name__)


@dataclass
class CollaborationMetrics:
    """Métricas de colaboración de un miembro del equipo."""
    member: str
    files_touched: Set[str]
    commits_count: int
    pr_count: int
    reviews_given: int
    reviews_received: int
    collaboration_score: float
    knowledge_areas: List[str]


@dataclass
class KnowledgeSilo:
    """Representa un silo de conocimiento detectado."""
    files: List[str]
    primary_owner: str
    ownership_percentage: float
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    collaborators: List[str]


class CollaborationAnalyzer:
    """
    Analizador de patrones de colaboración en equipos de desarrollo.
    """
    
    def __init__(self):
        """Inicializa el analizador de colaboración."""
        self.collaboration_graph = nx.Graph()
        self.file_ownership = defaultdict(Counter)
        self.member_metrics = {}
        
    def analyze(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza patrones de colaboración en los datos del repositorio.
        
        Args:
            raw_data: Datos recopilados del repositorio
            
        Returns:
            Resultados del análisis de colaboración
        """
        logger.info("🤝 Iniciando análisis de colaboración...")
        
        # Limpiar estado previo
        self._reset_state()
        
        # Analizar commits y PRs
        self._analyze_commits(raw_data.get('commits', []))
        self._analyze_pull_requests(raw_data.get('pull_requests', []))
        
        # Calcular métricas
        results = {
            'member_metrics': self._calculate_member_metrics(),
            'knowledge_silos': self._detect_knowledge_silos(),
            'collaboration_network': self._analyze_collaboration_network(),
            'team_health_metrics': self._calculate_team_health_metrics(),
            'collaboration_score': 0.0,
            'knowledge_distribution_score': 0.0,
            'knowledge_silos_detected': False
        }
        
        # Calcular scores generales
        results['collaboration_score'] = self._calculate_collaboration_score(results)
        results['knowledge_distribution_score'] = self._calculate_knowledge_distribution_score(results)
        results['knowledge_silos_detected'] = len(results['knowledge_silos']) > 0
        
        logger.info("✅ Análisis de colaboración completado")
        return results
    
    def _reset_state(self):
        """Limpia el estado del analizador para un nuevo análisis."""
        self.collaboration_graph.clear()
        self.file_ownership.clear()
        self.member_metrics.clear()
    
    def _analyze_commits(self, commits: List[Any]):
        """Analiza commits para extraer patrones de colaboración."""
        for commit in commits:
            author = getattr(commit, 'author', None) or commit.get('author', 'Unknown')
            files = getattr(commit, 'files_changed', None) or commit.get('files_changed', [])
            
            if author == 'Unknown':
                continue
                
            # Registrar ownership de archivos
            for file_path in files:
                self.file_ownership[file_path][author] += 1
            
            # Inicializar métricas del miembro si no existe
            if author not in self.member_metrics:
                self.member_metrics[author] = {
                    'commits': 0,
                    'files_touched': set(),
                    'prs_created': 0,
                    'reviews_given': 0,
                    'reviews_received': 0,
                    'collaborators': set()
                }
            
            # Actualizar métricas
            self.member_metrics[author]['commits'] += 1
            self.member_metrics[author]['files_touched'].update(files)
    
    def _analyze_pull_requests(self, pull_requests: List[Any]):
        """Analiza pull requests para detectar colaboración."""
        for pr in pull_requests:
            author = getattr(pr, 'author', None) or pr.get('author', 'Unknown')
            
            if author == 'Unknown':
                continue
            
            # Inicializar métricas si no existe
            if author not in self.member_metrics:
                self.member_metrics[author] = {
                    'commits': 0,
                    'files_touched': set(),
                    'prs_created': 0,
                    'reviews_given': 0,
                    'reviews_received': 0,
                    'collaborators': set()
                }
            
            self.member_metrics[author]['prs_created'] += 1
            
            # Analizar reviews (colaboración)
            reviews = getattr(pr, 'reviews', None) or pr.get('reviews', [])
            reviewers = set()
            
            for review in reviews:
                reviewer = review.get('author', 'Unknown')
                if reviewer != 'Unknown' and reviewer != author:
                    reviewers.add(reviewer)
                    
                    # Inicializar métricas del reviewer si no existe
                    if reviewer not in self.member_metrics:
                        self.member_metrics[reviewer] = {
                            'commits': 0,
                            'files_touched': set(),
                            'prs_created': 0,
                            'reviews_given': 0,
                            'reviews_received': 0,
                            'collaborators': set()
                        }
                    
                    self.member_metrics[reviewer]['reviews_given'] += 1
                    self.member_metrics[author]['reviews_received'] += 1
                    
                    # Registrar colaboración mutua
                    self.member_metrics[author]['collaborators'].add(reviewer)
                    self.member_metrics[reviewer]['collaborators'].add(author)
                    
                    # Añadir edge al grafo de colaboración
                    if self.collaboration_graph.has_edge(author, reviewer):
                        self.collaboration_graph[author][reviewer]['weight'] += 1
                    else:
                        self.collaboration_graph.add_edge(author, reviewer, weight=1)
            
            # Analizar comentarios para detectar más colaboración
            comments = getattr(pr, 'comments', None) or pr.get('comments', [])
            commenters = set()
            
            for comment in comments:
                commenter = comment.get('author', 'Unknown')
                if commenter != 'Unknown' and commenter != author:
                    commenters.add(commenter)
            
            # Registrar colaboración a través de comentarios
            for commenter in commenters:
                if commenter not in self.member_metrics:
                    self.member_metrics[commenter] = {
                        'commits': 0,
                        'files_touched': set(),
                        'prs_created': 0,
                        'reviews_given': 0,
                        'reviews_received': 0,
                        'collaborators': set()
                    }
                
                self.member_metrics[author]['collaborators'].add(commenter)
                self.member_metrics[commenter]['collaborators'].add(author)
                
                # Añadir edge más ligero para comentarios
                if self.collaboration_graph.has_edge(author, commenter):
                    self.collaboration_graph[author][commenter]['weight'] += 0.5
                else:
                    self.collaboration_graph.add_edge(author, commenter, weight=0.5)
    
    def _calculate_member_metrics(self) -> List[CollaborationMetrics]:
        """Calcula métricas detalladas para cada miembro del equipo."""
        metrics_list = []
        
        for member, data in self.member_metrics.items():
            # Calcular score de colaboración individual
            collaboration_score = self._calculate_individual_collaboration_score(member, data)
            
            # Determinar áreas de conocimiento basadas en archivos más tocados
            knowledge_areas = self._identify_knowledge_areas(data['files_touched'])
            
            metrics = CollaborationMetrics(
                member=member,
                files_touched=data['files_touched'],
                commits_count=data['commits'],
                pr_count=data['prs_created'],
                reviews_given=data['reviews_given'],
                reviews_received=data['reviews_received'],
                collaboration_score=collaboration_score,
                knowledge_areas=knowledge_areas
            )
            
            metrics_list.append(metrics)
        
        return sorted(metrics_list, key=lambda x: x.collaboration_score, reverse=True)
    
    def _calculate_individual_collaboration_score(self, member: str, data: Dict[str, Any]) -> float:
        """Calcula score de colaboración para un miembro individual."""
        # Componentes del score
        review_participation = min(1.0, (data['reviews_given'] + data['reviews_received']) / 10.0)
        collaboration_breadth = min(1.0, len(data['collaborators']) / 5.0)
        activity_level = min(1.0, (data['commits'] + data['prs_created']) / 20.0)
        
        # Peso ponderado
        score = (review_participation * 0.4) + (collaboration_breadth * 0.4) + (activity_level * 0.2)
        
        return round(score, 3)
    
    def _identify_knowledge_areas(self, files_touched: Set[str]) -> List[str]:
        """Identifica áreas de conocimiento basadas en archivos tocados."""
        if not files_touched:
            return []
        
        # Agrupar por extensiones y directorios
        extensions = Counter()
        directories = Counter()
        
        for file_path in files_touched:
            # Extensión
            if '.' in file_path:
                ext = file_path.split('.')[-1].lower()
                extensions[ext] += 1
            
            # Directorio principal
            parts = file_path.split('/')
            if len(parts) > 1:
                directories[parts[0]] += 1
        
        # Identificar áreas principales
        knowledge_areas = []
        
        # Top extensiones
        for ext, count in extensions.most_common(3):
            if count >= 2:  # Al menos 2 archivos
                knowledge_areas.append(f"{ext} development")
        
        # Top directorios
        for dir_name, count in directories.most_common(2):
            if count >= 3:  # Al menos 3 archivos
                knowledge_areas.append(f"{dir_name} module")
        
        return knowledge_areas[:3]  # Máximo 3 áreas
    
    def _detect_knowledge_silos(self) -> List[KnowledgeSilo]:
        """Detecta silos de conocimiento en el código."""
        silos = []
        
        for file_path, ownership_counter in self.file_ownership.items():
            if not ownership_counter:
                continue
            
            total_contributions = sum(ownership_counter.values())
            most_common = ownership_counter.most_common()
            
            if len(most_common) == 0:
                continue
            
            primary_owner, primary_count = most_common[0]
            ownership_percentage = primary_count / total_contributions
            
            # Determinar si es un silo (threshold configurables)
            if ownership_percentage >= 0.8:  # 80% o más del código
                risk_level = self._determine_silo_risk_level(ownership_percentage, total_contributions)
                
                # Obtener colaboradores secundarios
                collaborators = [owner for owner, count in most_common[1:] if count > 0]
                
                silo = KnowledgeSilo(
                    files=[file_path],
                    primary_owner=primary_owner,
                    ownership_percentage=ownership_percentage,
                    risk_level=risk_level,
                    collaborators=collaborators
                )
                
                silos.append(silo)
        
        # Agrupar silos por owner para detectar patrones más grandes
        grouped_silos = self._group_silos_by_owner(silos)
        
        return grouped_silos
    
    def _determine_silo_risk_level(self, ownership_percentage: float, total_contributions: int) -> str:
        """Determina el nivel de riesgo de un silo de conocimiento."""
        if ownership_percentage >= 0.95:
            return 'critical'
        elif ownership_percentage >= 0.9:
            return 'high'
        elif ownership_percentage >= 0.85:
            return 'medium'
        else:
            return 'low'
    
    def _group_silos_by_owner(self, silos: List[KnowledgeSilo]) -> List[KnowledgeSilo]:
        """Agrupa silos por owner para detectar patrones más grandes."""
        owner_silos = defaultdict(list)
        
        for silo in silos:
            owner_silos[silo.primary_owner].append(silo)
        
        grouped_silos = []
        
        for owner, owner_silo_list in owner_silos.items():
            if len(owner_silo_list) > 1:
                # Combinar múltiples silos del mismo owner
                all_files = []
                all_collaborators = set()
                total_ownership = 0
                
                for silo in owner_silo_list:
                    all_files.extend(silo.files)
                    all_collaborators.update(silo.collaborators)
                    total_ownership += silo.ownership_percentage
                
                avg_ownership = total_ownership / len(owner_silo_list)
                risk_level = self._determine_silo_risk_level(avg_ownership, len(all_files))
                
                grouped_silo = KnowledgeSilo(
                    files=all_files,
                    primary_owner=owner,
                    ownership_percentage=avg_ownership,
                    risk_level=risk_level,
                    collaborators=list(all_collaborators)
                )
                
                grouped_silos.append(grouped_silo)
            else:
                grouped_silos.extend(owner_silo_list)
        
        return sorted(grouped_silos, key=lambda x: x.ownership_percentage, reverse=True)
    
    def _analyze_collaboration_network(self) -> Dict[str, Any]:
        """Analiza la red de colaboración del equipo."""
        if len(self.collaboration_graph.nodes()) == 0:
            return {
                'network_density': 0.0,
                'central_members': [],
                'isolated_members': [],
                'clusters': [],
                'network_health': 'poor'
            }
        
        # Calcular métricas de red
        density = nx.density(self.collaboration_graph)
        
        # Centralidad (miembros más conectados)
        centrality = nx.degree_centrality(self.collaboration_graph)
        central_members = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Miembros aislados (sin colaboración)
        all_members = set(self.member_metrics.keys())
        connected_members = set(self.collaboration_graph.nodes())
        isolated_members = list(all_members - connected_members)
        
        # Detectar clusters de colaboración
        clusters = []
        if len(self.collaboration_graph.nodes()) > 2:
            try:
                communities = nx.algorithms.community.greedy_modularity_communities(self.collaboration_graph)
                clusters = [list(community) for community in communities if len(community) > 1]
            except Exception as e:
                logger.warning(f"Error detectando clusters de colaboración: {e}")
                clusters = []
        
        # Evaluar salud de la red
        network_health = self._evaluate_network_health(density, len(isolated_members), len(clusters))
        
        return {
            'network_density': round(density, 3),
            'central_members': [(member, round(score, 3)) for member, score in central_members],
            'isolated_members': isolated_members,
            'clusters': clusters,
            'network_health': network_health
        }
    
    def _evaluate_network_health(self, density: float, isolated_count: int, cluster_count: int) -> str:
        """Evalúa la salud general de la red de colaboración."""
        if density >= 0.7 and isolated_count == 0:
            return 'excellent'
        elif density >= 0.5 and isolated_count <= 1:
            return 'good'
        elif density >= 0.3 and isolated_count <= 2:
            return 'fair'
        else:
            return 'poor'
    
    def _calculate_team_health_metrics(self) -> Dict[str, Any]:
        """Calcula métricas generales de salud del equipo."""
        if not self.member_metrics:
            return {
                'team_size': 0,
                'active_contributors': 0,
                'review_participation_rate': 0.0,
                'knowledge_distribution': 'poor',
                'collaboration_balance': 'unbalanced'
            }
        
        team_size = len(self.member_metrics)
        active_contributors = sum(1 for data in self.member_metrics.values() 
                                if data['commits'] > 0 or data['prs_created'] > 0)
        
        # Participación en reviews
        members_giving_reviews = sum(1 for data in self.member_metrics.values() 
                                   if data['reviews_given'] > 0)
        review_participation_rate = members_giving_reviews / team_size if team_size > 0 else 0.0
        
        # Distribución de conocimiento
        knowledge_distribution = self._evaluate_knowledge_distribution()
        
        # Balance de colaboración
        collaboration_balance = self._evaluate_collaboration_balance()
        
        return {
            'team_size': team_size,
            'active_contributors': active_contributors,
            'review_participation_rate': round(review_participation_rate, 3),
            'knowledge_distribution': knowledge_distribution,
            'collaboration_balance': collaboration_balance
        }
    
    def _evaluate_knowledge_distribution(self) -> str:
        """Evalúa qué tan bien distribuido está el conocimiento."""
        if not self.file_ownership:
            return 'unknown'
        
        # Calcular concentración de ownership
        concentration_scores = []
        for file_path, ownership_counter in self.file_ownership.items():
            if ownership_counter:
                total = sum(ownership_counter.values())
                max_ownership = max(ownership_counter.values())
                concentration = max_ownership / total
                concentration_scores.append(concentration)
        
        if not concentration_scores:
            return 'unknown'
        
        avg_concentration = sum(concentration_scores) / len(concentration_scores)
        
        if avg_concentration <= 0.5:
            return 'excellent'
        elif avg_concentration <= 0.7:
            return 'good'
        elif avg_concentration <= 0.85:
            return 'fair'
        else:
            return 'poor'
    
    def _evaluate_collaboration_balance(self) -> str:
        """Evalúa el balance de colaboración en el equipo."""
        if len(self.member_metrics) < 2:
            return 'insufficient_data'
        
        collaboration_scores = []
        for member, data in self.member_metrics.items():
            score = self._calculate_individual_collaboration_score(member, data)
            collaboration_scores.append(score)
        
        # Calcular distribución de scores
        min_score = min(collaboration_scores)
        max_score = max(collaboration_scores)
        score_range = max_score - min_score
        
        if score_range <= 0.3:
            return 'balanced'
        elif score_range <= 0.5:
            return 'somewhat_unbalanced'
        else:
            return 'unbalanced'
    
    def _calculate_collaboration_score(self, results: Dict[str, Any]) -> float:
        """Calcula score general de colaboración del equipo."""
        network_metrics = results['collaboration_network']
        team_metrics = results['team_health_metrics']
        
        # Componentes del score
        network_density = network_metrics['network_density']
        review_participation = team_metrics['review_participation_rate']
        
        # Penalizar miembros aislados
        isolation_penalty = len(network_metrics['isolated_members']) * 0.1
        
        # Score base
        base_score = (network_density * 0.5) + (review_participation * 0.5)
        
        # Aplicar penalización
        final_score = max(0.0, base_score - isolation_penalty)
        
        return round(final_score, 3)
    
    def _calculate_knowledge_distribution_score(self, results: Dict[str, Any]) -> float:
        """Calcula score de distribución de conocimiento."""
        team_metrics = results['team_health_metrics']
        knowledge_distribution = team_metrics['knowledge_distribution']
        
        # Mapear evaluación cualitativa a score numérico
        distribution_scores = {
            'excellent': 1.0,
            'good': 0.8,
            'fair': 0.6,
            'poor': 0.3,
            'unknown': 0.0
        }
        
        base_score = distribution_scores.get(knowledge_distribution, 0.0)
        
        # Penalizar por silos críticos
        critical_silos = sum(1 for silo in results['knowledge_silos'] 
                           if silo.risk_level == 'critical')
        silo_penalty = critical_silos * 0.2
        
        final_score = max(0.0, base_score - silo_penalty)
        
        return round(final_score, 3)