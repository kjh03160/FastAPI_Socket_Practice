from sqlalchemy import Column, Integer, String, UniqueConstraint, Enum, ForeignKey, types, UniqueConstraint, Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Date, DateTime, Text, Boolean, SmallInteger
from sqlalchemy.orm import relationship, backref

import uuid
import enum
from app.database import Base

class IntEnum(types.TypeDecorator):
    impl = Integer()

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype


class TemplateStatusChoices(enum.Enum):
    DISABLED = 0
    ENABLED = 1


def gen_username():
    return uuid.uuid4().hex


users = Table('user_room_r',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('room_id', Integer, ForeignKey('chatting_rooms.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(String(50), unique=True, nullable=False)
    username = Column(postgresql.UUID(as_uuid=True), default=gen_username, unique=True)
    password = Column(String(128), nullable=False)
    nickname = Column(String(30), nullable=True)

    # # last_message foreign key
    # # use_alter=True along with name='' adds this foreign key after message has been created to avoid circular dependency
    # last_message_id = Column(Integer, ForeignKey("messages.id", 
    #                                                 use_alter=True, 
    #                                                 name='fk_user_last_message_id', 
    #                                                 ondelete="SET NULL"))
    # # last_message - message one-to-one relationship
    # # set post_update=True to avoid circular dependency during
    # last_message = relationship("Message", backref="+", uselist=False, foreign_keys=last_message_id, post_update=True)

    rooms = relationship('ChattingRoom',secondary=users, backref='users')

    create_dt = Column(DateTime(timezone=True), server_default=func.now())
    update_dt = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())
    

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    sender = relationship("User", backref="send_messages", foreign_keys=sender_id)
    
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    receiver = relationship("User", backref="receive_messages", foreign_keys=receiver_id)

    room_id = Column(Integer, ForeignKey("chatting_rooms.id", ondelete="SET NULL"))
    room = relationship("ChattingRoom", backref="messages", foreign_keys=room_id)

    create_dt = Column('create_dt', DateTime(timezone=True),  server_default=func.now())
    read_dt = Column('read_dt', DateTime(timezone=True), nullable=True)


class ChattingRoom(Base):
    __tablename__ = "chatting_rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    create_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    create_user = relationship("User", backref="create_rooms", foreign_keys=create_user_id)