import streamlit as st
import re

class AuthManager:
    """Handle user authentication and session management"""

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        """
        Validate password strength:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"

        return True, "Password is strong"

    @staticmethod
    def init_session_state():
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        if 'show_signup' not in st.session_state:
            st.session_state.show_signup = False

    @staticmethod
    def login(email):
        """Log in user"""
        st.session_state.authenticated = True
        st.session_state.user_email = email

    @staticmethod
    def logout():
        """Log out user"""
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.show_signup = False

    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)

    @staticmethod
    def get_current_user():
        """Get current logged-in user email"""
        return st.session_state.get('user_email', None)

    @staticmethod
    def toggle_signup():
        """Toggle between login and signup"""
        st.session_state.show_signup = not st.session_state.get('show_signup', False)
