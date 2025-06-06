"""
Image Generation Service

This module provides image generation capabilities using OpenAI's API.
"""

import os
import base64
import time
import uuid
from typing import Dict, Any, List, Optional, Union
from .base_service import BaseAIService
from .config import (
    DEFAULT_IMAGE_MODEL,
    FALLBACK_IMAGE_MODEL,
    REQUEST_TIMEOUT,
    PROMPT_TEMPLATES
)

class ImageGenerationService(BaseAIService):
    """Service for generating images using AI"""
    
    def __init__(self, upload_dir: str = "/tmp/community_ai/uploads"):
        """
        Initialize the image generation service
        
        Args:
            upload_dir: Directory to save generated images
        """
        super().__init__()
        self.upload_dir = upload_dir
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def generate_image(self,
                      prompt: str,
                      model: str = DEFAULT_IMAGE_MODEL,
                      size: str = "1024x1024",
                      quality: str = "standard",
                      save_to_disk: bool = True,
                      use_cache: bool = True) -> Dict[str, Any]:
        """
        Generate an image based on a prompt
        
        Args:
            prompt: The prompt to generate an image from
            model: The model to use for generation
            size: Image size (e.g., "1024x1024", "512x512")
            quality: Image quality ("standard" or "hd")
            save_to_disk: Whether to save the image to disk
            use_cache: Whether to use cached responses
            
        Returns:
            Dictionary containing the generated image info or error information
        """
        try:
            # Check rate limits
            self._rate_limit_check()
            
            # Log the request
            self._log_request(
                'generate_image',
                prompt=prompt,
                model=model,
                size=size,
                quality=quality
            )
            
            # Check cache if enabled
            if use_cache:
                cache_key = self._generate_cache_key(
                    prompt=prompt,
                    model=model,
                    size=size,
                    quality=quality
                )
                cached_response = self._get_from_cache(cache_key)
                if cached_response:
                    return self._format_success_response(cached_response)
            
            # Make the API request
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="b64_json",
                timeout=REQUEST_TIMEOUT
            )
            
            # Extract the image data
            image_data = response.data[0].b64_json
            
            # Save the image to disk if requested
            image_path = None
            if save_to_disk and image_data:
                # Generate a unique filename
                filename = f"{uuid.uuid4()}.png"
                image_path = os.path.join(self.upload_dir, filename)
                
                # Decode and save the image
                with open(image_path, "wb") as image_file:
                    image_file.write(base64.b64decode(image_data))
            
            # Prepare the result
            result = {
                'image_data': image_data,
                'image_path': image_path,
                'prompt': prompt,
                'model': model,
                'size': size,
                'quality': quality,
                'timestamp': time.time()
            }
            
            # Log the response (without the image data)
            log_result = result.copy()
            log_result['image_data'] = f"<base64 data of length {len(image_data) if image_data else 0}>"
            self._log_response('generate_image', log_result)
            
            # Cache the response if caching is enabled
            if use_cache:
                self._save_to_cache(cache_key, result)
            
            return self._format_success_response(result)
            
        except Exception as e:
            # Try fallback model if primary fails
            if model == DEFAULT_IMAGE_MODEL:
                try:
                    return self.generate_image(
                        prompt=prompt,
                        model=FALLBACK_IMAGE_MODEL,
                        size=size,
                        quality=quality,
                        save_to_disk=save_to_disk,
                        use_cache=use_cache
                    )
                except Exception as fallback_error:
                    return self._handle_error(fallback_error)
            else:
                return self._handle_error(e)
    
    def generate_social_media_image(self,
                                   platform: str,
                                   description: str,
                                   style: str = "moderne",
                                   mood: str = "positif",
                                   colors: str = "bleu, blanc") -> Dict[str, Any]:
        """
        Generate an image for social media
        
        Args:
            platform: The social media platform (e.g., "Instagram", "LinkedIn")
            description: Description of the image content
            style: The visual style of the image
            mood: The mood or emotion of the image
            colors: Dominant colors to use
            
        Returns:
            Dictionary containing the generated image info or error information
        """
        # Format the prompt using the template
        prompt = PROMPT_TEMPLATES['image_prompt'].format(
            platform=platform,
            description=description,
            style=style,
            mood=mood,
            colors=colors
        )
        
        # Determine the appropriate size based on platform
        size = "1024x1024"  # Default square format
        if platform.lower() == "instagram":
            size = "1024x1024"  # Square for Instagram
        elif platform.lower() == "facebook":
            size = "1792x1024"  # Landscape for Facebook
        elif platform.lower() == "twitter" or platform.lower() == "x":
            size = "1792x1024"  # Landscape for Twitter/X
        elif platform.lower() == "linkedin":
            size = "1792x1024"  # Landscape for LinkedIn
        elif platform.lower() == "pinterest":
            size = "1024x1792"  # Portrait for Pinterest
        elif platform.lower() == "tiktok":
            size = "1024x1792"  # Portrait for TikTok
        
        # Generate the image
        return self.generate_image(
            prompt=prompt,
            size=size,
            quality="standard"
        )
    
    def generate_profile_picture(self,
                               description: str,
                               style: str = "professionnel",
                               background: str = "neutre") -> Dict[str, Any]:
        """
        Generate a profile picture
        
        Args:
            description: Description of the profile picture
            style: The visual style of the image
            background: Background style or color
            
        Returns:
            Dictionary containing the generated image info or error information
        """
        prompt = f"Une photo de profil professionnelle avec {description}. Style: {style}. Arrière-plan: {background}. La photo doit être adaptée pour une utilisation comme photo de profil sur les réseaux sociaux, centrée et bien cadrée."
        
        # Generate the image (always square for profile pictures)
        return self.generate_image(
            prompt=prompt,
            size="1024x1024",
            quality="hd"  # Higher quality for profile pictures
        )
    
    def generate_banner(self,
                       description: str,
                       brand_name: str = "",
                       style: str = "minimaliste",
                       colors: str = "") -> Dict[str, Any]:
        """
        Generate a banner image
        
        Args:
            description: Description of the banner content
            brand_name: Name of the brand to include
            style: The visual style of the image
            colors: Dominant colors to use
            
        Returns:
            Dictionary containing the generated image info or error information
        """
        color_prompt = f"avec les couleurs dominantes: {colors}" if colors else ""
        brand_prompt = f"incluant le nom de marque '{brand_name}'" if brand_name else ""
        
        prompt = f"Une bannière web {style} {color_prompt} {brand_prompt} montrant {description}. La bannière doit être adaptée pour un site web ou les réseaux sociaux, avec un design professionnel et attrayant."
        
        # Generate the image (wide format for banners)
        return self.generate_image(
            prompt=prompt,
            size="1792x1024",
            quality="standard"
        )

