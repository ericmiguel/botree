# Botree: a friendly wrapper for boto3

Botree is a higher level API and text user intercace tool for AWS services.

## 🧠 Features

- ✔️ High level and easy to remember API for AWS services.
- 🔨 TUI (text user interface) powered by [Textual](https://github.com/willmcgugan/textual).
- 🔨 Asynchronous execution of I/O tasks.

## 🧰 Supported AWS services

- ✔️ S3
- 🔨 Secrets
- 🔨 EC2

## 🏗️ Development

Botree relies on [Poetry](https://github.com/python-poetry/poetry).

Install the Python dependencies with:

```bash
poetry install
```

## ⚗️ Testing

```bash
poetry run pytest --cov=botree tests/
```
