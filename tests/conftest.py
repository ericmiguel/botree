from pathlib import Path

import botree
import pytest

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


@pytest.fixture(scope="session")
def list_of_files(tmpdir_factory):
    """Create a dummie list of files for s3 list objects by date."""
    tmp_file = tmpdir_factory.mktemp("tmp").join("temp_text_file_1.txt")
    tmp_file2 = tmpdir_factory.mktemp("tmp").join("temp_text_file_2.txt")
    tmp_file3 = tmpdir_factory.mktemp("tmp").join("temp_text_file_3.txt")

    for file in [tmp_file, tmp_file2, tmp_file3]:
        file.write_text("botree test!", encoding="utf-8")

    return [Path(tmp_file), Path(tmp_file2), Path(tmp_file3)]