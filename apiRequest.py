import os
import aiohttp
from typing import Dict, Any
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

class KakaoAPI:
    @staticmethod
    def request_to_addr_api(api_url: str, confm_key: str):
        async def wrapper(query: Dict[str, Any]) -> Dict[str, Any]:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(
                        api_url,
                        headers={'Authorization': f'KakaoAK {confm_key}'},
                        params=query
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
                except aiohttp.ClientError as e:
                    raise Exception(f"Error: {e}")
        return wrapper

    @classmethod
    async def get_keyword_search(cls, query: Dict[str, Any]) -> Dict[str, Any]:
        api_url = os.getenv('KAKAO_API_URL')
        api_key = os.getenv('KAKAO_API_KEY')
        if api_url is None or api_key is None:
            raise Exception('API URL or API Key is not defined')
        # print(query)
        try:
            result = await cls.request_to_addr_api(api_url, api_key)(query)
            return result
        except aiohttp.ClientResponseError as e:
            if getattr(e, 'status', None) == 429:  # Too Many Requests
                return await cls.get_keyword_search(query)
            raise e
        except Exception:
            return await cls.get_keyword_search(query)

    @classmethod
    async def get_total_count_of_query(cls, query: Dict[str, Any]) -> int:
        result = await cls.get_keyword_search(query)
        total_count = result['meta']['total_count']
        pageable_count = result['meta']['pageable_count']
        if pageable_count < total_count:
            print(f'There are more results than pageable count with this query: {query}')
            print(f'Total count: {total_count}, Pageable count: {pageable_count}')
        return pageable_count
