"""
config.py

Central configuration for the README Generator.
All constants, template names, and settings live here.
No other module should define these values independently.
"""

from enum import Enum
from pathlib import Path

# ── Directory Paths ────────────────────────────────────────────────────────────

# The root of the project (one level above this file)
ROOT_DIR = Path(__file__).parent.parent

# Where template .md files are stored
TEMPLATES_DIR = ROOT_DIR / "templates"

# Where generated README files are saved by default

OUTPUT_DIR = ROOT_DIR / "output"

# ── Application Metadata ───────────────────────────────────────────────────────

APP_NAME = "README Generator"
APP_VERSION = "1.0.0"
OUTPUT_FILENAME = "README.md"

# ── Template Types ─────────────────────────────────────────────────────────────

class TemplateType(Enum):
    """
    Represents the supported project template types.

    Using an Enum instead of plain strings means:
    - Typos are caught immediately (invalid enum = error at startup)
    - IDE autocomplete works
    - You can iterate over all valid types easily
    """

    PYTHON = "python_project"
    ML = "ml_project"
    WEB = "web_project"
    JAVA = "java_project"

# Maps each TemplateType to its .md file in the templates/ directory
TEMPLATE_FILES = {
    TemplateType.PYTHON : "python_project.md",
    TemplateType.ML : "ml_project.md",
    TemplateType.WEB : "web_project.md",
    TemplateType.JAVA : "java_project.md",
}

# Human-readable labels for the terminal menu
TEMPLATE_DISPLAY_NAMES = {
    TemplateType.PYTHON : "Python Project",
    TemplateType.ML : "Machine Learning Project",
    TemplateType.WEB : "Web Project",
    TemplateType.JAVA : "Java Project",
}

# ── License Options ────────────────────────────────────────────────────────────

LICENSE_OPTIONS = [
    "MIT",
    "Apache 2.0",
    "GPL v3",
    "BSD 3-Clause",
    "None",
]

# ── Validation Rules ───────────────────────────────────────────────────────────

MAX_PROJECT_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
MIN_FIELD_LENGTH = 1