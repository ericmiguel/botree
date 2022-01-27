from datetime import datetime

from dateutil.parser import parse
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class HTTPHeaders(BaseModel):
    date: datetime
    content_type: str
    content_length: int
    connection: str
    x_amzn_requestid: str


class ResponseMetadata(BaseModel):
    request_id: str = Field(alias="RequestId")
    http_status_code: int = Field(alias="HTTPStatusCode")
    http_headers: HTTPHeaders = Field(alias="HTTPHeaders")
    retry_attempts: int = Field(alias="RetryAttempts")

    @validator("http_headers", pre=True)
    def validate_http_headers(cls, v):
        fields = [
            "date",
            "content-type",
            "content-length",
            "connection",
            "x-amzn-requestid",
        ]

        fields_ = dict()
        for field in fields:
            if field not in v:
                raise ValueError(f"must contain a {field} field")

            fields_.update({field.replace("-", "_"): v[field]})

        fields_.update({"date": parse(v["date"])})

        return HTTPHeaders(**fields_)
