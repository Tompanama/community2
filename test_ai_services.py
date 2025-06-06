#!/usr/bin/env python3
"""
Test script for AI services

This script tests the AI services to ensure they are working correctly.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import AI services
from src.services.ai.text_generation import TextGenerationService
from src.services.ai.image_generation import ImageGenerationService
from src.services.ai.content_analyzer import ContentAnalyzerService
from src.services.ai.response_generator import ResponseGeneratorService

def test_text_generation():
    """Test the text generation service"""
    print("\n=== Testing Text Generation Service ===")
    
    service = TextGenerationService()
    
    # Test basic text generation
    print("\nTesting basic text generation...")
    result = service.generate_text(
        prompt="Écris un court paragraphe sur l'importance du community management pour les entreprises.",
        max_tokens=100
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Generated text: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")
    
    # Test post generation
    print("\nTesting post generation...")
    result = service.generate_post(
        platform="Instagram",
        topic="Lancement d'un nouveau produit tech",
        tone="enthousiaste",
        length=200,
        hashtag_count=5
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Generated post: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")
    
    # Test content ideas generation
    print("\nTesting content ideas generation...")
    result = service.generate_content_ideas(
        platform="LinkedIn",
        industry="Marketing digital",
        count=3
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Generated ideas: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")

def test_image_generation():
    """Test the image generation service"""
    print("\n=== Testing Image Generation Service ===")
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(os.getcwd(), 'uploads', 'test_images')
    os.makedirs(uploads_dir, exist_ok=True)
    
    service = ImageGenerationService(upload_dir=uploads_dir)
    
    # Test basic image generation
    print("\nTesting basic image generation...")
    result = service.generate_image(
        prompt="Un logo minimaliste pour une application de community management avec des éléments de réseaux sociaux et d'intelligence artificielle",
        size="512x512"  # Smaller size for testing
    )
    
    if result.get('success'):
        print("✅ Success!")
        image_path = result['data'].get('image_path')
        if image_path and os.path.exists(image_path):
            print(f"Image saved to: {image_path}")
        else:
            print("Image data received but not saved to disk")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")

def test_content_analyzer():
    """Test the content analyzer service"""
    print("\n=== Testing Content Analyzer Service ===")
    
    service = ContentAnalyzerService()
    
    # Test sentiment analysis
    print("\nTesting sentiment analysis...")
    result = service.analyze_sentiment(
        text="J'adore cette nouvelle application de community management ! Elle est intuitive et m'aide à gagner beaucoup de temps."
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Sentiment analysis: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")
    
    # Test content optimization
    print("\nTesting content optimization...")
    result = service.optimize_content(
        text="Notre nouveau produit est maintenant disponible. Il a beaucoup de fonctionnalités intéressantes. Vous devriez l'acheter.",
        platform="Instagram",
        target_audience="Jeunes professionnels intéressés par la technologie",
        optimization_goals=["engagement", "conversion"]
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Optimized content: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")

def test_response_generator():
    """Test the response generator service"""
    print("\n=== Testing Response Generator Service ===")
    
    service = ResponseGeneratorService()
    
    # Test comment response generation
    print("\nTesting comment response generation...")
    result = service.generate_comment_response(
        comment="Est-ce que votre application fonctionne sur Android ?",
        post_content="Découvrez notre nouvelle application de community management avec IA intégrée !",
        brand_voice="Professionnel mais amical, axé sur le service client",
        response_type="informative"
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Generated response: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")
    
    # Test DM response generation
    print("\nTesting DM response generation...")
    result = service.generate_dm_response(
        message="Bonjour, j'ai un problème avec mon compte premium. Je ne peux pas accéder à certaines fonctionnalités.",
        conversation_history=[
            {"role": "user", "content": "Bonjour, j'ai une question sur votre application."},
            {"role": "assistant", "content": "Bonjour ! Je serais ravi de vous aider. Quelle est votre question ?"}
        ],
        brand_voice="Professionnel, serviable, orienté solution",
        customer_info={"subscription": "Premium", "signup_date": "2025-01-15"}
    )
    
    if result.get('success'):
        print("✅ Success!")
        print(f"Generated DM response: {result['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {result.get('error')}: {result.get('message')}")

def main():
    """Main function to run all tests"""
    print("Starting AI services tests...")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ Warning: OPENAI_API_KEY environment variable is not set.")
        print("Tests will use the default API key from config.py")
    
    try:
        # Run tests
        test_text_generation()
        test_content_analyzer()
        test_response_generator()
        
        # Image generation test is optional as it uses more API credits
        run_image_test = input("\nDo you want to run the image generation test? (y/n): ")
        if run_image_test.lower() == 'y':
            test_image_generation()
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Error during tests: {str(e)}")

if __name__ == "__main__":
    main()

