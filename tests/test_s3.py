from pathlib import Path
import time

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

        files = botree_session.s3.bucket(botree_test_bucket).list_objects()

        assert files == [text_file.name]

        download_temp_file = Path(text_file.parent, "download_temp_file.txt")

        botree_session.s3.bucket(botree_test_bucket).download(
            text_file.name, download_temp_file
        )

        assert Path(download_temp_file).is_file()

        botree_session.s3.bucket(botree_test_bucket).delete(text_file.name)

        with pytest.raises(KeyError):
            files = botree_session.s3.bucket(botree_test_bucket).list_objects()

def test_list_obj_by_date(botree_session, botree_test_bucket, list_of_files):
    """List objects by date method."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)

        ascending_order = [file.name for file in list_of_files]
        descending_order = ascending_order[::-1]

        for file in list_of_files:
            botree_session.s3.bucket(botree_test_bucket).upload(file, file.name)
            time.sleep(1)

        files = botree_session.s3.bucket(botree_test_bucket).list_objects(sort_by_date="ascending")

        assert files == ascending_order

        files = botree_session.s3.bucket(botree_test_bucket).list_objects(sort_by_date="descending")

        assert files == descending_order


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

        files = botree_session.s3.bucket(botree_test_bucket).list_objects()
        assert files == [uploaded_file_path.name]
