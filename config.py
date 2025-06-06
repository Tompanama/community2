"""
AI Services Configuration

This module contains configuration settings for AI services.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
OPENAI_ORG_ID = os.getenv('OPENAI_ORG_ID', '')

# Default models
DEFAULT_TEXT_MODEL = "gpt-4o"
DEFAULT_IMAGE_MODEL = "dall-e-3"

# Fallback models (if primary models are unavailable)
FALLBACK_TEXT_MODEL = "gpt-3.5-turbo"
FALLBACK_IMAGE_MODEL = "dall-e-2"

# API request settings
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
REQUEST_TIMEOUT = 60  # seconds

# Rate limiting settings
MAX_REQUESTS_PER_MINUTE = 60
MAX_TOKENS_PER_MINUTE = 90000

# Content moderation settings
ENABLE_CONTENT_MODERATION = True
CONTENT_MODERATION_MODEL = "text-moderation-latest"

# Caching settings
ENABLE_RESPONSE_CACHING = True
CACHE_EXPIRATION = 3600  # seconds (1 hour)

# Logging settings
LOG_AI_REQUESTS = True
LOG_AI_RESPONSES = True

# Prompt templates
PROMPT_TEMPLATES = {
    'post_generation': """
    Génère un post pour {platform} sur le sujet suivant : {topic}.
    Ton : {tone}
    Longueur : {length} caractères maximum
    Hashtags : {hashtag_count} maximum
    """,
    
    'comment_response': """
    Réponds au commentaire suivant de manière {tone} :
    Commentaire : {comment}
    Contexte : {context}
    """,
    
    'content_ideas': """
    Génère {count} idées de contenu pour {platform} dans le domaine {industry}.
    Format : titre court + description en une phrase
    """,
    
    'hashtag_suggestions': """
    Suggère {count} hashtags pertinents pour un post sur {topic} 
    destiné à {platform}.
    """,
    
    'image_prompt': """
    Génère une image pour {platform} illustrant {description}.
    Style : {style}
    Ambiance : {mood}
    Couleurs dominantes : {colors}
    """
}

