"""
validator.py

All input validation logic for the README Generator.
Every function here is a pure function — it takes a value,
returns a result, and has no side effects.

This module is intentionally independent — it imports nothing
from the rest of the project except config constants.
"""

from readme_generator.config import(
    MAX_PROJECT_NAME_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MIN_FIELD_LENGTH,
)

# ── Core Validation Helpers ────────────────────────────────────────────────────
def is_empty(value: str) -> bool:
    """Returns True if the value is blank or whitespace-only."""
    return len(value.strip()) < MIN_FIELD_LENGTH

def is_too_long(value: str, max_length: int) -> bool:
    """Returns True if the value exceeds the allowed length."""
    return len(value.strip()) > max_length

# ── Field-Specific Validators ──────────────────────────────────────────────────
def validate_project_name(name: str) -> tuple[bool, str]:
    """
    Validates the project name.

    Returns a tuple: (is_valid, error_message)
    If valid, error_message is an empty string.

    This pattern — returning (bool, message) — is cleaner than
    raising exceptions for expected user errors like empty input.
    """
    if is_empty(name):
        return False, "Project name cannot be empty."
    
    if is_too_long(name, MAX_PROJECT_NAME_LENGTH):
        return False, f"Project name must be under {MAX_PROJECT_NAME_LENGTH} characters."
    
    return True, ""

def validate_description(descrption: str) -> tuple[bool, str]:
    """Validates the project description."""
    if is_empty(descrption):
        return False, "Description cannot be empty."
    
    if is_too_long(descrption, MAX_DESCRIPTION_LENGTH):
        return False, f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters."
    
    return True, ""

def validate_github_username(username: str) -> tuple[bool, str]:
    """
    Validates a GitHub username.

    GitHub rules:
    - May only contain alphanumeric characters or hyphens
    - Cannot start or end with a hyphen
    - Maximum 39 characters
    """

    if is_empty(username):
        return False, "GitHub Username cannot be empty."
    
    username = username.strip()

    if len(username) > 39:
        return False, "GitHub username must be 39 characters or fewer."
    
    if username.startswith("-") or username.endswith("-"):
        return False, "GitHub username cannot start or end with a hyphen."
    
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")
    if not all(char in allowed for char in username):
        return False, "GitHub username may only contain letters, numbers, and hyphens."
    
    return True, ""

def validate_non_empty_list(items: list[str]) -> tuple[bool, str]:
    """
    Validates that a list has at least one non-empty item.
    Used for tech stack, features, installation steps.
    """
    if not items:
        return False, "Please provide atleast one item."
    
    cleaned = [item.strip() for item in items if item.strip()]
    if not cleaned:
        return False, "Please provide atleast ne non_empty item."
    
    return True, ""

def validate_required_field(value: str, field_name: str) -> tuple[bool,str]:
    """
    Generic validator for any required text field.
    Used for fields that just need to be non-empty.
    """
    if is_empty(value):
        return False, f"{field_name} cannot be empty."
    
    return True, ""

# ── Sanitizers ─────────────────────────────────────────────────────────────────

def sanitize_list_input(raw_input: str) -> list[str]:
    """
    Converts a comma-separated string into a clean list.

    Example:
        "Python, Flask , SQLite" → ["Python", "Flask", "SQLite"]
    """
    return [item.strip() for item in raw_input.split(",") if item.strip()]

def sanitize_multiline_input(raw_input: str) -> list[str]:
    """
    Converts a newline-separated string into a clean list.
    Used for installation steps entered one per line.

    Example:
        "git clone ...\npip install ..." → ["git clone ...", "pip install ..."]
    """
    return [line.strip() for line in raw_input.splitlines() if line.strip()]


