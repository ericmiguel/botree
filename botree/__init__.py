"""Botree - A friendly wrapper for boto3."""

from .core import Session
from .core import Session as session
from .core import S3
from .s3 import S3 as s3
from .s3 import Bucket
from .s3 import Bucket as bucket

__all__ = ['Session', 'session', 'S3', 's3', 'Bucket', 'bucket']


# module level doc-string
__doc__ = """Botree - A friendly wrapper for boto3."""
