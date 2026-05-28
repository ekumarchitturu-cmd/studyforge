from modules.database import Database

class CreditManager:
    def __init__(self):
        self.db = Database()
        self.PLAN_COST = 30
        self.INITIAL_CREDITS = 100

    def get_credits(self, email):
        """Get user's current credit balance"""
        return self.db.get_credits(email)

    def has_enough_credits(self, email, required=None):
        """Check if user has enough credits"""
        if required is None:
            required = self.PLAN_COST
        return self.get_credits(email) >= required

    def deduct_credits(self, email):
        """Deduct credits for generating a plan"""
        self.db.deduct_credits(email, self.PLAN_COST)

    def add_credits(self, email, amount):
        """Add credits (for purchases)"""
        self.db.add_credits(email, amount)
