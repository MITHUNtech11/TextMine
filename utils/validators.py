import re


def is_valid_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def calculate_completeness(data: dict, required_fields: list, recommended_fields: list) -> float:
    """Calculate data completeness score"""
    total_fields = len(required_fields) + len(recommended_fields)
    filled_fields = sum(1 for field in required_fields + recommended_fields if data.get(field))
    return filled_fields / total_fields if total_fields > 0 else 0.0
