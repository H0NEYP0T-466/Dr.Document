"""Configuration management for Dr. Document"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    longcat_api_key: str = os.getenv("LONGCAT_API_KEY", "")
    longcat_base_url: str = "https://api.longcat.chat/openai"
    
    # Model Configuration
    model_flash_lite: str = "LongCat-Flash-Lite"
    model_flash_chat: str = "LongCat-Flash-Chat"
    model_flash_thinking: str = "LongCat-Flash-Thinking"
    model_flash_thinking_2601: str = "LongCat-Flash-Thinking-2601"
    
    # Storage Configuration
    storage_path: str = "./backend/storage"
    
    # GitHub Configuration
    github_token: Optional[str] = None
    
    # Application Settings
    max_file_size: int = 1024 * 1024 * 10  # 10MB
    max_files_to_analyze: int = 90  # Maximum files to analyze per repository
    allowed_file_extensions: list = [
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c", ".h",
        ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
        ".html", ".css", ".scss", ".json", ".yaml", ".yml", ".md", ".txt"
    ]
    
    # LLM Configuration
    max_tokens_lite: int = 8192
    max_tokens_chat: int = 8192
    max_tokens_thinking: int = 8192
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
