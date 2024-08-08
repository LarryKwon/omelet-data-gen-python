# getAddressName.py
from typing import Dict

from sqlalchemy.orm import Session
from sqlalchemy import select, distinct
from models import RoadAddressCode

async def unique_sigungu(session: Session, sido_name: str):
    result = await session.execute(
        select(RoadAddressCode.sigungu_name)
        .where(RoadAddressCode.sido_name == sido_name)
        .distinct(RoadAddressCode.sigungu_name)
    )
    return [row.sigungu_name for row in result]

async def unique_address(session: Session, query: Dict[str, str]):
    sido_name = query['sido_name']
    sigungu_name = query.get('sigungu_name')
    stmt = select(
        RoadAddressCode.sido_name,
        RoadAddressCode.sigungu_name,
        RoadAddressCode.address_name
    ).distinct(RoadAddressCode.address_name)
    if sigungu_name:
        stmt = stmt.where(
            RoadAddressCode.sido_name == sido_name,
            RoadAddressCode.sigungu_name == sigungu_name
        )
    else:
        stmt = stmt.where(RoadAddressCode.sido_name == sido_name)
    result = await session.execute(stmt)
    return [
        {'sido_name': row.sido_name, 'sigungu_name': row.sigungu_name, 'address_name': row.address_name}
        for row in result
    ]