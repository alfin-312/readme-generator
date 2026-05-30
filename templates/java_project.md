{# ── Java Project Template ────────────────────────────────────────── #}
{# Variables expected:                                                  #}
{#   project_name, description, features, tech_stack,                  #}
{#   java_version, build_tool, installation_steps, usage_example,      #}
{#   author_name, github_username, license_type                        #}
{# ─────────────────────────────────────────────────────────────────── #}

# {{ project_name }}

![Java](https://img.shields.io/badge/Java-{{ java_version }}+-red?style=flat-square&logo=java)
![Build](https://img.shields.io/badge/Build-{{ build_tool }}-blue?style=flat-square)
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

## 📋 Prerequisites

- Java {{ java_version }}+
- {{ build_tool }}

---

## ⚙️ Installation & Build

```bash
{% for step in installation_steps %}
{{ step }}
{% endfor %}
```

---

## 📖 Usage

```java
{{ usage_example }}
```

---

## 👤 Author

**{{ author_name }}**

- GitHub: [@{{ github_username }}](https://github.com/{{ github_username }})

---

## 📄 License

This project is licensed under the **{{ license_type }}** License.