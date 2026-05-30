"""
input_handler.py

Handles all user interaction for the README Generator.
Responsibilities:
  - Displaying styled terminal output using rich
  - Collecting user input using questionary
  - Validating input live before accepting it
  - Returning a clean data dictionary for the template engine

This is the ONLY module that talks to the user.
All other modules are pure logic — no input, no printing.
"""

import sys
import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

from readme_generator.config import(
    APP_NAME,
    APP_VERSION,
    TemplateType,
    TEMPLATE_DISPLAY_NAMES,
    LICENSE_OPTIONS,
)

from readme_generator.validator import (
    validate_project_name,
    validate_description,
    validate_github_username,
    validate_required_field,
    sanitize_list_input,
    sanitize_multiline_input,
)

# ── Console & Style Setup ──────────────────────────────────────────────────────

console = Console()

# Custom questionary style — matches a clean, professional terminal look
PROMPT_STYLE = Style([
    ("qmark",     "fg:#00d7af bold"),   # the ? mark
    ("question",  "bold"),              # question text
    ("answer",    "fg:#00d7af bold"),   # confirmed answer
    ("pointer",   "fg:#00d7af bold"),   # arrow in select menus
    ("selected",  "fg:#00d7af bold"),   # selected item
    ("separator", "fg:#6c6c6c"),        # separator lines
    ("instruction","fg:#6c6c6c"),       # hint text
])

# ── Display Helpers ────────────────────────────────────────────────────────────

def display_welcome() -> None:
  """Displays the welcome banner when the app starts."""
  title = Text(f"{APP_NAME}  v{APP_VERSION}", style="bold cyan")
  subtitle = Text(
        "Generate professional README.md files in seconds",
        style="dim"
    )
  
  content = Text()
  content.append(f"{APP_NAME}  ", style="bold cyan")
  content.append(f"v{APP_VERSION}\n", style="cyan")
  content.append(
    "Generate professional README.md files in seconds",
    style="dim white"
  )

  console.print()
  console.print(Panel(
        content,
        box=box.DOUBLE_EDGE,
        border_style="cyan",
        padding=(1, 4),
    ))
  console.print()

def display_section(title: str) -> None:
    """Prints a styled section header between groups of questions."""
    console.print()
    console.print(f"  [bold cyan]── {title}[/bold cyan]")
    console.print()


def display_success(message: str) -> None:
    """Prints a green success message."""
    console.print(f"\n  [bold green]✔[/bold green]  {message}\n")


def display_error(message: str) -> None:
    """Prints a red error message."""
    console.print(f"\n  [bold red]✖[/bold red]  {message}\n")


def display_info(message: str) -> None:
    """Prints a cyan informational message."""
    console.print(f"  [cyan]ℹ[/cyan]  {message}")

# ── Prompt Helpers ─────────────────────────────────────────────────────────────

def ask(question: str, validator_fn=None, field_name: str = "") -> str:
    """
    Asks a single text question with optional live validation.

    questionary's validate parameter accepts a function that:
      - Returns True if the input is valid
      - Returns an error string if invalid

    This bridges our validator module into questionary's live
    validation system — the user sees the error inline and must
    fix it before continuing.

    Args:
        question:     The prompt text shown to the user.
        validator_fn: A function from validator.py that returns
                      (bool, str). Optional.
        field_name:   Used in the generic required-field validator.
    """
    def _validate(value):
        if validator_fn:
            valid, error = validator_fn(value)
            return error if not valid else True
        if field_name:
            valid, error = validate_required_field(value, field_name)
            return error if not valid else True
        return True

    try:
        answer = questionary.text(
            question,
            style=PROMPT_STYLE,
            validate=_validate if (validator_fn or field_name) else None,
        ).ask()
    except KeyboardInterrupt:
        _handle_exit()

    if answer is None:
        _handle_exit()

    return answer.strip()


def ask_select(question: str, choices: list[str]) -> str:
    """
    Presents an arrow-key selection menu and returns the chosen value.
    """
    try:
        answer = questionary.select(
            question,
            choices=choices,
            style=PROMPT_STYLE,
        ).ask()
    except KeyboardInterrupt:
        _handle_exit()

    if answer is None:
        _handle_exit()

    return answer


def ask_list(question: str, hint: str = "") -> list[str]:
    """
    Asks the user for a comma-separated list and returns it cleaned.

    Example input:  "Python, Flask , SQLite"
    Returns:        ["Python", "Flask", "SQLite"]
    """
    if hint:
        display_info(hint)

    def _validate(value):
        items = sanitize_list_input(value)
        if not items:
            return "Please enter at least one item."
        return True

    try:
        raw = questionary.text(
            question,
            style=PROMPT_STYLE,
            validate=_validate,
        ).ask()
    except KeyboardInterrupt:
        _handle_exit()

    if raw is None:
        _handle_exit()

    return sanitize_list_input(raw)


def ask_multiline_list(question: str) -> list[str]:
    """
    Collects multiple items one at a time until the user is done.

    Returns a list of the entered items.
    """
    console.print(f"  [bold]{question}[/bold]")
    display_info("Enter one item per line. Leave blank and press Enter when done.\n")

    items = []
    index = 1

    while True:
        try:
            entry = questionary.text(
                f"  Item {index}",
                style=PROMPT_STYLE,
            ).ask()
        except KeyboardInterrupt:
            _handle_exit()

        if entry is None or entry.strip() == "":
            if not items:
                display_error("Please enter at least one item.")
                continue
            break

        items.append(entry.strip())
        index += 1

    return items


def ask_confirm(question: str, default: bool = False) -> bool:
    """Asks a yes/no confirmation question."""
    try:
        answer = questionary.confirm(
            question,
            default=default,
            style=PROMPT_STYLE,
        ).ask()
    except KeyboardInterrupt:
        _handle_exit()

    if answer is None:
        _handle_exit()

    return answer


def _handle_exit() -> None:
    """Gracefully exits the program when the user cancels."""
    console.print(
        "\n\n  [dim]Cancelled — no file was saved.[/dim]\n"
    )
    sys.exit(0)


# ── Common Fields (shared across all templates) ────────────────────────────────

def _collect_common_fields() -> dict:
    """
    Collects the fields every template needs.
    Called at the start of every template-specific collector.
    """
    display_section("Project Details")

    project_name = ask(
        "Project name:",
        validator_fn=validate_project_name,
    )

    description = ask(
        "Short description (one sentence):",
        validator_fn=validate_description,
    )

    display_section("Features & Tech Stack")

    features = ask_list(
        "Key features:",
        hint="Comma-separated  e.g.  User authentication, REST API, Dark mode",
    )

    tech_stack = ask_list(
        "Tech stack:",
        hint="Comma-separated  e.g.  Python, Flask, SQLite",
    )

    display_section("Installation & Usage")

    installation_steps = ask_multiline_list("Installation steps:")

    usage_example = ask(
        "Usage example (code snippet or command):",
        field_name="Usage example",
    )

    display_section("Author & License")

    author_name = ask(
        "Your full name:",
        field_name="Author name",
    )

    github_username = ask(
        "GitHub username:",
        validator_fn=validate_github_username,
    )

    license_type = ask_select(
        "License:",
        choices=LICENSE_OPTIONS,
    )

    return {
        "project_name"      : project_name,
        "description"       : description,
        "features"          : features,
        "tech_stack"        : tech_stack,
        "installation_steps": installation_steps,
        "usage_example"     : usage_example,
        "author_name"       : author_name,
        "github_username"   : github_username,
        "license_type"      : license_type,
    }


# ── Template-Specific Collectors ──────────────────────────────────────────────

def _collect_python_fields() -> dict:
    """Collects all fields for a Python project README."""
    data = _collect_common_fields()
    return data


def _collect_ml_fields() -> dict:
    """Collects all fields for a Machine Learning project README."""
    data = _collect_common_fields()

    display_section("Machine Learning Details")

    data["dataset_info"] = ask(
        "Dataset description:",
        field_name="Dataset description",
    )
    data["model_architecture"] = ask(
        "Model architecture:",
        field_name="Model architecture",
    )
    data["training_info"] = ask(
        "Training details (optimizer, epochs, etc.):",
        field_name="Training details",
    )
    data["results"] = ask(
        "Results / metrics achieved:",
        field_name="Results",
    )

    return data


def _collect_web_fields() -> dict:
    """Collects all fields for a Web project README."""
    data = _collect_common_fields()

    display_section("Web Project Details")

    live_demo = ask(
        "Live demo URL (leave blank to skip):",
    )
    data["live_demo_url"] = live_demo

    has_env = ask_confirm(
        "Does your project use environment variables?",
        default=False,
    )
    if has_env:
        data["env_variables"] = ask_list(
            "Environment variables:",
            hint="e.g.  SECRET_KEY=your_secret, DEBUG=False",
        )
    else:
        data["env_variables"] = []

    has_api = ask_confirm(
        "Does your project have API endpoints to document?",
        default=False,
    )
    if has_api:
        data["api_endpoints"] = ask_list(
            "API endpoints:",
            hint="e.g.  GET /api/users, POST /api/auth/login",
        )
    else:
        data["api_endpoints"] = []

    return data


def _collect_java_fields() -> dict:
    """Collects all fields for a Java project README."""
    data = _collect_common_fields()

    display_section("Java Project Details")

    data["java_version"] = ask(
        "Java version (e.g. 17, 21):",
        field_name="Java version",
    )
    data["build_tool"] = ask_select(
        "Build tool:",
        choices=["Maven", "Gradle", "None"],
    )

    return data


# ── Template Selector ──────────────────────────────────────────────────────────

def select_template_type() -> TemplateType:
    """
    Presents the template selection menu and returns the chosen
    TemplateType enum value.
    """
    display_section("Choose Template")

    choices = [
        label for label in TEMPLATE_DISPLAY_NAMES.values()
    ]

    chosen_label = ask_select(
        "What type of project is this?",
        choices=choices,
    )

    # Reverse lookup — find the TemplateType whose label was chosen
    for template_type, label in TEMPLATE_DISPLAY_NAMES.items():
        if label == chosen_label:
            return template_type


# ── Public Entry Point ─────────────────────────────────────────────────────────

# Maps each TemplateType to its collector function
_COLLECTORS = {
    TemplateType.PYTHON: _collect_python_fields,
    TemplateType.ML    : _collect_ml_fields,
    TemplateType.WEB   : _collect_web_fields,
    TemplateType.JAVA  : _collect_java_fields,
}


def collect_user_input(template_type: TemplateType) -> dict:
    """
    Public function called by main.py.
    Dispatches to the correct collector based on template type
    and returns the completed data dictionary.

    Args:
        template_type: The TemplateType chosen by the user.

    Returns:
        A dictionary ready to be passed to render_template().
    """
    collector = _COLLECTORS.get(template_type)

    if collector is None:
        raise ValueError(
            f"No input collector defined for template type: {template_type}"
        )

    return collector()