"""
template_engine.py

Responsible for loading Jinja2 templates and rendering them
with user-supplied data.

This module is purely transformational:
    - Input:  a data dictionary + a TemplateType
    - Output: a rendered Markdown string

No I/O happens here. No user interaction. No file writing.
That separation is intentional — it makes this module
independently testable and reusable.
"""

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from readme_generator.config import TEMPLATES_DIR, TEMPLATE_FILES, TemplateType

def _create_environment() -> Environment:
    """
    Creates and configures the Jinja2 environment.

    The Environment is the core Jinja2 object. It holds:
      - Where to look for templates (FileSystemLoader)
      - How to handle whitespace (trim_blocks, lstrip_blocks)

    trim_blocks:   removes the newline after a block tag like {% for %}
    lstrip_blocks: removes leading whitespace before block tags

    Without these two settings, Jinja2 leaves blank lines in the
    output wherever your {% for %} and {% if %} tags sit.
    The generated README would have ugly gaps between every bullet.
    """

    return Environment(
        loader = FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks = True,
        lstrip_blocks = True,
        keep_trailing_newline = True,
    )

# Single shared environment — created once, reused for every render
_env = _create_environment()

# ── Public API ─────────────────────────────────────────────────────────────────
def render_template(template_type: TemplateType, data: dict) -> str:
    """
    Renders a README template with the provided data.

    Args:
        template_type: A TemplateType enum value identifying which
                       template to use.
        data:          A dictionary of variables the template expects.
                       Keys must match the {{ variable }} names in the
                       template file exactly.

    Returns:
        A fully rendered Markdown string.

    Raises:
        TemplateNotFound:  If the template file is missing from disk.
        ValueError:        If template_type is not a valid TemplateType.
        KeyError:          If a required variable is missing from data.
    """

    if not isinstance(template_type, TemplateType):
        raise ValueError(
            f"{template_type} must be a {TemplateType} enum"
            f"Got: {type(template_type).__name__}"
        )
    
    template_filename = TEMPLATE_FILES.get(template_type)

    try:
        template = _env.get_template(template_filename)
    except TemplateNotFound:
        raise TemplateNotFound(
            f"Template file '{template_filename}' not found"
            f"Expected location: {TEMPLATES_DIR / template_filename}"
        )
    
    rendered = template.render(**data)
    return rendered

def get_available_templates() -> list[dict]:
    """
    Returns a list of available templates with their display info.

    Each item is a dict with:
        - 'type':  the TemplateType enum value
        - 'label': the human-readable display name

    This is used by input_handler.py to build the selection menu
    without that module needing to know about TEMPLATE_DISPLAY_NAMES.
    """
    from readme_generator.config import TEMPLATE_DISPLAY_NAMES

    return [
        {"type": template_type, "label": label}
        for template_type, label in TEMPLATE_DISPLAY_NAMES.items()
    ]
