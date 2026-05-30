{# ── Machine Learning Project Template ───────────────────────────── #}
{# Variables expected:                                                 #}
{#   project_name, description, features, tech_stack,                 #}
{#   dataset_info, model_architecture, training_info,                 #}
{#   results, installation_steps, usage_example,                      #}
{#   author_name, github_username, license_type                       #}
{# ─────────────────────────────────────────────────────────────────── #}

# {{ project_name }}

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![ML](https://img.shields.io/badge/Machine%20Learning-Project-orange?style=flat-square)
![License](https://img.shields.io/badge/License-{{ license_type | urlencode }}-green?style=flat-square)

> {{ description }}

---

## ✨ Features

{% for feature in features %}
- {{ feature }}
{% endfor %}

---

## 🛠️ Tech Stack

{% for tech in tech_stack %}
- {{ tech }}
{% endfor %}

---

## 📊 Dataset

{{ dataset_info }}

---

## 🧠 Model Architecture

{{ model_architecture }}

---

## 🏋️ Training

{{ training_info }}

---

## 📈 Results

{{ results }}

---

## ⚙️ Installation

```bash
{% for step in installation_steps %}
{{ step }}
{% endfor %}
```

---

## 📖 Usage

```python
{{ usage_example }}
```

---

## 👤 Author

**{{ author_name }}**

- GitHub: [@{{ github_username }}](https://github.com/{{ github_username }})

---

## 📄 License

This project is licensed under the **{{ license_type }}** License.