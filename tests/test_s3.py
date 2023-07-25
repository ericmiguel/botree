from pathlib import Path

import pytest

from moto import mock_s3


def test_create_list_buckets(botree_session, botree_test_bucket):
    """Creation and bucket list methods."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)
        buckets = botree_session.s3.list_buckets()
        assert buckets == [botree_test_bucket]


def test_listobj_upload_download_delete(botree_session, botree_test_bucket, text_file):
    """List objects, upload, download and delete methods."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)

        botree_session.s3.bucket(botree_test_bucket).upload(text_file, text_file.name)

        files = botree_session.s3.bucket(botree_test_bucket).list_files()

        assert files == [text_file.name]

        download_temp_file = Path(text_file.parent, "download_temp_file.txt")

        botree_session.s3.bucket(botree_test_bucket).download(
            text_file.name, download_temp_file
        )

        assert Path(download_temp_file).is_file()

        botree_session.s3.bucket(botree_test_bucket).delete(text_file.name)

        with pytest.raises(KeyError):
            files = botree_session.s3.bucket(botree_test_bucket).list_files()


def test_copy_object(botree_session, botree_test_bucket, text_file):
    """Copy object method."""
    with mock_s3():
        other_botree_test_bucket = "other-botree-test-bucket"

        botree_session.s3.create_bucket(botree_test_bucket)

        botree_session.s3.create_bucket(other_botree_test_bucket)

        uploaded_file_path = Path(text_file.name)

        botree_session.s3.bucket(other_botree_test_bucket).upload(
            text_file, uploaded_file_path
        )

        botree_session.s3.bucket(botree_test_bucket).copy(
            uploaded_file_path,
            uploaded_file_path,
            source_bucket=other_botree_test_bucket,
        )

        files = botree_session.s3.bucket(botree_test_bucket).list_files()
        assert files == [uploaded_file_path.name]
