import streamlit as st
from modules.database import Database
from modules.credit_manager import CreditManager
from modules.prompt_builder import build_universal_prompt
from modules.ai_agent import AIAgent
from modules.input_validator import InputValidator
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="StudyForge - AI Study Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    db = Database()
    cm = CreditManager()
    ai = AIAgent()
    return db, cm, ai

db, credit_manager, ai_agent = init_components()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .credit-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎓 StudyForge</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personalized AI Study Planner - For Every Student, Every Subject</div>', unsafe_allow_html=True)

# Sidebar for user info and credits
with st.sidebar:
    st.markdown("## 👤 User Account")

    email = st.text_input("📧 Your Email:", placeholder="student@example.com", key="email_input")

    if email:
        # Validate email
        if not InputValidator.validate_email(email):
            st.error("⚠️ Please enter a valid email address")
        else:
            # Get user info
            user = db.get_user(email)
            credits = credit_manager.get_credits(email)

            # Display credits
            st.markdown("---")
            st.markdown("### 💎 Your Credits")
            st.markdown(f'<div class="credit-box"><h2>{credits}</h2><p>credits remaining</p></div>', unsafe_allow_html=True)

            # Smart credit warning
            warning_msg, severity = credit_manager.get_credit_warning_message(email)
            plans_remaining, leftover = credit_manager.calculate_remaining_plans(email)

            if leftover > 0:
                st.warning(f"💡 You have {leftover} leftover credits! Buy just {30 - leftover} more to unlock another plan!")
            elif credits < 30:
                st.error(warning_msg)
            elif credits < 60:
                st.warning(warning_msg)

            st.markdown("---")
            st.markdown("### 📊 Account Stats")
            plans_generated = user[4] if user else 0
            created_at = user[3] if user else datetime.now().isoformat()
            st.metric("Plans Generated", plans_generated)
            st.metric("Member Since", datetime.fromisoformat(created_at).strftime("%b %d, %Y"))

            # Get total users for phase display
            total_users = db.get_total_users()
            phase_info = ai_agent.get_phase_status(total_users)

            st.markdown("---")
            st.markdown("### 🚀 Platform Status")
            st.info(f"**Phase {phase_info['phase']}:** {phase_info['description']}\n\n**Strategy:** {phase_info['strategy']}")

            st.markdown("---")
            st.markdown("### 💰 Buy More Credits")

            pricing_tiers = credit_manager.get_pricing_tiers()
            for tier in pricing_tiers:
                badge = "⭐ POPULAR" if tier['popular'] else ""
                savings = f"(Save {tier['savings']}!)" if tier['savings'] else ""
                st.info(f"**{tier['name']}** {badge}\n- {tier['credits']} credits ({tier['plans']}) - ${tier['price']:.2f} {savings}")

            if st.button("💳 Buy Credits"):
                st.info("💡 Payment integration coming soon! Contact: support@studyforge.com")

# Main content
if not email or not InputValidator.validate_email(email):
    # Welcome screen
    st.markdown("## 👋 Welcome to StudyForge!")
    st.markdown("""
    StudyForge creates personalized study plans using AI, tailored to:
    - **Your field** (Engineering, Medicine, Law, Commerce, Design, etc.)
    - **Your level** (Beginner to Advanced)
    - **Your goals** (Exams, Jobs, Projects, Hobbies)
    - **Your schedule** (Daily time and duration)

    ### ✨ Features:
    - 🎯 Adaptive plans for every student type
    - 📚 Field-specific resources and study techniques
    - ⏰ Daily breakdown with time estimates
    - ✅ Checkboxes to track progress
    - 📥 Download your plan

    ### 🎉 Special Launch Offer:
    - **Get 45 FREE credits** (1 full study plan!)
    - Early adopters get **premium GPT-4 model**
    - Leftover credits? Buy just what you need!

    ### 🚀 Get Started:
    1. Enter your email in the sidebar → Get 45 credits instantly
    2. Fill out the form below
    3. Generate your personalized plan in 30 seconds!

    **👈 Enter your email in the sidebar to begin!**
    """)

else:
    # User is logged in, show the form
    credits = credit_manager.get_credits(email)

    if credits < 30:
        st.error("❌ Insufficient credits! You need 30 credits to generate a study plan.")
        st.info("💡 Please contact support@studyforge.com to purchase more credits.")
    else:
        st.markdown("## 📝 Create Your Personalized Study Plan")
        st.markdown(f"**This will cost 30 credits. You have {credits} credits.**")

        with st.form("study_plan_form"):
            st.markdown("### 👤 About You")

            col1, col2 = st.columns(2)

            with col1:
                age = st.selectbox(
                    "Age Group",
                    ["10-14 years (School)", "15-18 years (High School)", "19-25 years (College)", "26+ years (Professional)"]
                )

                education = st.selectbox(
                    "Education Level",
                    ["School (8th-10th)", "Intermediate/+2 (11th-12th)", "College (Undergraduate)", "Graduate (Masters/PhD)", "Working Professional"]
                )

                location = st.text_input("Location (City/State/Country)", placeholder="e.g., Bangalore, Karnataka")

            with col2:
                language = st.selectbox(
                    "Preferred Language",
                    ["English", "Telugu", "Hindi", "Tamil", "Mixed (English + Regional)"]
                )

                field = st.selectbox(
                    "Your Field/Stream",
                    [
                        "Engineering (CSE, ECE, Mech, etc.)",
                        "Medicine (MBBS, BDS, Nursing, Pharmacy)",
                        "Law (LLB, LLM, Judiciary)",
                        "Commerce/Finance (CA, CS, CMA, B.Com)",
                        "Arts/Humanities (History, Literature, etc.)",
                        "Science (BSc Physics, Chemistry, Biology)",
                        "Design (UI/UX, Graphic, Fashion, Architecture)",
                        "Agriculture/Veterinary",
                        "Management (MBA, BBA)",
                        "Other"
                    ]
                )

            st.markdown("---")
            st.markdown("### 🎯 Your Learning Goal")

            subject = st.text_input(
                "What do you want to learn?",
                placeholder="e.g., Python Programming, Constitutional Law, Anatomy, Financial Management"
            )

            level = st.radio(
                "Your current knowledge level",
                ["Complete Beginner (never studied this)", "Beginner (know basics)", "Intermediate (some experience)", "Advanced (want to master it)"],
                horizontal=True
            )

            goal = st.text_area(
                "Your specific goal (be detailed)",
                placeholder="e.g., Get a job as Python developer, Pass CA Inter exam, Prepare for NEET PG, Build portfolio for internship",
                height=100
            )

            reason = st.selectbox(
                "Why are you learning this?",
                ["School exam preparation", "College/University exam", "Get job/internship", "Career change", "Personal project/hobby", "Competitive exam (NEET, JEE, UPSC, etc.)", "Research/Advanced study"]
            )

            st.markdown("---")
            st.markdown("### ⏰ Study Schedule")

            col3, col4 = st.columns(2)

            with col3:
                daily_time = st.text_input(
                    "Daily study time available",
                    placeholder="e.g., 2 hours, 45 minutes, 3-4 hours"
                )

            with col4:
                duration = st.number_input(
                    "Duration (in weeks)",
                    min_value=1,
                    max_value=52,
                    value=4,
                    help="How many weeks until your goal/exam?"
                )

            st.markdown("---")

            # Submit button
            submitted = st.form_submit_button("🚀 Generate My Study Plan (30 credits)", use_container_width=True)

        # Handle form submission
        if submitted:
            # Validate inputs
            user_data = {
                'email': email,
                'age': age,
                'education': education,
                'location': location,
                'language': language,
                'field': field,
                'subject': subject,
                'level': level,
                'goal': goal,
                'reason': reason,
                'daily_time': daily_time,
                'duration': duration
            }

            errors = InputValidator.validate_all_inputs(user_data)

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Generate study plan
                with st.spinner("🤖 Generating your personalized study plan... This may take 20-30 seconds."):
                    try:
                        # Build prompt
                        prompt = build_universal_prompt(user_data)

                        # Get user's plan count (for hybrid logic)
                        user_plan_count = user[4]  # total_plans_generated

                        # Get total users (for phase detection)
                        total_users = db.get_total_users()

                        # Call AI with hybrid system
                        study_plan, model_used, estimated_cost = ai_agent.generate_study_plan(
                            prompt,
                            total_users=total_users,
                            user_plan_count=user_plan_count
                        )

                        # Deduct credits
                        credit_manager.deduct_credits(email)

                        # Save to database
                        db.save_plan(email, subject, field, level, study_plan)

                        # Display success with model info
                        if model_used == "gpt-4":
                            st.success("✅ Your personalized study plan is ready! (Generated with premium GPT-4 model)")
                        else:
                            st.success("✅ Your personalized study plan is ready! (Generated with fast GPT-3.5 model)")

                        # Display the plan
                        st.markdown("---")
                        st.markdown("## 📚 Your Study Plan")
                        st.markdown(study_plan)

                        # Download button
                        st.download_button(
                            label="📥 Download as Text File",
                            data=study_plan,
                            file_name=f"studyforge_{subject.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )

                        # Show updated credits
                        new_credits = credit_manager.get_credits(email)
                        plans_remaining, leftover = credit_manager.calculate_remaining_plans(email)

                        if leftover > 0:
                            st.info(f"💎 Credits remaining: {new_credits} ({leftover} leftover - buy {30-leftover} more to unlock another plan!)")
                        else:
                            st.info(f"💎 Credits remaining: {new_credits} ({plans_remaining} plans remaining)")

                        # Generate another button
                        if new_credits >= 30:
                            if st.button("🔄 Generate Another Plan"):
                                st.rerun()
                        else:
                            if leftover > 0:
                                st.warning(f"⚠️ You have {leftover} leftover credits! Buy just {30-leftover} more credits to generate another plan.")
                            else:
                                st.warning("⚠️ You don't have enough credits for another plan. Please purchase more credits.")

                    except Exception as e:
                        st.error(f"❌ Error generating study plan: {str(e)}")
                        st.info("💡 Please try again or contact support if the issue persists.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Made with ❤️ by StudyForge | <a href="mailto:support@studyforge.com">Contact Support</a></p>
    <p style="font-size: 0.8rem;">Note: AI-generated plans are suggestions. Always verify with your teachers/professors.</p>
</div>
""", unsafe_allow_html=True)
