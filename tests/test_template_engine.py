"""
test_template_engine.py

Tests for the template rendering pipeline.
We test that templates render without errors and that
the output contains the data we passed in.
"""

import pytest
from readme_generator.template_engine import render_template, get_available_templates
from readme_generator.config import TemplateType


# ── Shared Test Data ───────────────────────────────────────────────────────────

PYTHON_DATA = {
    "project_name"      : "Test Project",
    "description"       : "A project for testing purposes.",
    "features"          : ["Feature one", "Feature two"],
    "tech_stack"        : ["Python", "Pytest"],
    "installation_steps": ["git clone https://github.com/user/repo", "pip install -r requirements.txt"],
    "usage_example"     : "python main.py",
    "author_name"       : "Test Author",
    "github_username"   : "testauthor",
    "license_type"      : "MIT",
}

ML_DATA = {
    **PYTHON_DATA,
    "dataset_info"      : "Custom dataset with 10,000 samples.",
    "model_architecture": "3-layer neural network.",
    "training_info"     : "Trained for 50 epochs with Adam optimizer.",
    "results"           : "Achieved 94% accuracy on test set.",
}

WEB_DATA = {
    **PYTHON_DATA,
    "live_demo_url" : "https://myproject.com",
    "env_variables" : ["SECRET_KEY=your_secret", "DEBUG=False"],
    "api_endpoints" : ["GET /api/users", "POST /api/users"],
}

JAVA_DATA = {
    **PYTHON_DATA,
    "java_version": "17",
    "build_tool"  : "Maven",
}


# ── Render Tests ───────────────────────────────────────────────────────────────

class TestRenderTemplate:

    def test_python_template_renders_without_error(self):
        result = render_template(TemplateType.PYTHON, PYTHON_DATA)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ml_template_renders_without_error(self):
        result = render_template(TemplateType.ML, ML_DATA)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_web_template_renders_without_error(self):
        result = render_template(TemplateType.WEB, WEB_DATA)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_java_template_renders_without_error(self):
        result = render_template(TemplateType.JAVA, JAVA_DATA)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_output_contains_project_name(self):
        result = render_template(TemplateType.PYTHON, PYTHON_DATA)
        assert "Test Project" in result

    def test_output_contains_all_tech_stack_items(self):
        result = render_template(TemplateType.PYTHON, PYTHON_DATA)
        assert "Python" in result
        assert "Pytest" in result

    def test_output_contains_all_features(self):
        result = render_template(TemplateType.PYTHON, PYTHON_DATA)
        assert "Feature one" in result
        assert "Feature two" in result

    def test_output_contains_author_name(self):
        result = render_template(TemplateType.PYTHON, PYTHON_DATA)
        assert "Test Author" in result

    def test_output_contains_github_username(self):
        result = render_template(TemplateType.PYTHON, PYTHON_DATA)
        assert "testauthor" in result

    def test_web_template_shows_demo_url_when_provided(self):
        result = render_template(TemplateType.WEB, WEB_DATA)
        assert "https://myproject.com" in result

    def test_web_template_hides_demo_section_when_empty(self):
        data = {**WEB_DATA, "live_demo_url": ""}
        result = render_template(TemplateType.WEB, data)
        assert "Live Demo" not in result

    def test_invalid_template_type_raises_value_error(self):
        with pytest.raises(ValueError):
            render_template("python_project", PYTHON_DATA)

    def test_ml_template_contains_dataset_info(self):
        result = render_template(TemplateType.ML, ML_DATA)
        assert "Custom dataset with 10,000 samples." in result

    def test_java_template_contains_java_version(self):
        result = render_template(TemplateType.JAVA, JAVA_DATA)
        assert "17" in result


# ── get_available_templates Tests ─────────────────────────────────────────────

class TestGetAvailableTemplates:

    def test_returns_a_list(self):
        result = get_available_templates()
        assert isinstance(result, list)

    def test_returns_four_templates(self):
        result = get_available_templates()
        assert len(result) == 4

    def test_each_item_has_type_and_label(self):
        result = get_available_templates()
        for item in result:
            assert "type" in item
            assert "label" in item

    def test_each_type_is_a_template_type_enum(self):
        result = get_available_templates()
        for item in result:
            assert isinstance(item["type"], TemplateType)