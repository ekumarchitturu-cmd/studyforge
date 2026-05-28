import re

class InputValidator:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_all_inputs(user_data):
        """Validate all user inputs"""
        errors = []

        # Email
        if not user_data.get('email'):
            errors.append("Email is required")
        elif not InputValidator.validate_email(user_data['email']):
            errors.append("Invalid email format")

        # Subject
        if not user_data.get('subject') or len(user_data['subject'].strip()) < 3:
            errors.append("Subject must be at least 3 characters")

        # Goal
        if not user_data.get('goal') or len(user_data['goal'].strip()) < 10:
            errors.append("Please describe your goal (at least 10 characters)")

        # Daily time
        if not user_data.get('daily_time'):
            errors.append("Daily study time is required")

        # Duration
        if not user_data.get('duration') or user_data['duration'] < 1:
            errors.append("Duration must be at least 1 week")

        return errors
