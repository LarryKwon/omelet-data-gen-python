import os
from typing import Dict, List, Optional, TypedDict

class KakaoAPIInterface:
    api_url: str = os.getenv('KAKAO_API_URL')
    api_key: str = os.getenv('KAKAO_API_KEY')

    category_group_code = {
        'MT1': '대형마트',
        'CS2': '편의점',
        'PS3': '어린이집, 유치원',
        'SC4': '학교',
        'AC5': '학원',
        'PK6': '주차장',
        'OL7': '주유소, 충전소',
        'SW8': '지하철역',
        'BK9': '은행',
        'CT1': '문화시설',
        'AG2': '중개업소',
        'PO3': '공공기관',
        'AT4': '관광명소',
        'AD5': '숙박',
        'FD6': '음식점',
        'CE7': '카페',
        'HP8': '병원',
        'PM9': '약국',
    }

    class Query(TypedDict):
        query: Optional[str]
        category_group_code: Optional[str]
        x: Optional[str]
        y: Optional[str]
        radius: Optional[int]
        rect: Optional[str]
        page: Optional[int]
        size: Optional[int]
        sort: str

    class SameName(TypedDict):
        region: List[str]
        keyword: str
        selected_region: str

    class Meta(TypedDict):
        total_count: int
        pageable_count: int
        is_end: bool
        same_name: 'KakaoAPIInterface.SameName'

    class Document(TypedDict):
        id: str
        place_name: str
        category_name: str
        category_group_code: str
        category_group_name: str
        phone: str
        address_name: str
        road_address_name: str
        x: str
        y: str
        place_url: str
        distance: str

    class Response(TypedDict):
        meta: 'KakaoAPIInterface.Meta'
        documents: List['KakaoAPIInterface.Document']