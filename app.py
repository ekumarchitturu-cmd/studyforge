import streamlit as st
from modules.database import Database
from modules.credit_manager import CreditManager
from modules.prompt_builder import build_universal_prompt
from modules.ai_agent import AIAgent
from modules.input_validator import InputValidator
from modules.auth import AuthManager
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

# Initialize authentication
AuthManager.init_session_state()

# Custom CSS - Futuristic Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main background with gradient */
    .main {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
    }

    /* Header with gradient text */
    .main-header {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            filter: drop-shadow(0 0 10px #667eea);
        }
        to {
            filter: drop-shadow(0 0 20px #764ba2);
        }
    }

    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #a0aec0;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* Glassmorphism credit box */
    .credit-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }

    .credit-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.5);
    }

    .credit-box h2 {
        color: #667eea;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }

    .credit-box p {
        color: #cbd5e0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .css-10trblm {
        color: #e2e8f0 !important;
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select,
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus,
    .stNumberInput input:focus {
        border: 1px solid #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        transform: scale(1.02);
    }

    /* Primary button - Futuristic glow */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        padding: 1rem 2rem;
        border-radius: 15px;
        border: none;
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6);
    }

    .stButton>button:active {
        transform: translateY(-1px);
    }

    /* Success/Error/Warning messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem 1.5rem;
    }

    /* Form sections */
    .css-1kyxreq {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
    }

    /* Headers and labels */
    h1, h2, h3 {
        color: #e2e8f0 !important;
        font-weight: 700;
    }

    label, .css-81oif8 {
        color: #cbd5e0 !important;
        font-weight: 500;
        font-size: 0.95rem;
    }

    /* Radio buttons */
    .stRadio > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 5px;
        transition: all 0.3s ease;
    }

    .stRadio > label:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
    }

    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
    }

    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Phase status badge */
    .phase-badge {
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Pricing cards */
    .pricing-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
    }

    .pricing-card:hover {
        transform: translateX(10px);
        border-color: #667eea;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main > div {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 PlanMind</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Study Plans • Personalized • Adaptive • Smart</div>', unsafe_allow_html=True)

# Sidebar for authentication and user info
with st.sidebar:
    if not AuthManager.is_authenticated():
        # Show login/signup form
        st.markdown("## 🔐 Authentication")

        if st.session_state.get('show_signup', False):
            # SIGNUP FORM
            st.markdown("### Create Account")

            with st.form("signup_form"):
                signup_email = st.text_input("📧 Email", placeholder="your@email.com")
                signup_password = st.text_input("🔒 Password", type="password", placeholder="Min 8 chars, 1 upper, 1 number")
                signup_confirm = st.text_input("🔒 Confirm Password", type="password")
                signup_submit = st.form_submit_button("Create Account", use_container_width=True)

                if signup_submit:
                    # Validate email
                    if not AuthManager.validate_email(signup_email):
                        st.error("❌ Invalid email format")
                    # Check passwords match
                    elif signup_password != signup_confirm:
                        st.error("❌ Passwords don't match")
                    else:
                        # Validate password strength
                        is_valid, msg = AuthManager.validate_password(signup_password)
                        if not is_valid:
                            st.error(f"❌ {msg}")
                        else:
                            # Create user
                            success, message = db.create_user(signup_email, signup_password)
                            if success:
                                st.success(f"✅ {message}")
                                st.info("👉 Please login with your credentials")
                                AuthManager.toggle_signup()
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")

            if st.button("Already have an account? Login", use_container_width=True):
                AuthManager.toggle_signup()
                st.rerun()

        else:
            # LOGIN FORM
            st.markdown("### Login")

            with st.form("login_form"):
                login_email = st.text_input("📧 Email", placeholder="your@email.com")
                login_password = st.text_input("🔒 Password", type="password")
                login_submit = st.form_submit_button("Login", use_container_width=True)

                if login_submit:
                    # Validate email format
                    if not AuthManager.validate_email(login_email):
                        st.error("❌ Invalid email format")
                    else:
                        # Verify credentials
                        success, message = db.verify_password(login_email, login_password)
                        if success:
                            AuthManager.login(login_email)
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")

            if st.button("Don't have an account? Sign Up", use_container_width=True):
                AuthManager.toggle_signup()
                st.rerun()

    else:
        # User is authenticated - show their info
        email = AuthManager.get_current_user()
        st.markdown("## 👤 User Account")
        st.markdown(f"**Logged in as:**\n`{email}`")

        if st.button("🚪 Logout", use_container_width=True):
            AuthManager.logout()
            st.rerun()

        # Get user info
        user = db.get_user_by_email(email)
        if user:
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
if not AuthManager.is_authenticated():
    # Welcome screen - Not logged in
    st.markdown("## 👋 Welcome to PlanMind!")
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

    **👈 Sign up / Login in the sidebar to begin!**
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
