
import os
import sys
import json
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import anthropic

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modules
from config.settings import get_config
from services.anthropic_service import AnthropicService
from utils.validators import validate_messages, ValidationError
from utils.logger import setup_logger

# Initialize configuration and logging
config = get_config()
logger = setup_logger(__name__)

# Create Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configure Flask app
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# Setup CORS
CORS(app, origins=config.CORS_ORIGINS)

# Initialize services
try:
    anthropic_service = AnthropicService()
    logger.info("Anthropic service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Anthropic service: {e}")
    anthropic_service = None

@app.route('/')
def index():
    """Serve the main portfolio page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {e}")
        return jsonify({"error": "Page not found"}), 404

@app.route('/chatbot')
def chatbot():
    """Serve the chatbot page."""
    try:
        return render_template('chatbot.html')
    except Exception as e:
        logger.error(f"Error serving chatbot page: {e}")
        return jsonify({"error": "Chatbot page not found"}), 404

@app.route('/samra-Younas-cv.pdf')
def download_cv():
    """Serve the CV PDF file."""
    try:
        return send_file('../samra-Younas-cv.pdf', as_attachment=True, download_name='samra-Younas-cv.pdf')
    except Exception as e:
        logger.error(f"Error serving CV file: {e}")
        return jsonify({"error": "CV file not found"}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for interacting with the AI assistant.
    
    Expected JSON payload:
    {
        "messages": [
            {"role": "user", "content": "Your message here"}
        ]
    }
    """
    try:
        # Check if service is available
        if not anthropic_service:
            return jsonify({
                "error": "Chat service is currently unavailable"
            }), 503
        
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Validate messages
        messages = data.get("messages", [])
        validate_messages(messages)
        
        # Get response from Anthropic
        reply = anthropic_service.chat(messages)
        
        logger.info(f"Successfully processed chat request with {len(messages)} messages")
        return jsonify({"reply": reply})
        
    except ValidationError as e:
        logger.warning(f"Validation error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 400
        
    except anthropic.AuthenticationError:
        logger.error("Anthropic authentication error")
        return jsonify({
            "error": "Invalid API key. Check your .env file."
        }), 401
        
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit hit")
        return jsonify({
            "error": "Rate limit hit. Please wait a moment."
        }), 429
        
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        JSON with service status and health information
    """
    try:
        health_status = {
            "status": "ok",
            "service": "portfolio-chatbot",
            "version": "1.0.0",
            "anthropic_service": "healthy" if anthropic_service and anthropic_service.health_check() else "unhealthy"
        }
        
        logger.debug("Health check completed successfully")
        return jsonify(health_status)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config_info():
    """
    Get public configuration information.
    
    Returns:
        JSON with non-sensitive configuration
    """
    try:
        public_config = {
            "model": config.ANTHROPIC_MODEL,
            "max_tokens": config.ANTHROPIC_MAX_TOKENS,
            "cors_origins": config.CORS_ORIGINS
        }
        
        return jsonify(public_config)
        
    except Exception as e:
        logger.error(f"Error getting config info: {e}")
        return jsonify({"error": "Configuration unavailable"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

def create_app(config_name=None):
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration name to use
        
    Returns:
        Flask app instance
    """
    global config, anthropic_service
    
    # Update configuration
    config = get_config(config_name)
    
    # Reinitialize services with new config
    try:
        anthropic_service = AnthropicService()
        logger.info(f"App created with {config_name} configuration")
    except Exception as e:
        logger.error(f"Failed to initialize services for {config_name}: {e}")
    
    return app

if __name__ == "__main__":
    # Validate configuration
    try:
        config.validate_config()
        logger.info("Configuration validation passed")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        exit(1)
    
    # Start the application
    logger.info(f"🚀 Flask application for Samra Younas Portfolio Chatbot. Backend for LLM Integration & Agentic Systems...")
    logger.info(f"📍 Running at: http://{config.HOST}:{config.PORT}")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
