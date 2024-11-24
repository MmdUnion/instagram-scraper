
import logging
import time
from typing import Union

import urllib3
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from plugins.assistant.other_methods import (parse_json, return_proxy_url,
                                             url_isvalid)
from plugins.database.db import Base, SessionLocal, create_item, engine
from plugins.model.error import ErrorValidation
from plugins.model.url import UrlModel
from plugins.schema.url import CarouselSchema, ProfileSchema, StorySchema
from plugins.scraper.insta import InstaScraper

app = FastAPI(title="Instagram Downloader", description="Download anything from instagram such as (post, story, igtv, video, carousel and etc)")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

logging.basicConfig(filemode="a", filename="bot.log")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    



@app.get("/api/v1/media", response_model=Union[ProfileSchema, StorySchema, CarouselSchema, ErrorValidation])
async def get_media(item: UrlModel = Depends(), db: Session = Depends(get_db)):
    raw_url = item.url_username
    url_data = url_isvalid(raw_url)
    load_raw_json = None
    status = 404
    if url_data:
        get_type = url_data['type']
        get_key = url_data['key']
        get_proxy = return_proxy_url()
        get_insta = InstaScraper(proxy=get_proxy)
        load_raw_json = None

        if get_type in ['p', 'reel', 'tv']:
            load_raw_json = await get_insta.get_post_info(get_key)
            if load_raw_json:
                load_raw_json['__type__'] = "user_post"

        elif get_type == "stories":
            load_raw_json = await get_insta.get_story_info(get_key)
            if load_raw_json:
                load_raw_json['__type__'] = "user_story"

        elif get_type == "username":
            load_raw_json = await get_insta.get_profile_info(get_key)
            if load_raw_json:
                load_raw_json['__type__'] = "user_profile"


        if load_raw_json.get('status') != 500:
            if (load_raw_json.get("data") and load_raw_json.get("data").get("shortcode_media")) or (load_raw_json.get("data") and load_raw_json.get("data").get("user")):
                parse_data = parse_json(load_raw_json)
                if parse_data:
                    get_type = parse_data['type']
                    return_class = None
                    if get_type == "user_profile":
                        # profile picture
                        return_class = ProfileSchema(**parse_data)
                    elif get_type == "user_story":
                        # story media
                        return_class = StorySchema(**parse_data)
                    elif get_type == "user_post":
                        # carousel
                        return_class = CarouselSchema(**parse_data)

                    create_item(db, {"url":raw_url, "parse_url":str(url_data), "status":"success", "created_at":int(time.time())})

                    if return_class:
                        return return_class
        else:
            status = 500

    create_item(db, {"url":raw_url, "parse_url":f"{str(url_data)} ||||| {str(load_raw_json)}", "status":"fail", "created_at":int(time.time())})

    error_detail = {
        "message":"The url or username is not valid!",
        "status":"fail"
        }

    raise HTTPException(status_code=status, detail=error_detail)

