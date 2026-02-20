"""Comprehensive color-coded logging system for Dr. Document"""
import io
import logging
import sys
from datetime import datetime
from typing import Any, Dict
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support"""
    
    # Color mappings for different log levels
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.BLUE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE,
        'SUCCESS': Fore.GREEN,
        'LLM': Fore.MAGENTA,
    }
    
    # Emoji mappings
    EMOJIS = {
        'INFO': '🔵',
        'WARNING': '🟡',
        'ERROR': '🔴',
        'SUCCESS': '🟢',
        'LLM': '🟣',
        'START': '🎯',
        'INPUT': '📥',
        'OUTPUT': '📤',
        'API': '🤖',
        'CHECK': '✅',
        'FAIL': '❌',
        'PROCESS': '⚙️',
        'FILE': '📄',
        'FOLDER': '📁',
        'AGENT': '🤖',
        'REVIEW': '🔍',
        'WRITE': '✍️',
        'READ': '👀',
    }
    
    def format(self, record):
        # Get the color for this log level
        color = self.COLORS.get(record.levelname, Fore.WHITE)
        
        # Format timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # Format the log message
        log_msg = f"{color}[{timestamp}] [{record.levelname}] {record.getMessage()}{Style.RESET_ALL}"
        
        if record.exc_info:
            log_msg += f"\n{self.formatException(record.exc_info)}"
        
        return log_msg


class DrDocumentLogger:
    """Custom logger for Dr. Document with comprehensive logging capabilities"""
    
    def __init__(self, name: str = "DrDocument"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler with color – use UTF-8 so emoji don't cause
        # UnicodeEncodeError on Windows consoles whose default codec (e.g.
        # cp1252) cannot encode multi-byte characters.
        # line_buffering=True ensures each log line is flushed immediately.
        # We intentionally do NOT close the wrapper on exit so that
        # sys.stdout.buffer is not closed underneath the interpreter.
        try:
            _stream = io.TextIOWrapper(
                sys.stdout.buffer, encoding='utf-8', errors='replace',
                line_buffering=True
            )
        except AttributeError:
            # Fallback for environments where sys.stdout has no .buffer
            # attribute (e.g. StringIO-based stdout in tests or some IDEs).
            _stream = sys.stdout
        console_handler = logging.StreamHandler(_stream)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(ColoredFormatter())
        self.logger.addHandler(console_handler)
        
        # File handler without color
        try:
            file_handler = logging.FileHandler('backend/dr_document.log', mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            )
            self.logger.addHandler(file_handler)
        except Exception:
            pass  # If file creation fails, continue with console only
    
    def _get_emoji(self, emoji_type: str) -> str:
        """Get emoji for log message"""
        return ColoredFormatter.EMOJIS.get(emoji_type, '')
    
    def info(self, message: str, emoji: str = 'INFO'):
        """Log info message"""
        emoji_char = self._get_emoji(emoji)
        self.logger.info(f"{emoji_char} {message}")
    
    def warning(self, message: str, emoji: str = 'WARNING'):
        """Log warning message"""
        emoji_char = self._get_emoji(emoji)
        self.logger.warning(f"{emoji_char} {message}")
    
    def error(self, message: str, emoji: str = 'ERROR', exc_info: bool = False):
        """Log error message"""
        emoji_char = self._get_emoji(emoji)
        self.logger.error(f"{emoji_char} {message}", exc_info=exc_info)
    
    def success(self, message: str):
        """Log success message"""
        emoji_char = self._get_emoji('SUCCESS')
        self.logger.info(f"{emoji_char} {message}")
    
    def llm_input(self, model: str, input_data: Any):
        """Log LLM input"""
        emoji_char = self._get_emoji('INPUT')
        self.logger.info(f"{emoji_char} [LLM INPUT] Model: {model}")
        self.logger.info(f"  Input: {str(input_data)[:500]}...")  # Truncate long inputs
    
    def llm_call(self, model: str, details: Dict[str, Any]):
        """Log LLM API call"""
        emoji_char = self._get_emoji('API')
        self.logger.info(f"{emoji_char} [LLM CALL] Model: {model}, Details: {details}")
    
    def llm_output(self, model: str, output_data: Any):
        """Log LLM output"""
        emoji_char = self._get_emoji('OUTPUT')
        self.logger.info(f"{emoji_char} [LLM OUTPUT] Model: {model}")
        self.logger.info(f"  Output: {str(output_data)[:500]}...")  # Truncate long outputs
    
    def agent_start(self, agent_name: str, task: str):
        """Log agent starting"""
        emoji_char = self._get_emoji('AGENT')
        self.logger.info(f"{emoji_char} [AGENT START] {agent_name}: {task}")
    
    def agent_complete(self, agent_name: str, result: str):
        """Log agent completion"""
        emoji_char = self._get_emoji('CHECK')
        self.logger.info(f"{emoji_char} [AGENT COMPLETE] {agent_name}: {result}")
    
    def agent_failed(self, agent_name: str, error: str):
        """Log agent failure"""
        emoji_char = self._get_emoji('FAIL')
        self.logger.error(f"{emoji_char} [AGENT FAILED] {agent_name}: {error}")
    
    def file_process(self, filename: str, action: str):
        """Log file processing"""
        emoji_char = self._get_emoji('FILE')
        self.logger.info(f"{emoji_char} [FILE] {action}: {filename}")
    
    def workflow_step(self, step: str, details: str = ""):
        """Log workflow step"""
        emoji_char = self._get_emoji('PROCESS')
        self.logger.info(f"{emoji_char} [WORKFLOW] {step} {details}")


# Global logger instance
logger = DrDocumentLogger()
