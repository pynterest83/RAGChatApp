from sqlalchemy import Column, Text, Integer, ForeignKey, BigInteger
from utils.db import Base

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)  # Auto-increment primary key
    group_id = Column(Text, ForeignKey('doc_chat.group_id'), nullable=False)  # Foreign key, not nullable
    message = Column(Text, nullable=False)  # Message content, not nullable
    sender_id = Column(Integer, nullable=False)  # Sender ID, not nullable