from pydantic import BaseModel


class ErrorValidation(BaseModel):
    message : str = "The url or username is not valid!"
    status : str