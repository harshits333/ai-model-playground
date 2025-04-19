from typing import Dict
import tiktoken

class TokenCounter:
    def __init__(self):
        self.encoders: Dict[str, any] = {
            "gpt-4o": tiktoken.encoding_for_model("gpt-4"),
            "claude-3-opus-20240229": None,  # Anthropic uses different tokenization
            "xai-model-1": None  # XAI tokenization unknown
        }

    def count_tokens(self, model: str, text: str) -> int:
        """Count tokens for a given model and text.
        
        Args:
            model: The model name (e.g. 'gpt-4o')
            text: The text to count tokens for
            
        Returns:
            Number of tokens
        """
        if model in self.encoders and self.encoders[model] is not None:
            return len(self.encoders[model].encode(text))
        
        # Fallback for models without specific encoders
        return len(text.split())  # Very rough approximation