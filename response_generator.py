"""
Response Generator Service

This module provides automated response generation capabilities using OpenAI's API.
"""

from typing import Dict, Any, List, Optional, Union
from .base_service import BaseAIService
from .config import (
    DEFAULT_TEXT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    REQUEST_TIMEOUT
)

class ResponseGeneratorService(BaseAIService):
    """Service for generating automated responses using AI"""
    
    def __init__(self):
        """Initialize the response generator service"""
        super().__init__()
    
    def generate_comment_response(self,
                                 comment: str,
                                 post_content: str,
                                 brand_voice: str,
                                 response_type: str = "standard",
                                 max_length: int = 200) -> Dict[str, Any]:
        """
        Generate a response to a comment on a post
        
        Args:
            comment: The comment to respond to
            post_content: The content of the original post
            brand_voice: Description of the brand's voice and tone
            response_type: Type of response (e.g., "standard", "question", "promotional")
            max_length: Maximum length of the response in characters
            
        Returns:
            Dictionary containing the generated response or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'generate_comment_response',
                comment=comment,
                post_content=post_content[:100] + "..." if len(post_content) > 100 else post_content,
                brand_voice=brand_voice,
                response_type=response_type,
                max_length=max_length
            )
            
            # Create the prompt
            prompt = f"""
            En tant que community manager pour une marque avec la voix suivante: "{brand_voice}",
            génère une réponse à ce commentaire sur un post.
            
            Post original:
            "{post_content}"
            
            Commentaire:
            "{comment}"
            
            Type de réponse souhaité: {response_type}
            Longueur maximale: {max_length} caractères
            
            La réponse doit être authentique, engageante, et refléter la voix de la marque.
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un community manager professionnel qui répond aux commentaires sur les réseaux sociaux."},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=min(DEFAULT_MAX_TOKENS, max_length // 2),  # Estimate tokens based on characters
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the generated response
            generated_response = response.choices[0].message.content
            
            # Log the response
            self._log_response('generate_comment_response', generated_response)
            
            return self._format_success_response(generated_response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def generate_dm_response(self,
                            message: str,
                            conversation_history: List[Dict[str, str]],
                            brand_voice: str,
                            customer_info: Dict[str, Any] = None,
                            max_length: int = 500) -> Dict[str, Any]:
        """
        Generate a response to a direct message
        
        Args:
            message: The message to respond to
            conversation_history: List of previous messages in the conversation
            brand_voice: Description of the brand's voice and tone
            customer_info: Optional information about the customer
            max_length: Maximum length of the response in characters
            
        Returns:
            Dictionary containing the generated response or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Format conversation history
            formatted_history = ""
            for msg in conversation_history[-5:]:  # Only use the last 5 messages
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                formatted_history += f"{role}: {content}\n"
            
            # Format customer info
            customer_context = ""
            if customer_info:
                customer_context = "Informations sur le client:\n"
                for key, value in customer_info.items():
                    customer_context += f"- {key}: {value}\n"
            
            # Log the request
            self._log_request(
                'generate_dm_response',
                message=message,
                conversation_history_length=len(conversation_history),
                brand_voice=brand_voice,
                has_customer_info=customer_info is not None,
                max_length=max_length
            )
            
            # Create the prompt
            prompt = f"""
            En tant que community manager pour une marque avec la voix suivante: "{brand_voice}",
            génère une réponse à ce message direct.
            
            {customer_context if customer_context else ""}
            
            Historique récent de la conversation:
            {formatted_history}
            
            Message le plus récent du client:
            "{message}"
            
            Longueur maximale: {max_length} caractères
            
            La réponse doit être personnalisée, utile, et refléter la voix de la marque.
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un community manager professionnel qui répond aux messages directs sur les réseaux sociaux."},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=min(DEFAULT_MAX_TOKENS, max_length // 2),  # Estimate tokens based on characters
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the generated response
            generated_response = response.choices[0].message.content
            
            # Log the response
            self._log_response('generate_dm_response', generated_response)
            
            return self._format_success_response(generated_response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def generate_faq_response(self,
                             question: str,
                             faq_data: List[Dict[str, str]],
                             brand_voice: str,
                             max_length: int = 500) -> Dict[str, Any]:
        """
        Generate a response to a frequently asked question
        
        Args:
            question: The question to answer
            faq_data: List of FAQ items with 'question' and 'answer' keys
            brand_voice: Description of the brand's voice and tone
            max_length: Maximum length of the response in characters
            
        Returns:
            Dictionary containing the generated response or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Format FAQ data
            formatted_faq = ""
            for item in faq_data:
                q = item.get('question', '')
                a = item.get('answer', '')
                formatted_faq += f"Q: {q}\nR: {a}\n\n"
            
            # Log the request
            self._log_request(
                'generate_faq_response',
                question=question,
                faq_data_length=len(faq_data),
                brand_voice=brand_voice,
                max_length=max_length
            )
            
            # Create the prompt
            prompt = f"""
            En tant que community manager pour une marque avec la voix suivante: "{brand_voice}",
            réponds à cette question en utilisant les informations de la FAQ ci-dessous.
            
            Question du client:
            "{question}"
            
            FAQ:
            {formatted_faq}
            
            Longueur maximale: {max_length} caractères
            
            Si la question n'est pas directement couverte par la FAQ, utilise les informations disponibles pour formuler une réponse utile.
            Si tu ne peux pas répondre à la question avec les informations disponibles, suggère poliment de contacter le service client.
            La réponse doit être claire, précise, et refléter la voix de la marque.
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un community manager professionnel qui répond aux questions fréquemment posées."},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=min(DEFAULT_MAX_TOKENS, max_length // 2),  # Estimate tokens based on characters
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the generated response
            generated_response = response.choices[0].message.content
            
            # Log the response
            self._log_response('generate_faq_response', generated_response)
            
            return self._format_success_response(generated_response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def generate_outreach_message(self,
                                 target_profile: Dict[str, Any],
                                 campaign_info: Dict[str, Any],
                                 brand_voice: str,
                                 platform: str,
                                 max_length: int = 500) -> Dict[str, Any]:
        """
        Generate a personalized outreach message
        
        Args:
            target_profile: Information about the target recipient
            campaign_info: Information about the campaign
            brand_voice: Description of the brand's voice and tone
            platform: The platform for the outreach (e.g., "LinkedIn", "Email")
            max_length: Maximum length of the message in characters
            
        Returns:
            Dictionary containing the generated message or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Format target profile
            formatted_profile = ""
            for key, value in target_profile.items():
                formatted_profile += f"- {key}: {value}\n"
            
            # Format campaign info
            formatted_campaign = ""
            for key, value in campaign_info.items():
                formatted_campaign += f"- {key}: {value}\n"
            
            # Log the request
            self._log_request(
                'generate_outreach_message',
                target_profile=target_profile,
                campaign_info=campaign_info,
                brand_voice=brand_voice,
                platform=platform,
                max_length=max_length
            )
            
            # Create the prompt
            prompt = f"""
            En tant que community manager pour une marque avec la voix suivante: "{brand_voice}",
            génère un message de prospection personnalisé pour la plateforme {platform}.
            
            Profil de la cible:
            {formatted_profile}
            
            Informations sur la campagne:
            {formatted_campaign}
            
            Longueur maximale: {max_length} caractères
            
            Le message doit être personnalisé, non-intrusif, et refléter la voix de la marque.
            Il doit établir une connexion authentique et inclure un appel à l'action clair.
            """
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=DEFAULT_TEXT_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un community manager professionnel spécialisé dans la prospection et l'outreach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=min(DEFAULT_MAX_TOKENS, max_length // 2),  # Estimate tokens based on characters
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the generated message
            generated_message = response.choices[0].message.content
            
            # Log the response
            self._log_response('generate_outreach_message', generated_message)
            
            return self._format_success_response(generated_message)
            
        except Exception as e:
            return self._handle_error(e)

