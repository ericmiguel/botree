"""Botree core functions."""
from typing import Optional

from boto3.session import Session as boto_session
from botree.cost_explorer import CostExplorer
from botree.logs import Logs
from botree.s3 import S3
from botree.secrets_manager import SecretsManager


class Session:
    """Botree, a friendly Boto3 wrapper."""

    def __init__(
        self,
        region: str,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        profile: Optional[str] = None,
    ):
        """
        Start point to all other AWS services.

        If not specified, the default credentials (usualy in ~/.aws/credentials)
        are used. Use 'profile' to specify a different AWS profile.
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.region = region
        self.profile = profile
        self.session = boto_session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            region_name=region,
            profile_name=profile,
        )

    @property
    def s3(self) -> S3:
        """Get a S3 instance."""
        return S3(self.session)

    @property
    def secrets_manager(self) -> SecretsManager:
        """Get a SecretsManager instance."""
        return SecretsManager(self.session)

    @property
    def cost_explorer(self) -> CostExplorer:
        """Get a SecretsManager instance."""
        return CostExplorer(self.session)

    @property
    def logs(self) -> Logs:
        """Get a Logs instance."""
        return Logs(self.session)
