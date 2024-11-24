from pydantic import BaseModel


class UrlModel(BaseModel):
    url_username : str