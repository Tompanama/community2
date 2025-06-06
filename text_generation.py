"""
Text Generation Service

This module provides text generation capabilities using OpenAI's API.
"""

import time
from typing import Dict, Any, List, Optional, Union
from .base_service import BaseAIService
from .config import (
    DEFAULT_TEXT_MODEL,
    FALLBACK_TEXT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    REQUEST_TIMEOUT,
    PROMPT_TEMPLATES
)

class TextGenerationService(BaseAIService):
    """Service for generating text content using AI"""
    
    def __init__(self):
        """Initialize the text generation service"""
        super().__init__()
        
    def generate_text(self, 
                     prompt: str, 
                     model: str = DEFAULT_TEXT_MODEL,
                     temperature: float = DEFAULT_TEMPERATURE,
                     max_tokens: int = DEFAULT_MAX_TOKENS,
                     use_cache: bool = True) -> Dict[str, Any]:
        """
        Generate text based on a prompt
        
        Args:
            prompt: The prompt to generate text from
            model: The model to use for generation
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Maximum number of tokens to generate
            use_cache: Whether to use cached responses
            
        Returns:
            Dictionary containing the generated text or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'generate_text',
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Check cache if enabled
            if use_cache:
                cache_key = self._generate_cache_key(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                cached_response = self._get_from_cache(cache_key)
                if cached_response:
                    return self._format_success_response(cached_response)
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional community manager assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the generated text
            generated_text = response.choices[0].message.content
            
            # Log the response
            self._log_response('generate_text', generated_text)
            
            # Cache the response if caching is enabled
            if use_cache:
                self._save_to_cache(cache_key, generated_text)
            
            return self._format_success_response(generated_text)
            
        except Exception as e:
            # Try fallback model if primary fails
            if model == DEFAULT_TEXT_MODEL:
                try:
                    return self.generate_text(
                        prompt=prompt,
                        model=FALLBACK_TEXT_MODEL,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        use_cache=use_cache
                    )
                except Exception as fallback_error:
                    return self._handle_error(fallback_error)
            else:
                return self._handle_error(e)
    
    def generate_post(self,
                     platform: str,
                     topic: str,
                     tone: str = "professionnel",
                     length: int = 280,
                     hashtag_count: int = 3) -> Dict[str, Any]:
        """
        Generate a social media post
        
        Args:
            platform: The social media platform (e.g., "Instagram", "LinkedIn")
            topic: The topic of the post
            tone: The tone of the post (e.g., "professionnel", "décontracté")
            length: Maximum character length
            hashtag_count: Number of hashtags to include
            
        Returns:
            Dictionary containing the generated post or error information
        """
        # Format the prompt using the template
        prompt = PROMPT_TEMPLATES['post_generation'].format(
            platform=platform,
            topic=topic,
            tone=tone,
            length=length,
            hashtag_count=hashtag_count
        )
        
        # Generate the post
        return self.generate_text(
            prompt=prompt,
            max_tokens=min(1000, length // 2)  # Estimate tokens based on characters
        )
    
    def generate_comment_response(self,
                                 comment: str,
                                 context: str,
                                 tone: str = "amical") -> Dict[str, Any]:
        """
        Generate a response to a comment
        
        Args:
            comment: The comment to respond to
            context: Additional context about the post or conversation
            tone: The tone of the response
            
        Returns:
            Dictionary containing the generated response or error information
        """
        # Format the prompt using the template
        prompt = PROMPT_TEMPLATES['comment_response'].format(
            comment=comment,
            context=context,
            tone=tone
        )
        
        # Generate the response
        return self.generate_text(
            prompt=prompt,
            max_tokens=200  # Shorter for comment responses
        )
    
    def generate_content_ideas(self,
                              platform: str,
                              industry: str,
                              count: int = 5) -> Dict[str, Any]:
        """
        Generate content ideas for a specific platform and industry
        
        Args:
            platform: The social media platform
            industry: The industry or niche
            count: Number of ideas to generate
            
        Returns:
            Dictionary containing the generated ideas or error information
        """
        # Format the prompt using the template
        prompt = PROMPT_TEMPLATES['content_ideas'].format(
            platform=platform,
            industry=industry,
            count=count
        )
        
        # Generate the ideas
        return self.generate_text(
            prompt=prompt,
            max_tokens=500
        )
    
    def generate_hashtags(self,
                         topic: str,
                         platform: str,
                         count: int = 10) -> Dict[str, Any]:
        """
        Generate relevant hashtags for a topic
        
        Args:
            topic: The topic to generate hashtags for
            platform: The social media platform
            count: Number of hashtags to generate
            
        Returns:
            Dictionary containing the generated hashtags or error information
        """
        # Format the prompt using the template
        prompt = PROMPT_TEMPLATES['hashtag_suggestions'].format(
            topic=topic,
            platform=platform,
            count=count
        )
        
        # Generate the hashtags
        result = self.generate_text(
            prompt=prompt,
            max_tokens=200
        )
        
        # If successful, process the hashtags
        if result['success']:
            # Extract hashtags from the text
            text = result['data']
            hashtags = []
            
            # Process the text to extract hashtags
            for word in text.split():
                word = word.strip().strip(',.;:!?"\'-()[]{}')
                if word.startswith('#'):
                    hashtags.append(word)
                elif not word.startswith('#') and len(word) > 1:
                    hashtags.append(f"#{word}")
            
            # Limit to the requested count
            hashtags = hashtags[:count]
            
            return self._format_success_response(hashtags)
        
        return result

