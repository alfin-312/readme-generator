"""
file_manager.py

Handles all file system operations for the README Generator.
Responsibilities:
  - Ensuring the output directory exists
  - Writing rendered content to disk
  - Detecting existing files before overwriting
  - Returning structured results so the caller can decide what to do

This module never interacts with the user directly.
It receives data, acts on the file system, and returns results.
"""

from pathlib import Path
from dataclasses import dataclass
from readme_generator.config import OUTPUT_DIR, OUTPUT_FILENAME

# ── Result Objects ─────────────────────────────────────────────────────────────

@dataclass
class SaveResult:
    """
    Represents the outcome of a save operation.

    Using a dataclass instead of returning a raw tuple keeps
    the result self-documenting. The caller reads result.success
    and result.path instead of result[0] and result[1].

    Attributes:
        success:      True if the file was written successfully.
        path:         The absolute path where the file was saved.
        already_existed: True if a file already existed at that path
                         before this save operation.
        error:        Human-readable error message if success is False.
    """
    success       : bool
    path          : Path
    already_existed: bool = False
    error          : str = ""

# ── Core Functions ─────────────────────────────────────────────────────────────

def ensure_directory(directory: Path) -> None:
    """
    Creates a directory if it does not already exist.
    Does nothing if it already exists.

    parents=True  means it creates parent folders too if needed.
    exist_ok=True means it won't raise an error if already there.
    """
    directory.mkdir(parents=True, exist_ok=True)

def file_exists(path: Path) -> bool:
    """True is file exists in the given path"""
    return path.is_file()

def save_readme(
    content       : str,
    output_dir    : Path = OUTPUT_DIR,
    filename      : str  = OUTPUT_FILENAME,
    overwrite     : bool = False,
) -> SaveResult:
    """
    Saves rendered README content to a file.

    Args:
        content:    The rendered Markdown string to save.
        output_dir: Directory to save into. Defaults to OUTPUT_DIR
                    from config.
        filename:   Output filename. Defaults to 'README.md'.
        overwrite:  If False and file exists, returns a SaveResult
                    with success=False and already_existed=True.
                    The caller then decides whether to ask the user
                    for confirmation.

    Returns:
        SaveResult describing what happened.
    """
    output_path = Path(output_dir) / filename

    try: 
        ensure_directory(Path(output_dir))
    except PermissionError:
        return SaveResult(
            success=False,
            path=output_path,
            error=f"Permission denied: cannot create directory '{output_dir}'."
        )
    
    if file_exists(output_path) and not overwrite:
        return SaveResult(
            success=False,
            path=output_path,
            already_existed=True,
            error= f"'{filename}' already exists at {output_path}."
        )
    
    try:
        output_path.write_text(content, encoding="utf-8")
    except PermissionError:
        return SaveResult(
            success=False,
            path=output_path,
            error=f"Permission denied: cannot write to '{output_path}'."
        )
    except OSError as e:
        return SaveResult(
            success=False,
            path=output_path,
            error=f"Unexpected error while saving file: {e}"
        )

    return SaveResult(
        success=True,
        path=output_path,
        already_existed=file_exists(output_path),
    )

def read_file(path: Path) -> tuple[bool, str]:
    """
    Reads a file and returns its content.

    Returns:
        (True, content)  if successful.
        (False, error)   if the file could not be read.

    Useful later when loading saved READMEs or config files.
    """
    try:
        content = Path(path).read_text(encoding="utf-8")
        return True, content
    except FileNotFoundError:
        return False, f"File not found: '{path}'."
    except PermissionError:
        return False, f"Permission denied: cannot read '{path}'."
    except OSError as e:
        return False, f"Unexpected error reading file: {e}"
    
def resolve_output_path(
        output_dir: Path = OUTPUT_DIR,
        filename  : str  = OUTPUT_FILENAME,
) -> Path:
    """
    Returns the full resolved absolute path for an output file.
    Does not create or check the file — purely path construction.

    Useful for displaying the save path to the user before saving.
    """
    return (Path(output_dir) / filename).resolve()