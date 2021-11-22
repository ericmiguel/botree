from pathlib import Path

import pytest

import botree
from moto import mock_s3


@pytest.fixture(scope="function")
def botree_session():
    """
    Default AWS session for testing.

    Using the boto3 session api avoids using the ugly os.environ strategy
    as suggested by moto docs and still protects the real aws credentials from using.
    """
    with mock_s3():
        return botree.session(
            access_key_id="testing",
            secret_access_key="testing",
            session_token="testing",
            region="us-east-1",
            profile=None,
        )


@pytest.fixture(scope="function")
def botree_test_bucket():
    """Moto S3 bucket for testing."""
    return "botree-test-bucket"


@pytest.fixture(scope="session")
def text_file(tmpdir_factory):
    """Create a dummie txt file for s3 upload, list objects and download methods."""
    tmp_file = tmpdir_factory.mktemp("tmp").join("temp_text_file.txt")
    tmp_file.write_text("botree test!", encoding="utf-8")
    return Path(tmp_file)
