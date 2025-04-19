from typing import Dict

class CostCalculator:
    def __init__(self):
        self.pricing = {
            "gpt-4o": {"input": 0.000005, "output": 0.000015},
            "claude-3-opus-20240229": {"input": 0.000015, "output": 0.000075},
            "xai-model-1": {"input": 0.00001, "output": 0.00003}
        }

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for a given model and token counts.
        
        Args:
            model: The model name (e.g. 'gpt-4o')
            prompt_tokens: Number of tokens in the prompt
            completion_tokens: Number of tokens in the completion
            
        Returns:
            Estimated cost in USD
        """
        if model not in self.pricing:
            return 0.0
            
        input_cost = prompt_tokens * self.pricing[model]["input"]
        output_cost = completion_tokens * self.pricing[model]["output"]
        return input_cost + output_cost