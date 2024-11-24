import re
from settings import HTTP_PROXY_URL

def url_isvalid(url):
    # match igtv, real, videos, photos
    match_post = re.findall(r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/((?:p|reel|tv))\/([^/?#&]+).*", url)

    # match stories only.
    match_stories = re.findall(r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(stories)\/([A-Za-z0-9-_.]{0,29})\/([0-9]+).*", url)

    # match highlites
    # match_highlite = re.findall(r"((?:https?:\/\/)?(?:www\.)?instagram\.com\/(stories)\/(highlights)\/([0-9]+)).*", url)

#     match_highlite_pattern_2 = re.findall(r"((?:https?:\/\/)?(?:www\.)?instagram\.com\/(s)\/([A-Za-z0-9-_.]{10,100})).*", url)

    # match username by url only
    match_username_pattern1 = re.findall(r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/([A-Za-z0-9-_.]{0,29}).*", url)

    # match username by @ or not 
    match_username_pattern2 = re.findall(r"^(?:@?([A-Za-z0-9-_.]{0,29}))$", url)


    data_found = {}

    if match_post and len(match_post) == 1 and len(match_post[0]) == 2:
        post_type, post_key = match_post[0]
        data_found['type'] = post_type
        data_found['key'] = post_key

    elif match_stories and len(match_stories) == 1 and len(match_stories[0]) == 3:
        post_type, username, post_key = match_stories[0]
        if username != "highlights":
            data_found['type'] = post_type
            data_found['key'] = post_key
            data_found['username'] = username

    elif match_username_pattern1 and len(match_username_pattern1) == 1:
        username = match_username_pattern1[0]
        data_found['type'] = "username"
        data_found['key'] = username


    elif match_username_pattern2 and len(match_username_pattern2) == 1:
        username = match_username_pattern2[0]
        data_found['type'] = "username"
        data_found['key'] = username

    return data_found





def convert_key2id(code):
    charmap = {
        'A': '0',
        'B': '1',
        'C': '2',
        'D': '3',
        'E': '4',
        'F': '5',
        'G': '6',
        'H': '7',
        'I': '8',
        'J': '9',
        'K': 'a',
        'L': 'b',
        'M': 'c',
        'N': 'd',
        'O': 'e',
        'P': 'f',
        'Q': 'g',
        'R': 'h',
        'S': 'i',
        'T': 'j',
        'U': 'k',
        'V': 'l',
        'W': 'm',
        'X': 'n',
        'Y': 'o',
        'Z': 'p',
        'a': 'q',
        'b': 'r',
        'c': 's',
        'd': 't',
        'e': 'u',
        'f': 'v',
        'g': 'w',
        'h': 'x',
        'i': 'y',
        'j': 'z',
        'k': 'A',
        'l': 'B',
        'm': 'C',
        'n': 'D',
        'o': 'E',
        'p': 'F',
        'q': 'G',
        'r': 'H',
        's': 'I',
        't': 'J',
        'u': 'K',
        'v': 'L',
        'w': 'M',
        'x': 'N',
        'y': 'O',
        'z': 'P',
        '0': 'Q',
        '1': 'R',
        '2': 'S',
        '3': 'T',
        '4': 'U',
        '5': 'V',
        '6': 'W',
        '7': 'X',
        '8': 'Y',
        '9': 'Z',
        '-': '$',
        '_': '_'
    }

    id = ""
    for letter in code:
        id += charmap[letter]

    alphabet = list(charmap.values())
    number = 0
    for char in id:
        number = number * 64 + alphabet.index(char)

    return number



def convert_id2key(number):
    charmap = {
        '0': 'A',
        '1': 'B',
        '2': 'C',
        '3': 'D',
        '4': 'E',
        '5': 'F',
        '6': 'G',
        '7': 'H',
        '8': 'I',
        '9': 'J',
        'a': 'K',
        'b': 'L',
        'c': 'M',
        'd': 'N',
        'e': 'O',
        'f': 'P',
        'g': 'Q',
        'h': 'R',
        'i': 'S',
        'j': 'T',
        'k': 'U',
        'l': 'V',
        'm': 'W',
        'n': 'X',
        'o': 'Y',
        'p': 'Z',
        'q': 'a',
        'r': 'b',
        's': 'c',
        't': 'd',
        'u': 'e',
        'v': 'f',
        'w': 'g',
        'x': 'h',
        'y': 'i',
        'z': 'j',
        'A': 'k',
        'B': 'l',
        'C': 'm',
        'D': 'n',
        'E': 'o',
        'F': 'p',
        'G': 'q',
        'H': 'r',
        'I': 's',
        'J': 't',
        'K': 'u',
        'L': 'v',
        'M': 'w',
        'N': 'x',
        'O': 'y',
        'P': 'z',
        'Q': '0',
        'R': '1',
        'S': '2',
        'T': '3',
        'U': '4',
        'V': '5',
        'W': '6',
        'X': '7',
        'Y': '8',
        'Z': '9',
        '$': '-',
        '_': '_'
    }

    alphabet = list(charmap.keys())
    base = 64
    key = ""

    while number > 0:
        remainder = number % base        
        key = charmap[alphabet[remainder]] + key
        number = number // base

    return key





def return_proxy_url():
    return HTTP_PROXY_URL



def parse_json(json_response):
    get_type = json_response['__type__']

    return_data = {}

    if get_type == "user_profile":
        # its json of profile picture
        user_profile = json_response.get("data").get("user")

        user_id = user_profile.get("id")
        is_verified = user_profile.get("is_verified")
        is_private = user_profile.get("is_private")
        profile_picture_hd = user_profile.get("profile_pic_url_hd")
        username = user_profile.get("username")
        full_name = user_profile.get("full_name")
        post_count = user_profile.get("edge_owner_to_timeline_media")

        if post_count:
            post_count = post_count.get("count")
        else:
            post_count = None
        
        biography = user_profile.get("biography")
        external_bio_url = user_profile.get("external_url")
        follower_count = user_profile.get("edge_followed_by").get("count")
        following_count = user_profile.get("edge_follow").get("count")
        is_business_account = user_profile.get("is_business_account")
        is_professional_account = user_profile.get("is_professional_account")
        profile_picture_thumbnail = user_profile.get("profile_pic_url")


        return {"owner":{
            "user_id": user_id, 
            "is_verified": is_verified,
            "is_private": is_private,
            "profile_picture_hd": profile_picture_hd,
            "username": username,
            "full_name": full_name,
            "post_count": post_count,
            "biography": biography,
            "external_bio_url": external_bio_url,
            "follower_count": follower_count,
            "following_count": following_count,
            "is_business_account": is_business_account,
            "is_professional_account": is_professional_account,
            "profile_picture_thumbnail": profile_picture_thumbnail 
            }, "type":"user_profile", "status": "ok"}

    elif get_type == "user_post":
        user_post = json_response.get("data").get("shortcode_media")
        json_response_model = []
        # its json of story

        is_carousel = user_post.get("edge_sidecar_to_children")


        if not is_carousel:
            # one file
            is_video = user_post.get("is_video")
            if is_video:
                url = user_post.get("video_url")
            else:
                url = user_post.get("display_resources")[-1]['src']

            thumbnail = user_post.get("display_url")

            json_response_model.append({
                    "url":url,
                    "thumbnail":thumbnail,
                    "is_video":is_video
                    })

        else:
            # multiple files
            get_carousel = is_carousel.get("edges")
            for item in get_carousel:
                get_item = item.get("node")

                is_video = get_item.get("is_video")
                if is_video:
                    url = get_item.get("video_url")
                else:
                    url = get_item.get("display_resources")[-1]['src']

                thumbnail = get_item.get("display_url")

                json_response_model.append({
                    "url":url,
                    "thumbnail":thumbnail,
                    "is_video":is_video
                    })

        return_data.update({"media": json_response_model, "type":"user_post"})
        other_data = user_post





    elif get_type == "user_story":
        user_story = json_response.get("data").get("shortcode_media")
        # its json of story
        is_video = user_story.get("is_video")
        if is_video:
            url = user_story.get("video_url")
        else:
            url = user_story.get("display_resources")[-1]['src']

        if not url:
            # currently story video not supported!
            url = user_story.get("display_resources")[-1]['src']
            
        thumbnail = user_story.get("display_url")
        other_data = user_story
        return_data.update({
            "media":[{
                "url":url, 
                "thumbnail":thumbnail, 
                "is_video":is_video
            }], 
        "type":"user_story"})



    comment_count = other_data.get("edge_media_to_comment")
    if comment_count:
        comment_count = comment_count.get("count")
    else:
        comment_count = None



    like_count = other_data.get("edge_media_preview_like")
    if like_count:
        like_count = like_count.get("count")
    else:
        like_count = None


    location = other_data.get("location")
    if location:
        location = location.get("name")
    else:
        location = None

    
    caption = other_data.get("edge_media_to_caption") and other_data.get("edge_media_to_caption").get("edges")
    if caption:
        caption = caption[0].get("node").get("text")
    else:
        caption = None



    owner_data = other_data.get("owner")
    user_id = owner_data.get("id")
    is_verified = owner_data.get("is_verified")
    is_private = owner_data.get("is_private")
    profile_picture_thumbnail = owner_data.get("profile_pic_url")
    username = owner_data.get("username")
    full_name = owner_data.get("full_name")
    post_count = owner_data.get("edge_owner_to_timeline_media")
    if post_count:
        post_count = post_count.get("count")
    else:
        post_count = None
    



    return_data.update({
        "caption": caption, 
        "location":location,
        "like_count":like_count,
        "comment_count":comment_count,
        "owner":{
            "user_id": user_id, 
            "is_verified": is_verified,
            "is_private": is_private,
            "profile_picture_thumbnail": profile_picture_thumbnail,
            "username": username,
            "full_name": full_name,
            "post_count": post_count,
            },
        "status": "ok"
        })
    return return_data