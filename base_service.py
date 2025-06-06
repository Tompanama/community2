"""
Base AI Service

This module provides a base class for all AI services.
"""

import time
import logging
import json
from typing import Dict, Any, Optional, List, Union
import openai
from openai import OpenAI
from .config import (
    OPENAI_API_KEY,
    OPENAI_ORG_ID,
    REQUEST_TIMEOUT,
    MAX_REQUESTS_PER_MINUTE,
    LOG_AI_REQUESTS,
    LOG_AI_RESPONSES,
    ENABLE_RESPONSE_CACHING,
    CACHE_EXPIRATION
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ai_service')

class BaseAIService:
    """Base class for AI services"""
    
    def __init__(self):
        """Initialize the AI service"""
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            organization=OPENAI_ORG_ID if OPENAI_ORG_ID else None
        )
        self.request_timestamps = []
        self.cache = {}
        
    def _rate_limit_check(self) -> None:
        """Check and enforce rate limits"""
        current_time = time.time()
        # Remove timestamps older than 1 minute
        self.request_timestamps = [ts for ts in self.request_timestamps 
                                  if current_time - ts < 60]
        
        # Check if we've exceeded the rate limit
        if len(self.request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
            sleep_time = 60 - (current_time - self.request_timestamps[0])
            if sleep_time > 0:
                logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        # Add current timestamp
        self.request_timestamps.append(time.time())
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get a response from cache if available and not expired"""
        if not ENABLE_RESPONSE_CACHING:
            return None
            
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if time.time() - cached_item['timestamp'] < CACHE_EXPIRATION:
                logger.info(f"Cache hit for key: {cache_key}")
                return cached_item['data']
            else:
                # Remove expired item
                del self.cache[cache_key]
                
        return None
    
    def _save_to_cache(self, cache_key: str, data: Any) -> None:
        """Save a response to cache"""
        if ENABLE_RESPONSE_CACHING:
            self.cache[cache_key] = {
                'data': data,
                'timestamp': time.time()
            }
    
    def _generate_cache_key(self, **kwargs) -> str:
        """Generate a cache key from the request parameters"""
        # Sort the kwargs to ensure consistent key generation
        sorted_items = sorted(kwargs.items())
        # Convert to a string and hash
        return json.dumps(sorted_items)
    
    def _log_request(self, service_name: str, **kwargs) -> None:
        """Log an AI request"""
        if LOG_AI_REQUESTS:
            # Remove sensitive or large data from logging
            log_kwargs = kwargs.copy()
            if 'api_key' in log_kwargs:
                log_kwargs['api_key'] = '***'
            if 'file' in log_kwargs:
                log_kwargs['file'] = f"<File: {log_kwargs['file'].name}>"
                
            logger.info(f"AI Request - {service_name}: {log_kwargs}")
    
    def _log_response(self, service_name: str, response: Any) -> None:
        """Log an AI response"""
        if LOG_AI_RESPONSES:
            # Truncate response for logging if it's too large
            response_str = str(response)
            if len(response_str) > 1000:
                response_str = response_str[:1000] + "... [truncated]"
                
            logger.info(f"AI Response - {service_name}: {response_str}")
    
    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors from the OpenAI API"""
        logger.error(f"AI Service Error: {str(error)}")
        
        if isinstance(error, openai.APIError):
            return {
                'success': False,
                'error': 'API Error',
                'message': str(error)
            }
        elif isinstance(error, openai.APIConnectionError):
            return {
                'success': False,
                'error': 'Connection Error',
                'message': 'Failed to connect to the API'
            }
        elif isinstance(error, openai.RateLimitError):
            return {
                'success': False,
                'error': 'Rate Limit Error',
                'message': 'Rate limit exceeded'
            }
        elif isinstance(error, openai.AuthenticationError):
            return {
                'success': False,
                'error': 'Authentication Error',
                'message': 'Invalid API key'
            }
        elif isinstance(error, openai.BadRequestError):
            return {
                'success': False,
                'error': 'Bad Request',
                'message': str(error)
            }
        else:
            return {
                'success': False,
                'error': 'Unknown Error',
                'message': str(error)
            }
    
    def _format_success_response(self, data: Any) -> Dict[str, Any]:
        """Format a successful response"""
        return {
            'success': True,
            'data': data
        }

