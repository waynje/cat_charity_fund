from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import DonationCharityBase


class Donation(DonationCharityBase):
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_user'
    ))
    comment = Column(Text)