from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import PreBaseDonationCharity


class Donation(PreBaseDonationCharity):
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_user'
    ))
    comment = Column(Text)

    def __repr__(self) -> str:
        return f'Фонд - {self.user_id}, {self.comment}' + super().__repr__()
