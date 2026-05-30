{# ── Web Project Template ─────────────────────────────────────────── #}
{# Variables expected:                                                  #}
{#   project_name, description, features, tech_stack,                  #}
{#   live_demo_url, installation_steps, usage_example,                 #}
{#   env_variables, api_endpoints,                                      #}
{#   author_name, github_username, license_type                        #}
{# ─────────────────────────────────────────────────────────────────── #}

# {{ project_name }}

![License](https://img.shields.io/badge/License-{{ license_type | urlencode }}-green?style=flat-square)
{% if live_demo_url %}
![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=flat-square)
{% endif %}

> {{ description }}

{% if live_demo_url %}
🌐 **Live Demo:** [{{ live_demo_url }}]({{ live_demo_url }})
{% endif %}

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

## ⚙️ Installation

```bash
{% for step in installation_steps %}
{{ step }}
{% endfor %}
```

---

{% if env_variables %}
## 🔐 Environment Variables

Create a `.env` file in the root directory and add the following:

```env
{% for var in env_variables %}
{{ var }}
{% endfor %}
```

---
{% endif %}

{% if api_endpoints %}
## 🔌 API Endpoints

{% for endpoint in api_endpoints %}
- `{{ endpoint }}`
{% endfor %}

---
{% endif %}

## 📖 Usage

{{ usage_example }}


---

## 👤 Author

**{{ author_name }}**

- GitHub: [@{{ github_username }}](https://github.com/{{ github_username }})

---

## 📄 License

This project is licensed under the **{{ license_type }}** License.