from modules.database import Database

class CreditManager:
    def __init__(self):
        self.db = Database()
        self.STANDARD_PLAN_COST = 30  # Phase 1 & 2
        self.QUICK_PLAN_COST = 20     # Phase 3: GPT-3.5
        self.PREMIUM_PLAN_COST = 30   # Phase 3: GPT-4
        self.INITIAL_CREDITS = 45     # New users get 45 credits

    def get_credits(self, email):
        """Get user's current credit balance"""
        return self.db.get_credits(email)

    def has_enough_credits(self, email, plan_type="standard"):
        """
        Check if user has enough credits

        Args:
            email: User email
            plan_type: "standard" (30), "quick" (20), or "premium" (30)
        """
        current_credits = self.get_credits(email)

        if plan_type == "quick":
            required = self.QUICK_PLAN_COST
        elif plan_type == "premium":
            required = self.PREMIUM_PLAN_COST
        else:  # standard
            required = self.STANDARD_PLAN_COST

        return current_credits >= required

    def get_plan_cost(self, plan_type="standard"):
        """Get cost for a specific plan type"""
        if plan_type == "quick":
            return self.QUICK_PLAN_COST
        elif plan_type == "premium":
            return self.PREMIUM_PLAN_COST
        else:
            return self.STANDARD_PLAN_COST

    def deduct_credits(self, email, plan_type="standard"):
        """
        Deduct credits for generating a plan

        Args:
            email: User email
            plan_type: "standard", "quick", or "premium"
        """
        cost = self.get_plan_cost(plan_type)
        self.db.deduct_credits(email, cost)

    def add_credits(self, email, amount):
        """Add credits (for purchases)"""
        self.db.add_credits(email, amount)

    def get_pricing_tiers(self):
        """
        Get pricing information for all tiers

        Returns list of pricing packages
        """
        return [
            {
                "name": "Starter Pack",
                "credits": 50,
                "plans": "1-2 plans",
                "price": 1.00,
                "price_per_plan": 0.50,
                "savings": None,
                "popular": False
            },
            {
                "name": "Popular Pack",
                "credits": 100,
                "plans": "3-5 plans",
                "price": 2.00,
                "price_per_plan": 0.40,
                "savings": "20%",
                "popular": True
            },
            {
                "name": "Pro Pack",
                "credits": 300,
                "plans": "10-15 plans",
                "price": 5.00,
                "price_per_plan": 0.33,
                "savings": "33%",
                "popular": False
            },
            {
                "name": "Ultimate Pack",
                "credits": 750,
                "plans": "25-37 plans",
                "price": 10.00,
                "price_per_plan": 0.27,
                "savings": "46%",
                "popular": False
            }
        ]

    def calculate_remaining_plans(self, email, plan_type="standard"):
        """
        Calculate how many plans user can still generate

        Returns:
            tuple: (can_generate_count, leftover_credits)
        """
        credits = self.get_credits(email)
        cost = self.get_plan_cost(plan_type)

        plans_possible = credits // cost
        leftover = credits % cost

        return plans_possible, leftover

    def get_credit_warning_message(self, email):
        """
        Get appropriate warning/info message based on credit balance

        Returns:
            tuple: (message, severity)  severity: "info", "warning", "danger"
        """
        credits = self.get_credits(email)
        plans_remaining, leftover = self.calculate_remaining_plans(email)

        if credits >= 90:
            return f"You have {credits} credits ({plans_remaining} plans). Plenty remaining! 🎉", "info"

        elif credits >= 60:
            return f"You have {credits} credits ({plans_remaining} plans remaining).", "info"

        elif credits >= 30:
            return f"You have {credits} credits ({plans_remaining} plan remaining). Consider buying more!", "warning"

        elif leftover > 0:
            return f"⚠️ You have {credits} credits (not enough for a full plan). Buy {30 - leftover} more credits to unlock!", "warning"

        else:
            return f"❌ Out of credits! You need {30} credits to generate a plan. Buy credits below.", "danger"
