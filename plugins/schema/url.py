from typing import List, Union

from pydantic import BaseModel


class BaseOwnerSchema(BaseModel):
    user_id : int
    is_verified : bool
    is_private : bool
    profile_picture_thumbnail : str
    username : str
    full_name : str
    post_count : int


class OwnerSchema(BaseOwnerSchema):
    biography : Union[str, None]
    external_bio_url : Union[str, None]
    follower_count : int
    following_count : int
    is_business_account : bool
    is_professional_account : bool
    profile_picture_hd : str



class BaseStoryMediaSchema(BaseModel):
    url: str
    thumbnail : str
    is_video : bool



class BasePostMediaSchema(BaseModel):
    url: str
    thumbnail : str
    is_video : bool


# ----------------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------





class StorySchema(BaseModel):
    media: List[BaseStoryMediaSchema]
    owner : BaseOwnerSchema
    location : Union[str, None]
    type : str
    status : str



class CarouselSchema(BaseModel):
    media: List[BasePostMediaSchema]
    location : Union[str, None]
    caption : Union[str, None]
    comment_count : Union[int, None]
    like_count : Union[int, None]
    owner : BaseOwnerSchema
    type : str
    status : str



class ProfileSchema(BaseModel):
    owner : OwnerSchema
    type : str
    status : str
