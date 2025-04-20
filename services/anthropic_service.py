import anthropic
import yaml
from typing import Union
from models.provider_response import AIResponse, ErrorResponse
from pathlib import Path
from utils.rate_limiter import RateLimiter
from .base_service import BaseAIService

class AnthropicService(BaseAIService):
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        anthropic_config = config["providers"]["anthropic"]
        self.client = anthropic.Anthropic(api_key=anthropic_config["api_key"])
        self.model = anthropic_config["model"]
        self.price_per_token = anthropic_config["price_per_token"]
        
        self.rate_limiter = RateLimiter(
            entity="anthropic",
            rate_limit=anthropic_config["rate_limit"],
            rate_limit_window=anthropic_config["rate_limit_window"]
        )

    def get_provider_name(self) -> str:
        return "anthropic"
        
    def get_model_name(self) -> str:
        return self.model
        
    async def get_completion(self, prompt: str) -> Union[AIResponse, ErrorResponse]:
        try:
            if not self.rate_limiter.check_limit():
                return ErrorResponse(
                    model=self.model,
                    provider="anthropic",
                    error="Rate limit exceeded"
                )
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
            total_tokens = prompt_tokens + completion_tokens
            
            cost = (prompt_tokens * self.price_per_token["input"]) + \
                   (completion_tokens * self.price_per_token["output"])
            
            return AIResponse(
                content=response.content[0].text,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                model=self.model,
                cost=cost,
                provider="anthropic",
                error=None
            )
        except Exception as e:
            return ErrorResponse(
                model=self.model,
                provider="anthropic",
                error=str(e)
            )