"""
Validation utilities for the chatbot application.
"""
import re
from typing import List, Dict, Any, Optional

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_messages(messages: List[Dict[str, Any]]) -> None:
    """
    Validate chat messages format and content.
    
    Args:
        messages: List of message dictionaries
        
    Raises:
        ValidationError: If validation fails
    """
    if not messages:
        raise ValidationError("No messages provided")
    
    if not isinstance(messages, list):
        raise ValidationError("Messages must be a list")
    
    for i, message in enumerate(messages):
        if not isinstance(message, dict):
            raise ValidationError(f"Message {i} must be a dictionary")
        
        if 'role' not in message:
            raise ValidationError(f"Message {i} missing 'role' field")
        
        if 'content' not in message:
            raise ValidationError(f"Message {i} missing 'content' field")
        
        if message['role'] not in ['user', 'assistant', 'system']:
            raise ValidationError(f"Message {i} has invalid role: {message['role']}")
        
        if not isinstance(message['content'], str):
            raise ValidationError(f"Message {i} content must be a string")
        
        if len(message['content'].strip()) == 0:
            raise ValidationError(f"Message {i} content cannot be empty")

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input text.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        raise ValidationError("Input must be a string")
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def validate_json_structure(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate JSON structure has required fields.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Data must be a dictionary")
    
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

def validate_api_key_format(api_key: str) -> bool:
    """
    Validate Anthropic API key format.
    
    Args:
        api_key: API key string to validate
        
    Returns:
        bool: True if format looks valid, False otherwise
    """
    if not isinstance(api_key, str):
        return False
    
    # Anthropic API keys typically start with 'sk-ant-api'
    return api_key.startswith('sk-ant-api') and len(api_key) > 50
