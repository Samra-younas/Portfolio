"""
Anthropic API service for handling chat interactions.
"""
import anthropic
from typing import List, Dict, Any
import logging
from config.settings import get_config

logger = logging.getLogger(__name__)

class AnthropicService:
    """Service class for interacting with Anthropic's Claude API."""
    
    def __init__(self):
        """Initialize the Anthropic service."""
        self.config = get_config()
        self.client = anthropic.Anthropic(api_key=self.config.ANTHROPIC_API_KEY)
        self.model = self.config.ANTHROPIC_MODEL
        self.max_tokens = self.config.ANTHROPIC_MAX_TOKENS
        
        # System prompt for Samra Younas persona
        self.system_prompt = """You are Samra Younas. 
Talk exactly like a real person in a casual interview.
Short sentences. Confident. No bullet points unless asked.
No em dashes. No formal language.

When someone asks about you, talk like this:
"Yeah so I've been building AI systems for about a year now 
at 3rd Eye Software. Mostly healthcare stuff — voice 
translators, RAG chatbots, that kind of thing. 
I use Claude API and LangChain a lot."

YOUR INFO:
- AI Engineer at 3rd Eye Software since May 2024
- Built: MediBridge, English Coach, Deals Scraper, 
  FHIR integration, RAG chatbot
- Skills: Python, Claude API, LangChain, React, Next.js,
  Whisper, FHIR, Docker
- Open to remote and Lahore/Karachi/Islamabad
- Email: samrayounas334@gmail.com
- GitHub: github.com/samra-younas
- LinkedIn: linkedin.com/in/samra-younas-ai

RULES:
- Max 3-4 lines per response
- Sound like a real 24 year old engineer talking
- First person always
- Never say "certainly" or "absolutely" or "great question"
- For visuals output exactly: [[SHOW:skills]] 
  or [[SHOW:projects]] or [[SHOW:experience]] 
  or [[SHOW:certs]]"""
    
    def chat(self, messages: List[Dict[str, Any]]) -> str:
        """
        Send a chat request to Anthropic API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            str: The assistant's response
            
        Raises:
            anthropic.AuthenticationError: If API key is invalid
            anthropic.RateLimitError: If rate limit is exceeded
            Exception: For other API errors
        """
        try:
            logger.info(f"Sending chat request with {len(messages)} messages")
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=messages
            )
            
            reply = response.content[0].text
            logger.info("Successfully received response from Anthropic API")
            return reply
            
        except anthropic.AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            raise
        except anthropic.RateLimitError as e:
            logger.error(f"Rate limit error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in chat: {e}")
            raise
    
    def health_check(self) -> bool:
        """
        Check if the Anthropic service is healthy.
        
        Returns:
            bool: True if service is healthy, False otherwise
        """
        try:
            # Simple test message to check API connectivity
            test_messages = [{"role": "user", "content": "test"}]
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                system=self.system_prompt,
                messages=test_messages
            )
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
