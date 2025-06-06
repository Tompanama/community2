"""
AI Assistant Routes

This module provides API routes for AI assistant functionality.
"""

from flask import Blueprint, jsonify, request, current_app
from src.services.ai.text_generation import TextGenerationService
from src.services.ai.image_generation import ImageGenerationService
from src.services.ai.content_analyzer import ContentAnalyzerService
from src.services.ai.response_generator import ResponseGeneratorService
from src.routes.auth import token_required
import os

# Create blueprint
ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/api/ai')

# Initialize services
text_generation_service = TextGenerationService()
image_generation_service = ImageGenerationService(upload_dir=os.path.join(os.getcwd(), 'uploads', 'images'))
content_analyzer_service = ContentAnalyzerService()
response_generator_service = ResponseGeneratorService()

@ai_assistant_bp.route('/generate-text', methods=['POST'])
@token_required
def generate_text(current_user):
    """Generate text using AI"""
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({'success': False, 'error': 'Missing prompt parameter'}), 400
    
    prompt = data.get('prompt')
    model = data.get('model')
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 1000)
    
    result = text_generation_service.generate_text(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-post', methods=['POST'])
@token_required
def generate_post(current_user):
    """Generate a social media post using AI"""
    data = request.get_json()
    
    if not data or 'platform' not in data or 'topic' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    platform = data.get('platform')
    topic = data.get('topic')
    tone = data.get('tone', 'professionnel')
    length = data.get('length', 280)
    hashtag_count = data.get('hashtag_count', 3)
    
    result = text_generation_service.generate_post(
        platform=platform,
        topic=topic,
        tone=tone,
        length=length,
        hashtag_count=hashtag_count
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-content-ideas', methods=['POST'])
@token_required
def generate_content_ideas(current_user):
    """Generate content ideas using AI"""
    data = request.get_json()
    
    if not data or 'platform' not in data or 'industry' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    platform = data.get('platform')
    industry = data.get('industry')
    count = data.get('count', 5)
    
    result = text_generation_service.generate_content_ideas(
        platform=platform,
        industry=industry,
        count=count
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-hashtags', methods=['POST'])
@token_required
def generate_hashtags(current_user):
    """Generate hashtags using AI"""
    data = request.get_json()
    
    if not data or 'topic' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    topic = data.get('topic')
    platform = data.get('platform', 'Instagram')
    count = data.get('count', 10)
    
    result = text_generation_service.generate_hashtags(
        topic=topic,
        platform=platform,
        count=count
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-image', methods=['POST'])
@token_required
def generate_image(current_user):
    """Generate an image using AI"""
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({'success': False, 'error': 'Missing prompt parameter'}), 400
    
    prompt = data.get('prompt')
    model = data.get('model')
    size = data.get('size', '1024x1024')
    quality = data.get('quality', 'standard')
    
    result = image_generation_service.generate_image(
        prompt=prompt,
        model=model,
        size=size,
        quality=quality
    )
    
    if result.get('success'):
        # Extract the image path and convert to URL
        image_data = result['data']
        if 'image_path' in image_data and image_data['image_path']:
            # Get the relative path from the full path
            base_path = os.path.join(os.getcwd(), 'uploads')
            rel_path = os.path.relpath(image_data['image_path'], base_path)
            image_data['image_url'] = f"/uploads/{rel_path}"
        
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-social-media-image', methods=['POST'])
@token_required
def generate_social_media_image(current_user):
    """Generate a social media image using AI"""
    data = request.get_json()
    
    if not data or 'platform' not in data or 'description' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    platform = data.get('platform')
    description = data.get('description')
    style = data.get('style', 'moderne')
    mood = data.get('mood', 'positif')
    colors = data.get('colors', 'bleu, blanc')
    
    result = image_generation_service.generate_social_media_image(
        platform=platform,
        description=description,
        style=style,
        mood=mood,
        colors=colors
    )
    
    if result.get('success'):
        # Extract the image path and convert to URL
        image_data = result['data']
        if 'image_path' in image_data and image_data['image_path']:
            # Get the relative path from the full path
            base_path = os.path.join(os.getcwd(), 'uploads')
            rel_path = os.path.relpath(image_data['image_path'], base_path)
            image_data['image_url'] = f"/uploads/{rel_path}"
        
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/analyze-sentiment', methods=['POST'])
@token_required
def analyze_sentiment(current_user):
    """Analyze sentiment of text using AI"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Missing text parameter'}), 400
    
    text = data.get('text')
    
    result = content_analyzer_service.analyze_sentiment(text=text)
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/check-content-moderation', methods=['POST'])
@token_required
def check_content_moderation(current_user):
    """Check content moderation using AI"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Missing text parameter'}), 400
    
    text = data.get('text')
    
    result = content_analyzer_service.check_content_moderation(text=text)
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/optimize-content', methods=['POST'])
@token_required
def optimize_content(current_user):
    """Optimize content using AI"""
    data = request.get_json()
    
    if not data or 'text' not in data or 'platform' not in data or 'target_audience' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    text = data.get('text')
    platform = data.get('platform')
    target_audience = data.get('target_audience')
    optimization_goals = data.get('optimization_goals')
    
    result = content_analyzer_service.optimize_content(
        text=text,
        platform=platform,
        target_audience=target_audience,
        optimization_goals=optimization_goals
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-comment-response', methods=['POST'])
@token_required
def generate_comment_response(current_user):
    """Generate a response to a comment using AI"""
    data = request.get_json()
    
    if not data or 'comment' not in data or 'post_content' not in data or 'brand_voice' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    comment = data.get('comment')
    post_content = data.get('post_content')
    brand_voice = data.get('brand_voice')
    response_type = data.get('response_type', 'standard')
    max_length = data.get('max_length', 200)
    
    result = response_generator_service.generate_comment_response(
        comment=comment,
        post_content=post_content,
        brand_voice=brand_voice,
        response_type=response_type,
        max_length=max_length
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/generate-dm-response', methods=['POST'])
@token_required
def generate_dm_response(current_user):
    """Generate a response to a direct message using AI"""
    data = request.get_json()
    
    if not data or 'message' not in data or 'conversation_history' not in data or 'brand_voice' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    message = data.get('message')
    conversation_history = data.get('conversation_history')
    brand_voice = data.get('brand_voice')
    customer_info = data.get('customer_info')
    max_length = data.get('max_length', 500)
    
    result = response_generator_service.generate_dm_response(
        message=message,
        conversation_history=conversation_history,
        brand_voice=brand_voice,
        customer_info=customer_info,
        max_length=max_length
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@ai_assistant_bp.route('/chat', methods=['POST'])
@token_required
def chat_with_assistant(current_user):
    """Chat with the AI assistant"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'success': False, 'error': 'Missing message parameter'}), 400
    
    message = data.get('message')
    conversation_history = data.get('conversation_history', [])
    
    # Create a system message for the assistant
    system_message = """
    Tu es un assistant IA de community management nommé "Le Community". 
    Tu aides les utilisateurs à gérer leurs réseaux sociaux, créer du contenu, 
    planifier des publications, et analyser leurs performances.
    
    Tu peux:
    - Générer des idées de contenu
    - Suggérer des hashtags
    - Optimiser des textes pour différentes plateformes
    - Analyser le sentiment et l'engagement potentiel
    - Aider à créer des stratégies de contenu
    - Répondre aux questions sur le community management
    
    Sois professionnel, utile et concis dans tes réponses.
    """
    
    # Format the conversation history for the API
    formatted_history = [{"role": "system", "content": system_message}]
    
    # Add conversation history if available
    if conversation_history:
        for msg in conversation_history:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            formatted_history.append({"role": role, "content": content})
    
    # Add the current message
    formatted_history.append({"role": "user", "content": message})
    
    try:
        # Make the API request
        response = text_generation_service.client.chat.completions.create(
            model="gpt-4o",
            messages=formatted_history,
            temperature=0.7,
            max_tokens=1000,
            timeout=60
        )
        
        # Extract the assistant's response
        assistant_response = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'data': {
                'response': assistant_response,
                'role': 'assistant'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'AI Assistant Error',
            'message': str(e)
        }), 500

