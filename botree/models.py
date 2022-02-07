from typing import Dict
from typing import Union

from pydantic import BaseModel
from pydantic import Field


class ResponseMetadata(BaseModel):
    request_id: str = Field("", alias="RequestId")
    http_status_code: int = Field(200, alias="HTTPStatusCode")
    http_headers: Dict[str, Union[str, int]] = Field(alias="HTTPHeaders")
    retry_attempts: int = Field(0, alias="RetryAttempts")
