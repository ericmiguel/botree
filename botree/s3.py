"""Botree S3 utilities."""

from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional

from boto3.session import Session


class Bucket:
    """AWS S3 Bucket level transactions."""

    def __init__(
        self,
        session: Session,
        name: str,
        client_kwargs: dict = dict(),
        resource_kwargs: dict = dict(),
    ):
        self.name = name
        self.session = session
        self.client = self.session.client(service_name="s3", **client_kwargs)
        self.resource = self.session.resource("s3", **resource_kwargs).Bucket(
            name=self.name
        )

    def download(self, source: Path, target: Path, **kwargs):
        """
        Download a file from S3.

        Parameters
        ----------
        source : Path
            remote file path.
        target : Path
            local file path.
        """
        self.resource.download_file(str(source), str(target), **kwargs)

    def upload(self, source: Path, target: Path, **kwargs):
        """
        Upload a file to S3.

        Parameters
        ----------
        source : Path
            local file path.
        target : Path
            remote file path.
        """
        self.resource.upload_file(str(source), str(target), **kwargs)

    def copy(
        self,
        source: Path,
        target: Path,
        source_bucket: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Copy an object stored in the bucket or from another bucket.

        If source_bucket is not specified, the object is copied from the current bucket.

        if target_key has no suffix, it assumes target_key is a folder and source_key
        file name is used.

        Parameters
        ----------
        source : Path
            source file path
        target : Path
            target file path. If target_key has no suffix, it assumes target_key
            is a folder.
        source_bucket : Optional[str], optional
            bucket from wich source file will be copied from, by default None
        """
        copy_source = {"Bucket": source_bucket, "Key": str(source)}

        if not source_bucket:
            copy_source.update({"Bucket": self.name})

        if not target.suffix:
            target = target / source.name

        self.client.copy(copy_source, self.name, str(target), **kwargs)  # type: ignore

    def list_files(
        self, prefix: str = "", reverse: bool = False, *args, **kwargs
    ) -> List[str]:
        """
        List and sort (by date) all files in a given prefix.

        Parameters
        ----------
        prefix : str
            S3 prefix.
        reverse : bool, optional
            Reverse (descending) date sort, by default False

        Returns
        -------
        List[str]
            Paths to files.
        """
        response = self.client.list_objects_v2(
            Bucket=self.name, Prefix=prefix, Delimiter="", *args, **kwargs
        )

        date_sorted = sorted(
            response["Contents"],  # type: ignore
            key=lambda x: x["LastModified"],  # type: ignore
            reverse=reverse,
        )

        keys = [key["Key"] for key in date_sorted]  # type: ignore

        return keys

    def list_folders(self, prefix: str = "", *args, **kwargs) -> List[str]:
        """
        List all folders in a given prefix.

        Parameters
        ----------
        prefix : str
            S3 prefix.

        Returns
        -------
        List[str]
            Paths to folders.
        """
        if not prefix.endswith("/"):
            prefix = prefix + "/"

        response = self.client.list_objects_v2(
            Bucket=self.name, Prefix=prefix, Delimiter="/", *args, **kwargs
        )

        keys = [key["Prefix"] for key in response["CommonPrefixes"]]  # type: ignore

        return keys

    def paginate_objects(self, prefix: str = "", page_size: int = 1000) -> Generator:
        """
        Return a list all objects in a bucket with specified prefix.

        Paginator is useful when you have 1000s of files in S3.
        S3 list_objects_v2 can list at max 1000 files in one go.
        :return: None
        """
        paginator = self.client.get_paginator("list_objects_v2")

        response = paginator.paginate(
            Bucket=self.name, Prefix=prefix, PaginationConfig={"PageSize": page_size}
        )

        for page in response:
            files = page.get("Contents")
            yield files

    def delete(self, target: Path, **kwargs):
        """
        Delete a file from S3.

        Parameters
        ----------
        target : Path
            remote file path.
        """
        self.client.delete_object(Bucket=self.name, Key=str(target), **kwargs)


class S3:
    """AWS S3 operations."""

    def __init__(self, session: Session, **kwargs):
        """
        S3 class init.

        Parameters
        ----------
        region : str, optional
            região AWS do bucket
        profile : Optional[str], optional
            profile da AWS CLI, by default None.
        """
        self.session = session
        self.client = self.session.client(service_name="s3", **kwargs)

    def create_bucket(self, name: str, *args, **kwargs):
        """Create a bucket."""
        self.client.create_bucket(Bucket=name, *args, **kwargs)

    def list_buckets(self) -> List[str]:
        """Return a list of bucket names."""
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]  # type: ignore

    def bucket(
        self,
        name: str,
        client_kwargs: dict = dict(),
        resource_kwargs: dict = dict(),
    ) -> Bucket:
        """Get a bucket resource instance."""
        return Bucket(self.session, name, **client_kwargs, **resource_kwargs)
