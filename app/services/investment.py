from datetime import datetime

from app.models.base import PreBaseDonationCharity


def execute_investment_process(
        target: PreBaseDonationCharity,
        sources: list[PreBaseDonationCharity]
) -> list[PreBaseDonationCharity]:
    changed = []
    for source in sources:
        investing_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        changed.append(source)
        for obj in (target, source):
            obj.invested_amount += investing_amount
            if fully_invested := obj.invested_amount == obj.full_amount:
                obj.fully_invested = fully_invested
                obj.close_date = datetime.now()
        if target.fully_invested:
            break

    return changed
