"""Base agent class for all Dr. Document agents"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from openai import OpenAI
from backend.config import settings
from backend.logger import logger


class BaseAgent(ABC):
    """Base class for all agents with LLM integration"""
    
    def __init__(self, agent_name: str, model: str = None):
        self.agent_name = agent_name
        self.model = model or settings.model_flash_lite  # Default to Flash Lite
        self.client = self._initialize_client()
        logger.info(f"Initialized {agent_name} with model {self.model}", emoji='AGENT')
    
    def _initialize_client(self) -> OpenAI:
        """Initialize OpenAI client for LongCat"""
        try:
            client = OpenAI(
                api_key=settings.longcat_api_key,
                base_url=settings.longcat_base_url
            )
            logger.success(f"LongCat client initialized for {self.agent_name}")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize LongCat client: {str(e)}", exc_info=True)
            raise
    
    def _call_llm(
        self,
        messages: list,
        max_tokens: int = None,
        temperature: float = 0.7
    ) -> str:
        """Call LLM and log the interaction"""
        try:
            # Determine max tokens based on model
            if max_tokens is None:
                if 'lite' in self.model.lower():
                    max_tokens = settings.max_tokens_lite
                elif 'thinking' in self.model.lower():
                    max_tokens = settings.max_tokens_thinking
                else:
                    max_tokens = settings.max_tokens_chat
            
            # Log LLM input
            logger.llm_input(self.model, messages)
            
            # Log LLM call details
            call_details = {
                'model': self.model,
                'max_tokens': max_tokens,
                'temperature': temperature,
                'messages_count': len(messages)
            }
            logger.llm_call(self.model, call_details)
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract response content
            result = response.choices[0].message.content
            
            # Log LLM output
            logger.llm_output(self.model, result)
            
            return result
            
        except Exception as e:
            logger.error(f"LLM call failed for {self.agent_name}: {str(e)}", exc_info=True)
            raise
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return result. Must be implemented by subclasses."""
        pass
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent with logging"""
        try:
            logger.agent_start(self.agent_name, f"Processing input: {str(input_data)[:100]}")
            result = self.process(input_data)
            logger.agent_complete(self.agent_name, f"Successfully processed")
            return result
        except Exception as e:
            logger.agent_failed(self.agent_name, str(e))
            raise
