import time

class RateLimiter:
    """
    Rate limiter that works in seconds.
    rate_limit_window parameter should be provided in seconds.
    """
    def __init__(self, rate_limit: int, rate_limit_window: int):
        """
        Initialize rate limiter.
        Args:
            rate_limit: Maximum number of calls allowed in the window
            rate_limit_window: Time window in seconds
        """
        self.rate_limit = rate_limit
        self.rate_limit_window = rate_limit_window
        self.last_called = 0
        self.call_count = 0

    def check_limit(self) -> bool:
        current_time = time.time()
        
        if (current_time - self.last_called) > self.rate_limit_window:
            self.call_count = 0
            self.last_called = current_time
        
        if self.call_count >= self.rate_limit:
            return False
            
        self.call_count += 1
        return True