import yaml
import logging
from typing import Union
from pathlib import Path
from openai import OpenAI
from models.provider_response import AIResponse, ErrorResponse
from utils.rate_limiter import RateLimiter
from .base_service import BaseAIService

class XAIService(BaseAIService):
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        xai_config = config["providers"]["xai"]
        self.client = OpenAI(
            api_key=xai_config["api_key"],
            base_url=xai_config["base_url"]
        )
        self.model = xai_config["model"]
        self.price_per_token = xai_config["price_per_token"]
        
        self.rate_limiter = RateLimiter(
            entity="xai",
            rate_limit=xai_config["rate_limit"],
            rate_limit_window=xai_config["rate_limit_window"]
        )

    def get_provider_name(self) -> str:
        return "xai"
        
    def get_model_name(self) -> str:
        return self.model
        
    async def get_completion(self, prompt: str) -> Union[AIResponse, ErrorResponse]:
        try:
            if not self.rate_limiter.check_limit():
                return ErrorResponse(
                    model=self.model,
                    provider="xai",
                    error="Rate limit exceeded"
                )
            
            logging.info(f"Making request to XAI API with prompt: {prompt[:100]}...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            logging.info(f"Received response from XAI API")
            
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            cost = (prompt_tokens * self.price_per_token["input"]) + \
                   (completion_tokens * self.price_per_token["output"])
            
            return AIResponse(
                content=response.choices[0].message.content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                model=self.model,
                cost=cost,
                provider="xai",
                error=None
            )
        except Exception as e:
            return ErrorResponse(
                model=self.model,
                provider="xai",
                error=str(e)
            )