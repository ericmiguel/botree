# botree
# Botree: a friendly wrapper for boto3

Botree is a higher level API and text user intercace tool for AWS services.

## 🧠 Features

- ✔️ High level and easy to remember API for AWS services.
- 🔨 TUI (text user interface) powered by [Textual](https://github.com/willmcgugan/textual).

## 🧰 Supported AWS services

- ✔️ S3
- ✔️ Secrets
- 🔨 CloudWatch
- 🔨 EC2

## 💻 Examples

Until I've written the documentation, some dummie examples may be the best way to get used to the Botree API.

### S3

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

# downloads are more of the same
session.s3.bucket("sample-bucket").download(source_file, target_file)
```

Copy files:

```python
source_file = Path("sample_source_file.png")
target_file = Path("sample_target_file.png")
session.s3.bucket("sample-bucket").copy(source_file, target_file)

# you can specify a source bucket to copy a file from
session.s3.bucket("sample-bucket").copy(source_file, target_file, source_bucket="other-bucket")
```

List files:

```python
session.s3.bucket("sample-bucket").list_objects()
```

Delete files:

```python
session.s3.bucket("sample-bucket").delete("sample_target_file")
```

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