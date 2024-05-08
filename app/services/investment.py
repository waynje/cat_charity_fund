from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.core.db import DonationCharityBase


async def get_not_closed_projects(
    session: AsyncSession,
    model_in: DonationCharityBase
) -> list[DonationCharityBase]:

    not_closed_obj = await session.execute(select(model_in).where(
        model_in.fully_invested == false()
    ).order_by('create_date'))
    return not_closed_obj.scalars().all()


async def make_investment(
    session: AsyncSession,
    obj: DonationCharityBase,
    list_obj: list[DonationCharityBase]
):

    need_to_invest = obj.full_amount

    if list_obj:
        for item in list_obj:

            if need_to_invest == item.full_amount - item.invested_amount:
                obj.invested_amount = obj.full_amount
                item.full_amount = item.full_amount
                obj.close_date = datetime.now()
                obj.fully_invested = True
                item.close_date = datetime.now()
                item.fully_invested = True
                break

            elif need_to_invest > item.full_amount - item.invested_amount:
                need_to_invest -= item.full_amount - item.invested_amount
                item.invested_amount = item.full_amount
                item.close = datetime.now()
                item.fully_invested = True

            else:
                item.invested_amount += need_to_invest
                obj.invested_amount = obj.full_amount
                obj.close_date = datetime.now()
                obj.fully_invested = True
                break
    session.commit()
    session.refresh(obj)
    return obj