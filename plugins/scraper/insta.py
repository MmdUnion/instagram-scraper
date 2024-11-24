import logging

import aiohttp

from plugins.assistant.other_methods import convert_id2key
from settings import MAX_RETRY_COUNT, HTTP_HEADERS



class InstaScraper:
    def __init__(self, proxy=None):
        self.proxy_url = proxy

    async def get_profile_info(self, username):
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        HTTP_HEADERS['x-asbd-id'] = '198387'
        HTTP_HEADERS['x-ig-app-id'] = '936619743392459'
        return (await self.send_request(url)) 

    async def get_post_info(self, post_key):
        url = 'https://www.instagram.com/graphql/query/?query_hash=9f8827793ef34641b2fb195d4d41151c&variables={"shortcode":"%s"}' % (post_key, )

        return (await self.send_request(url)) 



    async def get_story_info(self, post_key):
        get_shortcode_by_id = convert_id2key(int(post_key))
        url = 'https://www.instagram.com/graphql/query/?query_hash=9f8827793ef34641b2fb195d4d41151c&variables={"shortcode":"%s"}' % (get_shortcode_by_id, )


        return (await self.send_request(url)) 


    async def send_request(self, url, max_retry=0):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=self.proxy_url, headers=HTTP_HEADERS, ssl=False) as response:
                    json_response = await response.json()
                    if json_response.get("require_login"):
                        raise ValueError
                    return json_response
        except:
            logging.exception("Error aiohttp")

        if max_retry < MAX_RETRY_COUNT:
            return await self.send_request(url, max_retry+1)
        else:
            return {"status": 500}



