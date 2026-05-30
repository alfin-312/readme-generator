"""
main.py

Entry point for the README Generator.
Orchestrates the full pipeline:
    1. Welcome screen
    2. Template selection
    3. User input collection
    4. README rendering
    5. Optional preview
    6. File saving with overwrite protection

This module contains no business logic of its own.
It connects modules and controls the flow between them.
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich import box

from readme_generator.input_handler import (
    display_welcome,
    display_success,
    display_error,
    display_info,
    display_section,
    select_template_type,
    collect_user_input,
    ask_confirm,
    ask,
)
from readme_generator.template_engine import render_template
from readme_generator.file_manager import save_readme, resolve_output_path
from readme_generator.config import OUTPUT_DIR, OUTPUT_FILENAME

console = Console()


# ── Preview ────────────────────────────────────────────────────────────────────

def show_preview(content: str) -> None:
    """
    Renders the generated README as styled Markdown in the terminal.

    rich.Markdown renders headers, bold, code blocks, and lists
    with real formatting — the user gets a genuine preview of how
    their README will look on GitHub.
    """
    console.print()
    console.print(Rule("[bold cyan]README Preview[/bold cyan]", style="cyan"))
    console.print()
    console.print(Markdown(content))
    console.print()
    console.print(Rule(style="cyan"))
    console.print()


# ── Save Flow ──────────────────────────────────────────────────────────────────

def handle_save(content: str) -> Path | None:
    """
    Manages the full save flow including overwrite confirmation.

    Returns the saved file path on success, None on cancellation.
    """
    display_section("Save Options")

    # Show the default path and let the user customise it
    default_path = resolve_output_path(OUTPUT_DIR, OUTPUT_FILENAME)
    display_info(f"Default save location:  {default_path}")
    console.print()

    use_custom = ask_confirm(
        "Save to a custom location instead?",
        default=False,
    )

    if use_custom:
        custom_path_str = ask(
            "Enter the full directory path to save into:",
            field_name="Output directory",
        )
        output_dir = Path(custom_path_str)
        filename   = OUTPUT_FILENAME
    else:
        output_dir = OUTPUT_DIR
        filename   = OUTPUT_FILENAME

    # First save attempt
    result = save_readme(
        content,
        output_dir=output_dir,
        filename=filename,
        overwrite=False,
    )

    # Handle the case where the file already exists
    if not result.success and result.already_existed:
        display_error(f"'{filename}' already exists at {result.path}")
        overwrite = ask_confirm(
            "Overwrite the existing file?",
            default=False,
        )

        if not overwrite:
            display_info("Save cancelled — existing file was not changed.")
            return None

        # Second save attempt with overwrite=True
        result = save_readme(
            content,
            output_dir=output_dir,
            filename=filename,
            overwrite=True,
        )

    # Handle any other failure
    if not result.success:
        display_error(f"Could not save file.\n  {result.error}")
        return None

    return result.path


# ── Main Pipeline ──────────────────────────────────────────────────────────────

def main() -> None:
    """
    Main entry point — runs the full README generation pipeline.
    """
    # ── Step 1: Welcome ────────────────────────────────────────────
    display_welcome()

    # ── Step 2: Template Selection ─────────────────────────────────
    template_type = select_template_type()

    # ── Step 3: Collect User Input ─────────────────────────────────
    console.print()
    display_info(
        f"Filling out a [bold cyan]{template_type.name.title()}[/bold cyan] "
        f"project template.  Answer each question — press Enter to confirm.\n"
    )

    data = collect_user_input(template_type)

    # ── Step 4: Render ─────────────────────────────────────────────
    console.print()
    display_info("Generating your README...")

    try:
        content = render_template(template_type, data)
    except Exception as e:
        display_error(f"Failed to render template.\n  {e}")
        sys.exit(1)

    console.print("  [bold green]✔[/bold green]  Rendered successfully.\n")

    # ── Step 5: Preview ────────────────────────────────────────────
    want_preview = ask_confirm(
        "Preview your README in the terminal before saving?",
        default=True,
    )

    if want_preview:
        show_preview(content)

    # ── Step 6: Save ───────────────────────────────────────────────
    saved_path = handle_save(content)

    if saved_path is None:
        console.print(
            "\n  [dim]Exited without saving.[/dim]\n"
        )
        sys.exit(0)

    # ── Step 7: Done ───────────────────────────────────────────────
    display_success(f"README saved successfully!")
    console.print(
        f"  [dim]Location:[/dim]  [bold]{saved_path}[/bold]\n"
    )
    console.print(
        Panel(
            "[bold cyan]What's next?[/bold cyan]\n\n"
            "  [white]• Copy the file to your project's root directory[/white]\n"
            "  [white]• Open it in any Markdown editor to review[/white]\n"
            "  [white]• Push your project to GitHub — your README is ready[/white]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 4),
        )
    )
    console.print()


# ── Guard ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()