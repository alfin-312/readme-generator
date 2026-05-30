"""
test_file_manager.py

Tests for file system operations.
We use pytest's tmp_path fixture to create temporary directories
so tests never touch the real output/ folder.
"""

import pytest
from pathlib import Path
from readme_generator.file_manager import (
    save_readme,
    read_file,
    file_exists,
    ensure_directory,
    resolve_output_path,
    SaveResult,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────

SAMPLE_CONTENT = "# Test Project\n\nThis is a test README."


# ── ensure_directory ───────────────────────────────────────────────────────────

class TestEnsureDirectory:

    def test_creates_directory_if_not_exists(self, tmp_path):
        new_dir = tmp_path / "new_folder"
        assert not new_dir.exists()
        ensure_directory(new_dir)
        assert new_dir.exists()

    def test_does_not_raise_if_directory_already_exists(self, tmp_path):
        ensure_directory(tmp_path)  # already exists
        assert tmp_path.exists()

    def test_creates_nested_directories(self, tmp_path):
        nested = tmp_path / "a" / "b" / "c"
        ensure_directory(nested)
        assert nested.exists()


# ── save_readme ────────────────────────────────────────────────────────────────

class TestSaveReadme:

    def test_saves_file_successfully(self, tmp_path):
        result = save_readme(SAMPLE_CONTENT, output_dir=tmp_path)
        assert result.success is True
        assert result.path.is_file()

    def test_saved_file_contains_correct_content(self, tmp_path):
        save_readme(SAMPLE_CONTENT, output_dir=tmp_path)
        written = (tmp_path / "README.md").read_text(encoding="utf-8")
        assert written == SAMPLE_CONTENT

    def test_returns_save_result_object(self, tmp_path):
        result = save_readme(SAMPLE_CONTENT, output_dir=tmp_path)
        assert isinstance(result, SaveResult)

    def test_custom_filename_is_used(self, tmp_path):
        result = save_readme(
            SAMPLE_CONTENT,
            output_dir=tmp_path,
            filename="CUSTOM.md"
        )
        assert result.success is True
        assert (tmp_path / "CUSTOM.md").is_file()

    def test_does_not_overwrite_by_default(self, tmp_path):
        save_readme(SAMPLE_CONTENT, output_dir=tmp_path)
        result = save_readme("New content", output_dir=tmp_path)
        assert result.success is False
        assert result.already_existed is True

    def test_overwrites_when_flag_is_true(self, tmp_path):
        save_readme(SAMPLE_CONTENT, output_dir=tmp_path)
        result = save_readme(
            "New content",
            output_dir=tmp_path,
            overwrite=True
        )
        assert result.success is True
        written = (tmp_path / "README.md").read_text(encoding="utf-8")
        assert written == "New content"

    def test_creates_output_dir_if_missing(self, tmp_path):
        new_dir = tmp_path / "brand_new_folder"
        assert not new_dir.exists()
        result = save_readme(SAMPLE_CONTENT, output_dir=new_dir)
        assert result.success is True
        assert new_dir.exists()


# ── read_file ──────────────────────────────────────────────────────────────────

class TestReadFile:

    def test_reads_existing_file(self, tmp_path):
        target = tmp_path / "test.md"
        target.write_text(SAMPLE_CONTENT, encoding="utf-8")
        success, content = read_file(target)
        assert success is True
        assert content == SAMPLE_CONTENT

    def test_returns_false_for_missing_file(self, tmp_path):
        missing = tmp_path / "ghost.md"
        success, error = read_file(missing)
        assert success is False
        assert "not found" in error.lower()


# ── resolve_output_path ────────────────────────────────────────────────────────

class TestResolveOutputPath:

    def test_returns_path_object(self, tmp_path):
        result = resolve_output_path(output_dir=tmp_path)
        assert isinstance(result, Path)

    def test_path_ends_with_readme_md(self, tmp_path):
        result = resolve_output_path(output_dir=tmp_path)
        assert result.name == "README.md"

    def test_custom_filename_reflected_in_path(self, tmp_path):
        result = resolve_output_path(output_dir=tmp_path, filename="CUSTOM.md")
        assert result.name == "CUSTOM.md"