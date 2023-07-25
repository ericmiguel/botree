# Botree: a friendly wrapper for boto3

Botree is a higher level API for AWS services / Boto3 classes and aims to make Boto3 experience easier.

## 🧰 Supported AWS services

Currently, there are just some Boto3 wrapped classes.

-   ✔️ S3
-   ✔️ Secrets
-   ✔️ CloudWatch
-   ✔️ Cost Explorer
-   ✔️ Secrets Manager

## 💻 Basic usage

To start a Botree session, use the following:

```Python
import botree
session = botree.session("us-east-1", profile="dev")
```

Create a bucket:

```Python
session.s3.create_bucket("sample-bucket")
session.s3.list_buckets()
```

Note that all S3 operations will use Python's pathlib to handle directory paths, so let's import it:

```python
from pathlib import Path
```

Download and upload:

```Python
source_file = Path("sample_source_file.png")
target_file = Path("sample_target_file.png")
session.s3.bucket("sample-bucket").upload(source_file, target_file)
session.s3.bucket("sample-bucket").download(source_file, target_file)
```

## 📜 Docs

The docs are under development, but it's (very) early stage is already [available](https://ericmiguel.github.io/botree/).

## 🏗️ Development

Botree relies on [PDM](https://pdm.fming.dev/latest/).

Install the Python dependencies with:

```bash
pdm install
```

## ⚗️ Testing

```bash
pdm run pytest --cov=botree tests/
```

## 🖖 Contributors

<a href = "https://github.com/Tanu-N-Prabhu/Python/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo = ericmiguel/botree"/>
</a>
