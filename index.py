# index.py
import asyncio
from typing import List, Dict
from sqlalchemy.orm import Session
from getAddressName import unique_address, unique_sigungu
from apiRequest import KakaoAPI
from makeCsv import create_excel, create_csv
from kakaoAPI.interface import KakaoAPIInterface


async def set_search_target(
        session: Session,
        sido_name: str,
        keyword: str,
        category_code: str,
        sigungu_name: str = None
) -> List[KakaoAPIInterface.Query]:
    db_query = {'sido_name': sido_name}
    if sigungu_name:
        db_query['sigungu_name'] = sigungu_name

    road_address_names = [
        f"{address['sido_name']} {address['sigungu_name']} {address['address_name']}"
        for address in await unique_address(session, db_query)
    ]

    search_target_list = [f"{address} {keyword}" for address in road_address_names]

    return [
        {
            'query': address,
            'category_group_code': category_code,
            'sort': 'accuracy'
        }
        for address in search_target_list
    ]


async def main(
        session: Session,
        sido_name: str,
        keyword: str,
        category_code: str,
        sigungu_name: str = None
):
    query = await set_search_target(session, sido_name, keyword, category_code, sigungu_name)
    api_batch_size = 5
    api_batch_count = (len(query) + api_batch_size - 1) // api_batch_size
    total_result: List[KakaoAPIInterface.Document] = []
    for i in range(api_batch_count):
        batch_query = query[i * api_batch_size:(i + 1) * api_batch_size]
        batch_result = await asyncio.gather(*(
            KakaoAPI.get_keyword_search(q) for q in batch_query
        ))
        total_result.extend(doc for result in batch_result for doc in result['documents'])
    create_excel(total_result, f'./output/xlsx/{keyword}_{sido_name}_{sigungu_name}.xlsx')
    create_csv(total_result, f'./output/csv/{keyword}_{sido_name}_{sigungu_name}.csv')


async def main_wrap(
        session: Session,
        sido_name: str,
        keyword: str,
        category_code: str,
        sigungu_name: str = None
):
    if sigungu_name is None:
        sigungu_name_list = await unique_sigungu(session, sido_name)
        print(sigungu_name_list)
        for sigungu in sigungu_name_list:
            if sigungu:
                await main(session, sido_name, keyword, category_code, sigungu)
                print('complete: ', sigungu)
    else:
        await main(session, sido_name, keyword, category_code, sigungu_name)
