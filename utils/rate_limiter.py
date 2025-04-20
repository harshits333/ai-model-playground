import time

class RateLimiter:
    """
    Rate limiter that works in seconds.
    rate_limit_window parameter should be provided in seconds.
    """
    _instances = {}
    
    def __init__(self, entity: str, rate_limit: int, rate_limit_window: int):
        """
        Initialize rate limiter.
        Args:
            rate_limit: Maximum number of calls allowed in the window
            rate_limit_window: Time window in seconds
        """
        self.rate_limit = rate_limit
        self.rate_limit_window = rate_limit_window
        self.entity = entity
        if self.entity not in RateLimiter._instances:
            RateLimiter._instances[self.entity] = {'last_called': 0, 'call_count': 0}

    def check_limit(self) -> bool:
        current_time = time.time()
        instance_data = RateLimiter._instances[self.entity]
        
        if (current_time - instance_data['last_called']) > self.rate_limit_window:
            instance_data['call_count'] = 0
            instance_data['last_called'] = current_time
        
        if instance_data['call_count'] >= self.rate_limit:
            return False
            
        instance_data['call_count'] += 1
        return True