"""
Content Analyzer Service

This module provides content analysis capabilities using OpenAI's API.
"""

from typing import Dict, Any, List, Optional, Union
from .base_service import BaseAIService
from .config import (
    DEFAULT_TEXT_MODEL,
    DEFAULT_TEMPERATURE,
    REQUEST_TIMEOUT,
    ENABLE_CONTENT_MODERATION,
    CONTENT_MODERATION_MODEL
)

class ContentAnalyzerService(BaseAIService):
    """Service for analyzing content using AI"""
    
    def __init__(self):
        """Initialize the content analyzer service"""
        super().__init__()
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of a text
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing sentiment analysis or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'analyze_sentiment',
                text=text[:100] + "..." if len(text) > 100 else text
            )
            
            # Create the prompt
            prompt = f"""
            Analyse le sentiment du texte suivant et réponds uniquement avec un JSON contenant:
            - sentiment: "positif", "négatif", ou "neutre"
            - score: un nombre entre -1 (très négatif) et 1 (très positif)
            - émotions: un tableau des émotions principales détectées
            - confiance: un nombre entre 0 et 1 indiquant le niveau de confiance de l'analyse
            
            Texte à analyser: "{text}"
            
            Réponds uniquement avec le JSON, sans texte supplémentaire.
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un expert en analyse de sentiment qui répond uniquement en format JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for more consistent results
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the analysis
            analysis = response.choices[0].message.content
            
            # Log the response
            self._log_response('analyze_sentiment', analysis)
            
            return self._format_success_response(analysis)
            
        except Exception as e:
            return self._handle_error(e)
    
    def check_content_moderation(self, text: str) -> Dict[str, Any]:
        """
        Check if content violates content policies
        
        Args:
            text: The text to check
            
        Returns:
            Dictionary containing moderation results or error information
        """
        if not ENABLE_CONTENT_MODERATION:
            return self._format_success_response({
                'flagged': False,
                'categories': {},
                'category_scores': {}
            })
            
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'check_content_moderation',
                text=text[:100] + "..." if len(text) > 100 else text
            )
            
            # Make the API request
            response = self.client.moderations.create(
                input=text,
                model=CONTENT_MODERATION_MODEL
            )
            
            # Extract the results
            result = response.results[0]
            moderation_result = {
                'flagged': result.flagged,
                'categories': {k: v for k, v in result.categories.items()},
                'category_scores': {k: v for k, v in result.category_scores.items()}
            }
            
            # Log the response
            self._log_response('check_content_moderation', moderation_result)
            
            return self._format_success_response(moderation_result)
            
        except Exception as e:
            return self._handle_error(e)
    
    def optimize_content(self, 
                        text: str, 
                        platform: str,
                        target_audience: str,
                        optimization_goals: List[str] = None) -> Dict[str, Any]:
        """
        Optimize content for a specific platform and audience
        
        Args:
            text: The text to optimize
            platform: The social media platform
            target_audience: Description of the target audience
            optimization_goals: List of optimization goals (e.g., "engagement", "clicks")
            
        Returns:
            Dictionary containing optimized content or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Set default optimization goals if none provided
            if not optimization_goals:
                optimization_goals = ["engagement", "clarté", "pertinence"]
            
            # Log the request
            self._log_request(
                'optimize_content',
                text=text[:100] + "..." if len(text) > 100 else text,
                platform=platform,
                target_audience=target_audience,
                optimization_goals=optimization_goals
            )
            
            # Create the prompt
            prompt = f"""
            Optimise le contenu suivant pour la plateforme {platform} et l'audience cible: {target_audience}.
            
            Objectifs d'optimisation: {', '.join(optimization_goals)}
            
            Contenu original:
            "{text}"
            
            Fournis une version optimisée du contenu, puis explique brièvement les modifications apportées et pourquoi elles amélioreront les performances selon les objectifs d'optimisation.
            
            Format de réponse:
            ```
            CONTENU OPTIMISÉ:
            [contenu optimisé ici]
            
            EXPLICATIONS:
            [explications des modifications ici]
            ```
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un expert en optimisation de contenu pour les réseaux sociaux."},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the optimized content
            optimized_content = response.choices[0].message.content
            
            # Log the response
            self._log_response('optimize_content', optimized_content)
            
            return self._format_success_response(optimized_content)
            
        except Exception as e:
            return self._handle_error(e)
    
    def extract_keywords(self, text: str, count: int = 10) -> Dict[str, Any]:
        """
        Extract keywords from text
        
        Args:
            text: The text to extract keywords from
            count: Number of keywords to extract
            
        Returns:
            Dictionary containing extracted keywords or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'extract_keywords',
                text=text[:100] + "..." if len(text) > 100 else text,
                count=count
            )
            
            # Create the prompt
            prompt = f"""
            Extrais les {count} mots-clés ou expressions les plus pertinents du texte suivant.
            Réponds uniquement avec un tableau JSON des mots-clés, sans texte supplémentaire.
            
            Texte:
            "{text}"
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un expert en extraction de mots-clés qui répond uniquement en format JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for more consistent results
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the keywords
            keywords = response.choices[0].message.content
            
            # Log the response
            self._log_response('extract_keywords', keywords)
            
            return self._format_success_response(keywords)
            
        except Exception as e:
            return self._handle_error(e)
    
    def analyze_engagement_potential(self, 
                                    text: str, 
                                    platform: str,
                                    target_audience: str) -> Dict[str, Any]:
        """
        Analyze the engagement potential of content
        
        Args:
            text: The content to analyze
            platform: The social media platform
            target_audience: Description of the target audience
            
        Returns:
            Dictionary containing engagement analysis or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'analyze_engagement_potential',
                text=text[:100] + "..." if len(text) > 100 else text,
                platform=platform,
                target_audience=target_audience
            )
            
            # Create the prompt
            prompt = f"""
            Analyse le potentiel d'engagement du contenu suivant pour la plateforme {platform} et l'audience cible: {target_audience}.
            
            Contenu:
            "{text}"
            
            Réponds uniquement avec un JSON contenant:
            - score: un nombre entre 0 et 100 représentant le potentiel d'engagement
            - forces: un tableau des points forts du contenu
            - faiblesses: un tableau des points faibles du contenu
            - suggestions: un tableau de suggestions pour améliorer l'engagement
            
            Réponds uniquement avec le JSON, sans texte supplémentaire.
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un expert en analyse d'engagement sur les réseaux sociaux qui répond uniquement en format JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the analysis
            analysis = response.choices[0].message.content
            
            # Log the response
            self._log_response('analyze_engagement_potential', analysis)
            
            return self._format_success_response(analysis)
            
        except Exception as e:
            return self._handle_error(e)

