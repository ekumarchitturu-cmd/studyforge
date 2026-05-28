"""
Hybrid AI Model Configuration

This file controls the three-phase rollout strategy for StudyForge.
Edit these settings to control which phase is active.
"""

# =============================================================================
# PHASE CONFIGURATION
# =============================================================================

# Phase 1: Pure GPT-4 (Reputation Building)
# - First X users get pure GPT-4 for all plans
# - Goal: Build reputation, get testimonials, prove quality
# - Cost: Higher ($0.03 per plan) but worth it for early reviews
PHASE_1_THRESHOLD = 100  # First 100 users

# Phase 2: Hybrid Mode (Cost Optimization)
# - After PHASE_1_THRESHOLD users, switch to hybrid
# - First plan per user = GPT-4 (great first impression)
# - Subsequent plans = GPT-3.5 (save costs, user already converted)
# - Goal: Optimize costs while maintaining quality perception
PHASE_2_ACTIVE = True  # Set to False to disable

# Phase 3: Two-Tier Choice (Future Revenue Optimization)
# - Users can choose between two plan types:
#   * Quick Plan (GPT-3.5) - 20 credits - Faster, good quality
#   * Premium Plan (GPT-4) - 30 credits - Best quality
# - Goal: Price discrimination, let users choose quality vs cost
PHASE_3_ACTIVE = False  # Set to True when ready to launch

# =============================================================================
# CREDIT CONFIGURATION
# =============================================================================

# Initial credits for new users
INITIAL_CREDITS = 45  # Gives 1 full plan + 15 leftover (creates urgency!)

# Plan costs
STANDARD_PLAN_COST = 30  # Phase 1 & 2
QUICK_PLAN_COST = 20     # Phase 3: GPT-3.5
PREMIUM_PLAN_COST = 30   # Phase 3: GPT-4

# =============================================================================
# PRICING TIERS (For Credit Purchases)
# =============================================================================

PRICING_TIERS = [
    {
        "name": "Starter Pack",
        "credits": 50,
        "price": 1.00,
        "popular": False,
        "description": "Perfect to unlock your leftover credits!"
    },
    {
        "name": "Popular Pack",
        "credits": 100,
        "price": 2.00,
        "popular": True,
        "description": "Best value - Most popular choice!"
    },
    {
        "name": "Pro Pack",
        "credits": 300,
        "price": 5.00,
        "popular": False,
        "description": "For serious learners - Save 33%!"
    },
    {
        "name": "Ultimate Pack",
        "credits": 750,
        "price": 10.00,
        "popular": False,
        "description": "Maximum value - Save 46%!"
    }
]

# =============================================================================
# COST ESTIMATES (For Internal Tracking)
# =============================================================================

GPT4_COST_PER_PLAN = 0.03        # Approximate cost
GPT35_COST_PER_PLAN = 0.002      # Approximate cost

# =============================================================================
# FEATURE FLAGS
# =============================================================================

# Show phase status in sidebar (for transparency)
SHOW_PHASE_STATUS = True

# Show AI model used in success message
SHOW_MODEL_INFO = True

# Enable "leftover credits" messaging
ENABLE_LEFTOVER_MESSAGING = True

# =============================================================================
# PHASE TRANSITION GUIDE
# =============================================================================

"""
HOW TO TRANSITION BETWEEN PHASES:

STARTING (Launch Day):
- PHASE_1_THRESHOLD = 100
- PHASE_2_ACTIVE = True
- PHASE_3_ACTIVE = False
- Result: First 100 users get pure GPT-4

AFTER 100 USERS (Week 2-3):
- System automatically switches to Phase 2 (hybrid)
- New users: First plan = GPT-4, rest = GPT-3.5
- Cost savings: ~85% on subsequent plans!

LAUNCHING PHASE 3 (Month 2-3):
- Set PHASE_3_ACTIVE = True
- Update app.py to show plan type selector
- Users can choose Quick (20) or Premium (30) plans
- Revenue optimization: Some users prefer cheap, others premium

COST EXAMPLES:

Phase 1 (100 users, 1 plan each):
- 100 × $0.03 = $3.00
- Break-even: 2 paid customers ($4)

Phase 2 (100 users, avg 2 plans):
- First plans: 100 × $0.03 = $3.00
- Second plans: 100 × $0.002 = $0.20
- Total: $3.20 for 200 plans!
- Break-even: 2 paid customers ($4)

Phase 3 (100 users, 50/50 split):
- 50 Quick plans: 50 × $0.002 = $0.10
- 50 Premium plans: 50 × $0.03 = $1.50
- Total: $1.60
- Break-even: 1 paid customer ($2)

RECOMMENDED TIMELINE:

Week 1: Launch with Phase 1 (pure GPT-4)
- Focus on quality
- Get testimonials
- Cost: ~$3-5

Week 2-4: Phase 2 activates automatically
- Hybrid mode saves costs
- New users still get great first impression
- Cost: ~$5-10 for 200+ users

Month 2+: Launch Phase 3
- Give users choice
- Some pick cheap (profit!)
- Some pick premium (quality!)
- Cost: ~$10-20 for 500+ users
"""
