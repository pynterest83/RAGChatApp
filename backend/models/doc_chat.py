from sqlalchemy import Column, Text, Integer, ForeignKey
from utils.db import Base

class DocChat(Base):
    __tablename__ = "doc_chat"

    group_id = Column(Text, primary_key=True, index=True)
    doc_name = Column(Text, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))