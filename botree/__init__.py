"""Botree - A friendly wrapper for boto3."""

# flake8: noqa

from botree.botree import Session as session
from botree.s3 import S3 as s3
from botree.s3 import Bucket as bucket


# module level doc-string
__doc__ = """
botree - A friendly wrapper for boto3.
=====================================================================

**Botree** aims to abstract and optimize the use of the powerful Boto3 by easing
its lower-level features with a little syntactic sugar.
"""
