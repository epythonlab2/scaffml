# scaffml  

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  

---

## 🚀 Overview

**scaffml** is a **professional ML project structure generator** that allows data scientists and ML engineers to quickly scaffold production-ready machine learning projects.  

It provides:  

- Clean, modular project architecture  
- Optional Docker support  
- Templated code files for rapid development  
- Preconfigured `.gitignore` and folder structure  
- Easy integration with CI/CD, testing, and ML workflows  

---

## 📦 Features

- ✅ Generate ML projects with a single CLI command  
- ✅ Optional Docker support via `--docker` flag  
- ✅ Predefined folder hierarchy: `app/`, `src/`, `data/`, `notebooks/`, `tests/`  
- ✅ Jinja2 templated files for customizable project boilerplate  
- ✅ Safe collision detection to avoid overwriting existing projects  
- ✅ Professional CLI with version info and help menus  

---

## 🛠️ Installation

Create directory:

``bash
mkdir your_root_project_name
cd your_root_project_name
```

Activate vertual Env(Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install via pip:

```bash
pip install scaffml
```

Or clone and install locally:

```bash
git clone https://github.com/epythonlab2/scaffml.git
cd scaffml
pip install .
```

---

## ⚡ Usage

### Check version

```bash
scaffml version
```

### Create a new ML project

```bash
scaffml create my_ml_project
```

### Create a new ML project with Docker support

```bash
scaffml create my_ml_project --docker
```

- This generates a professional folder structure with templated files.  
- Empty directories are preserved with `.gitkeep`.  

---

## 📂 Generated Project Structure

Example project layout:

```text
my_ml_project/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   └── prediction.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── pipelines/
│   ├── services/
│   └── core/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── notebooks/
├── models/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── preprocessing.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── predict.py
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_data.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── __init__.py
├── .gitignore
├── Dockerfile
├── requirements.txt
├── README.md
└── pyproject.toml
```

---

## 📝 Contributing

We welcome contributions!  

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/my-feature`)  
3. Commit your changes (`git commit -m "Add feature"`)  
4. Push and submit a pull request  

---

## 📄 License

**MIT License** – see [LICENSE](LICENSE) for details.

---

## 💡 Notes

- Designed for ML engineers who want **clean, production-ready projects** quickly.  
- Easily extendable for additional templates and features.  
- Works cross-platform (Linux/macOS/Windows) with Python 3.10+.