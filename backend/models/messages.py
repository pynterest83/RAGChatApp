from sqlalchemy import Column, Text, Integer, ForeignKey, BigInteger
from utils.db import Base

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(BigInteger, primary_key=True, index=True)
    group_id = Column(Text, ForeignKey('doc_chat.group_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)