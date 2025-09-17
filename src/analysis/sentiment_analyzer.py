"""
Analizador de sentimientos para el Proyecto Empathy.

Este módulo analiza el tono y sentimiento de:
- Mensajes de commit
- Comentarios en pull requests
- Reviews de código
- Comunicación general del equipo
"""

import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import re

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VaderAnalyzer

logger = logging.getLogger(__name__)


@dataclass
class SentimentResult:
    """Resultado del análisis de sentimiento."""
    text: str
    sentiment_score: float  # -1.0 (muy negativo) a 1.0 (muy positivo)
    sentiment_label: str    # 'positive', 'negative', 'neutral'
    confidence: float      # 0.0 a 1.0
    emotions: Dict[str, float]  # Emociones específicas detectadas


class SentimentAnalyzer:
    """
    Analizador de sentimientos para comunicación de equipos de desarrollo.
    """
    
    def __init__(self, model: str = 'vader'):
        """
        Inicializa el analizador de sentimientos.
        
        Args:
            model: Modelo a usar ('vader', 'textblob', 'hybrid')
        """
        self.model = model
        self._setup_analyzers()
        
        # Patrones específicos para comunicación de desarrollo
        self._setup_dev_patterns()
    
    def _setup_analyzers(self):
        """Configura los analizadores de sentimiento."""
        try:
            # Descargar recursos de NLTK si es necesario
            try:
                nltk.data.find('vader_lexicon')
            except LookupError:
                nltk.download('vader_lexicon', quiet=True)
            
            # Inicializar analizadores
            self.vader = VaderAnalyzer()
            self.nltk_analyzer = SentimentIntensityAnalyzer()
            
            logger.info(f"✅ Analizador de sentimientos '{self.model}' inicializado")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando analizadores: {e}")
            raise
    
    def _setup_dev_patterns(self):
        """Configura patrones específicos para comunicación de desarrollo."""
        
        # Palabras/frases que indican sentimientos positivos en desarrollo
        self.positive_dev_patterns = [
            r'good\s+(?:job|work|catch|point)',
            r'nice\s+(?:work|job|fix|solution)',
            r'(?:well|great)\s+done',
            r'(?:looks|sounds)\s+good',
            r'thanks?\s+for',
            r'appreciate\s+(?:it|this|the)',
            r'clever\s+(?:solution|fix|approach)',
            r'clean\s+(?:code|implementation)',
            r'excellent\s+(?:work|job|solution)'
        ]
        
        # Palabras/frases que indican sentimientos negativos en desarrollo
        self.negative_dev_patterns = [
            r'(?:this\s+is\s+)?(?:terrible|awful|horrible)',
            r'what\s+(?:the\s+hell|were\s+you\s+thinking)',
            r'(?:this\s+)?(?:doesn\'?t\s+)?(?:work|make\s+sense)',
            r'(?:completely\s+)?(?:wrong|broken|buggy)',
            r'(?:waste\s+of\s+time|pointless)',
            r'(?:stupid|dumb|ridiculous)\s+(?:mistake|error|approach)',
            r'(?:why\s+would\s+you|how\s+could\s+you)',
            r'(?:sloppy|messy)\s+code'
        ]
        
        # Palabras que indican frustración técnica
        self.frustration_patterns = [
            r'(?:still\s+)?(?:not\s+working|broken)',
            r'(?:keeps?\s+)?(?:failing|crashing)',
            r'(?:can\'?t\s+)?(?:figure\s+out|understand)',
            r'(?:this\s+is\s+)?(?:confusing|unclear)',
            r'(?:urgent|critical)\s+(?:fix|bug)',
            r'(?:blocking|blocked\s+by)'
        ]
        
        # Compilar patrones para mejor rendimiento
        self.positive_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.positive_dev_patterns]
        self.negative_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.negative_dev_patterns]
        self.frustration_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.frustration_patterns]
    
    def analyze(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza el sentimiento en todos los datos recopilados.
        
        Args:
            raw_data: Datos recopilados del repositorio
            
        Returns:
            Resultados del análisis de sentimientos
        """
        logger.info("🧠 Iniciando análisis de sentimientos...")
        
        # 🚨 ADVERTENCIA SOBRE LIMITACIONES NLP
        logger.warning("⚠️  LIMITACIONES NLP: Los resultados pueden verse afectados por:")
        logger.warning("   - Sarcasmo e ironía no detectados correctamente") 
        logger.warning("   - Diferencias culturales en expresión")
        logger.warning("   - Jerga técnica malinterpretada")
        logger.warning("   - Contexto específico del equipo no considerado")
        logger.warning("   📋 Usar como herramienta de apoyo, no decisión final")
        
        results = {
            'commit_sentiments': self._analyze_commits(raw_data.get('commits', [])),
            'pr_sentiments': self._analyze_pull_requests(raw_data.get('pull_requests', [])),
            'overall_metrics': {},
            'sentiment_trends': {},
            'communication_patterns': {}
        }
        
        # Calcular métricas generales
        results['overall_metrics'] = self._calculate_overall_metrics(results)
        
        # Analizar tendencias temporales
        results['sentiment_trends'] = self._analyze_sentiment_trends(results)
        
        # Analizar patrones de comunicación
        results['communication_patterns'] = self._analyze_communication_patterns(results)
        
        logger.info("✅ Análisis de sentimientos completado")
        return results
    
    def _analyze_commits(self, commits: List[Any]) -> List[SentimentResult]:
        """Analiza el sentimiento en mensajes de commit."""
        commit_sentiments = []
        
        for commit in commits:
            if hasattr(commit, 'message'):
                message = commit.message
            else:
                message = commit.get('message', '')
            
            sentiment = self._analyze_text(message, context='commit')
            commit_sentiments.append(sentiment)
        
        return commit_sentiments
    
    def _analyze_pull_requests(self, pull_requests: List[Any]) -> Dict[str, List[SentimentResult]]:
        """Analiza el sentimiento en pull requests y sus comentarios."""
        pr_sentiments = {
            'titles': [],
            'comments': [],
            'reviews': []
        }
        
        for pr in pull_requests:
            # Analizar título del PR
            if hasattr(pr, 'title'):
                title = pr.title
            else:
                title = pr.get('title', '')
            
            title_sentiment = self._analyze_text(title, context='pr_title')
            pr_sentiments['titles'].append(title_sentiment)
            
            # Analizar comentarios
            comments = pr.comments if hasattr(pr, 'comments') else pr.get('comments', [])
            for comment in comments:
                comment_text = comment.get('body', '')
                if comment_text:
                    comment_sentiment = self._analyze_text(comment_text, context='comment')
                    pr_sentiments['comments'].append(comment_sentiment)
            
            # Analizar reviews
            reviews = pr.reviews if hasattr(pr, 'reviews') else pr.get('reviews', [])
            for review in reviews:
                review_text = review.get('body', '')
                if review_text:
                    review_sentiment = self._analyze_text(review_text, context='review')
                    pr_sentiments['reviews'].append(review_sentiment)
        
        return pr_sentiments
    
    def _analyze_text(self, text: str, context: str = 'general') -> SentimentResult:
        """
        Analiza el sentimiento de un texto específico.
        
        Args:
            text: Texto a analizar
            context: Contexto del texto ('commit', 'comment', 'review', etc.)
            
        Returns:
            Resultado del análisis de sentimiento
        """
        if not text or not text.strip():
            return SentimentResult(
                text=text,
                sentiment_score=0.0,
                sentiment_label='neutral',
                confidence=0.0,
                emotions={}
            )
        
        # Limpiar texto
        cleaned_text = self._clean_text(text)
        
        # Analizar con diferentes métodos según el modelo
        if self.model == 'vader':
            score, confidence, emotions = self._analyze_with_vader(cleaned_text, context)
        elif self.model == 'textblob':
            score, confidence, emotions = self._analyze_with_textblob(cleaned_text, context)
        else:  # hybrid
            score, confidence, emotions = self._analyze_hybrid(cleaned_text, context)
        
        # Determinar etiqueta
        label = self._get_sentiment_label(score)
        
        return SentimentResult(
            text=text,
            sentiment_score=score,
            sentiment_label=label,
            confidence=confidence,
            emotions=emotions
        )
    
    def _clean_text(self, text: str) -> str:
        """Limpia y normaliza el texto para análisis."""
        # Remover URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remover menciones de usuarios
        text = re.sub(r'@\w+', '', text)
        
        # Remover caracteres especiales excesivos
        text = re.sub(r'[^\w\s\.,!?\-\(\)]', ' ', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _analyze_with_vader(self, text: str, context: str) -> Tuple[float, float, Dict[str, float]]:
        """Analiza texto usando VADER."""
        scores = self.vader.polarity_scores(text)
        
        # VADER devuelve compound score (-1 a 1)
        sentiment_score = scores['compound']
        
        # Ajustar score basado en patrones específicos de desarrollo
        adjustment = self._get_dev_pattern_adjustment(text)
        sentiment_score = max(-1.0, min(1.0, sentiment_score + adjustment))
        
        # Calcular confianza basada en intensidad
        confidence = abs(sentiment_score)
        
        # Emociones básicas de VADER
        emotions = {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }
        
        return sentiment_score, confidence, emotions
    
    def _analyze_with_textblob(self, text: str, context: str) -> Tuple[float, float, Dict[str, float]]:
        """Analiza texto usando TextBlob."""
        blob = TextBlob(text)
        
        # TextBlob devuelve polarity (-1 a 1) y subjectivity (0 a 1)
        sentiment_score = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Ajustar score basado en patrones específicos de desarrollo
        adjustment = self._get_dev_pattern_adjustment(text)
        sentiment_score = max(-1.0, min(1.0, sentiment_score + adjustment))
        
        # Usar subjectividad como indicador de confianza
        confidence = subjectivity
        
        # Emociones simuladas para TextBlob
        emotions = {
            'positive': max(0, sentiment_score),
            'negative': max(0, -sentiment_score),
            'neutral': 1 - abs(sentiment_score)
        }
        
        return sentiment_score, confidence, emotions
    
    def _analyze_hybrid(self, text: str, context: str) -> Tuple[float, float, Dict[str, float]]:
        """Analiza texto usando un enfoque híbrido."""
        # Combinar VADER y TextBlob
        vader_score, _, vader_emotions = self._analyze_with_vader(text, context)
        textblob_score, textblob_confidence, textblob_emotions = self._analyze_with_textblob(text, context)
        
        # Promedio ponderado (VADER es mejor para texto informal)
        sentiment_score = (vader_score * 0.7) + (textblob_score * 0.3)
        
        # Usar la confianza más alta
        confidence = max(abs(vader_score), textblob_confidence)
        
        # Combinar emociones
        emotions = {
            'positive': (vader_emotions['positive'] + textblob_emotions['positive']) / 2,
            'negative': (vader_emotions['negative'] + textblob_emotions['negative']) / 2,
            'neutral': (vader_emotions['neutral'] + textblob_emotions['neutral']) / 2
        }
        
        return sentiment_score, confidence, emotions
    
    def _get_dev_pattern_adjustment(self, text: str) -> float:
        """Ajusta el score basado en patrones específicos de desarrollo."""
        adjustment = 0.0
        
        # Buscar patrones positivos
        positive_matches = sum(1 for pattern in self.positive_regex if pattern.search(text))
        if positive_matches > 0:
            adjustment += 0.2 * positive_matches
        
        # Buscar patrones negativos
        negative_matches = sum(1 for pattern in self.negative_regex if pattern.search(text))
        if negative_matches > 0:
            adjustment -= 0.3 * negative_matches
        
        # Buscar patrones de frustración (menos severo que negativo)
        frustration_matches = sum(1 for pattern in self.frustration_regex if pattern.search(text))
        if frustration_matches > 0:
            adjustment -= 0.1 * frustration_matches
        
        return max(-0.5, min(0.5, adjustment))
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convierte score numérico a etiqueta de sentimiento."""
        if score >= 0.1:
            return 'positive'
        elif score <= -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_overall_metrics(self, sentiment_results: Dict[str, Any]) -> Dict[str, float]:
        """Calcula métricas generales de sentimiento."""
        all_sentiments = []
        
        # Recopilar todos los sentimientos
        all_sentiments.extend(sentiment_results['commit_sentiments'])
        
        pr_sentiments = sentiment_results['pr_sentiments']
        all_sentiments.extend(pr_sentiments['titles'])
        all_sentiments.extend(pr_sentiments['comments'])
        all_sentiments.extend(pr_sentiments['reviews'])
        
        if not all_sentiments:
            return {
                'overall_sentiment_score': 0.0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'neutral_ratio': 0.0,
                'average_confidence': 0.0
            }
        
        # Calcular métricas
        scores = [s.sentiment_score for s in all_sentiments]
        labels = [s.sentiment_label for s in all_sentiments]
        confidences = [s.confidence for s in all_sentiments]
        
        return {
            'overall_sentiment_score': sum(scores) / len(scores),
            'positive_ratio': labels.count('positive') / len(labels),
            'negative_ratio': labels.count('negative') / len(labels),
            'neutral_ratio': labels.count('neutral') / len(labels),
            'average_confidence': sum(confidences) / len(confidences)
        }
    
    def _analyze_sentiment_trends(self, sentiment_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza tendencias temporales de sentimiento."""
        # TODO: Implementar análisis de tendencias temporales
        # Esto requeriría agrupar sentimientos por fecha y analizar cambios
        return {
            'trend_direction': 'stable',  # 'improving', 'declining', 'stable'
            'trend_strength': 0.0,
            'recent_change': 0.0
        }
    
    def _analyze_communication_patterns(self, sentiment_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza patrones de comunicación del equipo."""
        pr_sentiments = sentiment_results['pr_sentiments']
        
        # Analizar comentarios vs reviews
        comment_scores = [s.sentiment_score for s in pr_sentiments['comments']]
        review_scores = [s.sentiment_score for s in pr_sentiments['reviews']]
        
        patterns = {
            'comment_sentiment_avg': sum(comment_scores) / len(comment_scores) if comment_scores else 0.0,
            'review_sentiment_avg': sum(review_scores) / len(review_scores) if review_scores else 0.0,
            'communication_balance': 'balanced'  # 'positive_heavy', 'negative_heavy', 'balanced'
        }
        
        # Determinar balance de comunicación
        if patterns['comment_sentiment_avg'] > 0.2 and patterns['review_sentiment_avg'] > 0.2:
            patterns['communication_balance'] = 'positive_heavy'
        elif patterns['comment_sentiment_avg'] < -0.2 or patterns['review_sentiment_avg'] < -0.2:
            patterns['communication_balance'] = 'negative_heavy'
        
        return patterns