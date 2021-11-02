from pathlib import Path

from moto import mock_s3


def test_create_list_buckets(botree_session, botree_test_bucket):
    """Creation and bucket list methods."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)
        buckets = botree_session.s3.list_buckets()
        assert buckets == [botree_test_bucket]


def test_listobj_upload_download(botree_session, botree_test_bucket, text_file):
    """List objects, upload and download methods."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)
        botree_session.s3.upload(botree_test_bucket, text_file, text_file.name)
        files = botree_session.s3.list_objects(bucket=botree_test_bucket)
        assert files == [text_file.name]
        download_temp_file = Path(text_file.parent, "download_temp_file.txt")
        botree_session.s3.download(
            botree_test_bucket, text_file.name, download_temp_file
        )
        assert Path(download_temp_file).is_file()
