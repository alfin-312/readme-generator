"""
test_validator.py

Unit tests for the validator module.
Each test is small, focused, and tests one specific behaviour.
"""

import pytest
from readme_generator.validator import(
    validate_project_name,
    validate_description,
    validate_github_username,
    validate_non_empty_list,
    validate_required_field,
    sanitize_list_input,
    sanitize_multiline_input,
)

# ── validate_project_name ──────────────────────────────────────────────────────

class TestValidateProjectName:

    def test_valid_name_passes(self):
        valid, error = validate_project_name("My Project")
        assert valid is True
        assert error == ""

    def test_valid_name_fails(self):
        valid, error = validate_project_name("")
        assert valid is False
        assert "empty" in error.lower()

    def test_whitespace_only_fails(self):
        valid, error = validate_description("    ")
        assert valid is False
        assert "empty" in error.lower()

    def test_name_at_max_length_passes(self):
        name = "a" * 100
        valid, error = validate_project_name(name)
        assert valid is True
    
    def test_name_over_max_length_fails(self):
        name = "a" * 101
        valid, error = validate_project_name(name)
        assert valid is False
        assert "100" in error
         
# ── validate_github_username ───────────────────────────────────────────────────

class TestValidateGithubUsername:

    def test_valid_username_passes(self):
        valid, error = validate_github_username("alfin-312")
        assert valid is True
    
    def test_valid_username_fails(self):
        valid, error = validate_github_username("")
        assert valid is False
    
    def test_username_starting_with_hyphen_fails(self):
        valid, error = validate_github_username("-alfin")
        assert valid is False
        assert "hyphen" in error.lower()

    def test_username_ending_with_hyphen_fails(self):
        valid, error = validate_github_username("badname-")
        assert valid is False
        assert "hyphen" in error.lower()

    def test_username_with_special_chars_fails(self):
        valid, error = validate_github_username("bad_name!")
        assert valid is False
        assert "letters" in error.lower()

    def test_username_over_39_chars_fails(self):
        valid, error = validate_github_username("a" * 40)
        assert valid is False
        assert "39" in error
    
# ── validate_non_empty_list ────────────────────────────────────────────────────

class TestValidateNonEmptyList:

    def test_valid_list_passes(self):
        valid, error = validate_non_empty_list(["Python", "Flask"])
        assert valid is True

    def test_empty_list_fails(self):
        valid, error = validate_non_empty_list([])
        assert valid is False

    def test_list_of_blank_strings_fails(self):
        valid, error = validate_non_empty_list(["  ", ""])
        assert valid is False

# ── sanitize_list_input ────────────────────────────────────────────────────────

class TestSanitizeListInput:

    def test_comma_separated_splits_correctly(self):
        result = sanitize_list_input("Python, Flask, SQLite")
        assert result == ["Python", "Flask", "SQLite"]

    def test_extra_whitespace_is_stripped(self):
        result = sanitize_list_input("  Python ,  Flask  ")
        assert result == ["Python", "Flask"]

    def test_empty_items_are_removed(self):
        result = sanitize_list_input("Python,,Flask")
        assert result == ["Python", "Flask"]

    def test_empty_string_returns_empty_list(self):
        result = sanitize_list_input("")
        assert result == []

# ── sanitize_multiline_input ───────────────────────────────────────────────────

class TestSanitizeMultilineInput:

    def test_newline_separated_splits_correctly(self):
        result = sanitize_multiline_input("git clone repo\npip install -r requirements.txt")
        assert result == ["git clone repo", "pip install -r requirements.txt"]

    def test_blank_lines_are_removed(self):
        result = sanitize_multiline_input("step one\n\nstep two")
        assert result == ["step one", "step two"]

    def test_empty_string_returns_empty_list(self):
        result = sanitize_multiline_input("")
        assert result == []