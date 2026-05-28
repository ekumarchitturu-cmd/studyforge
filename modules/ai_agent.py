import openai
import os
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in .env file")
        openai.api_key = self.api_key

        # Phase thresholds
        self.PHASE_1_THRESHOLD = 100  # First 100 users get pure GPT-4
        self.PHASE_2_ACTIVE = True    # Hybrid mode after 100 users
        self.PHASE_3_ACTIVE = False   # Two-tier choice (future)

    def select_model(self, total_users, user_plan_count, plan_type="standard"):
        """
        Smart model selection based on phase and user status

        PHASE 1 (First 100 users): Pure GPT-4 for reputation building
        PHASE 2 (After 100 users): Hybrid
            - First plan per user = GPT-4 (great first impression)
            - Subsequent plans = GPT-3.5 (cost optimization)
        PHASE 3 (Future): Two-tier choice
            - Quick Plan (GPT-3.5) - 20 credits
            - Premium Plan (GPT-4) - 30 credits
        """

        # PHASE 3: Two-tier system (if implemented)
        if self.PHASE_3_ACTIVE:
            if plan_type == "quick":
                return "gpt-3.5-turbo", 20  # Cheaper option
            elif plan_type == "premium":
                return "gpt-4", 30  # Premium option

        # PHASE 1: First 100 users - Pure GPT-4 (reputation building)
        if total_users < self.PHASE_1_THRESHOLD:
            return "gpt-4", 30

        # PHASE 2: Hybrid mode (after 100 users)
        if self.PHASE_2_ACTIVE:
            if user_plan_count == 0:
                # First plan = GPT-4 (impress them!)
                return "gpt-4", 30
            else:
                # Subsequent plans = GPT-3.5 (save costs)
                return "gpt-3.5-turbo", 30

        # Default fallback
        return "gpt-4", 30

    def generate_study_plan(self, prompt, total_users=0, user_plan_count=0, plan_type="standard"):
        """
        Call OpenAI API to generate study plan with smart model selection

        Args:
            prompt: The study plan prompt
            total_users: Total number of users in system (for phase detection)
            user_plan_count: Number of plans this user has generated (for hybrid logic)
            plan_type: "standard", "quick", or "premium" (for Phase 3)

        Returns:
            tuple: (plan_content, model_used, cost_estimate)
        """
        try:
            # Smart model selection
            model, credits_cost = self.select_model(total_users, user_plan_count, plan_type)

            # Cost estimation (for logging/tracking)
            if model == "gpt-4":
                estimated_cost = 0.03  # Approximate
            else:  # gpt-3.5-turbo
                estimated_cost = 0.002

            # Call OpenAI API
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational consultant who creates personalized, detailed study plans for students of all ages and fields."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )

            plan_content = response.choices[0].message.content

            # Add metadata footer (helpful for user)
            phase_info = self._get_phase_info(total_users, user_plan_count, model)
            footer = f"\n\n---\n💡 {phase_info}"

            return plan_content + footer, model, estimated_cost

        except Exception as e:
            return f"Error generating study plan: {str(e)}", None, 0

    def _get_phase_info(self, total_users, user_plan_count, model_used):
        """Generate helpful message based on current phase"""

        if total_users < self.PHASE_1_THRESHOLD:
            return f"🎉 Early Adopter #{total_users}! You're using our premium GPT-4 model. Thank you for being an early user!"

        elif user_plan_count == 0 and model_used == "gpt-4":
            return "✨ Your first plan uses our premium GPT-4 model for the best quality!"

        elif model_used == "gpt-3.5-turbo":
            return "⚡ Generated with GPT-3.5 for fast, quality results!"

        else:
            return "Powered by advanced AI technology"

    def get_phase_status(self, total_users):
        """
        Get current phase information (for admin/dashboard)
        """
        if total_users < self.PHASE_1_THRESHOLD:
            return {
                "phase": 1,
                "description": "Pure GPT-4 - Reputation Building",
                "users_until_next_phase": self.PHASE_1_THRESHOLD - total_users,
                "model": "gpt-4",
                "strategy": "All plans use GPT-4 for best quality"
            }
        elif self.PHASE_2_ACTIVE and not self.PHASE_3_ACTIVE:
            return {
                "phase": 2,
                "description": "Hybrid Mode - Cost Optimization",
                "model": "GPT-4 (first) + GPT-3.5 (subsequent)",
                "strategy": "First plan = GPT-4, Others = GPT-3.5"
            }
        elif self.PHASE_3_ACTIVE:
            return {
                "phase": 3,
                "description": "Two-Tier Choice",
                "model": "User selects Quick (GPT-3.5) or Premium (GPT-4)",
                "strategy": "Quick: 20 credits | Premium: 30 credits"
            }
        else:
            return {
                "phase": 0,
                "description": "Default",
                "model": "gpt-4",
                "strategy": "Standard operation"
            }
