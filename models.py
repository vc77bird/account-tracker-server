from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    existing_user = Column(Boolean)
    date_requested = Column(String)
    date_au_created = Column(String)
    date_training_assigned = Column(String)
    date_account_created = Column(String)
    date_account_activated = Column(String)
    date_account_inactivated = Column(String)