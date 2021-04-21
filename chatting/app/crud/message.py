from fastapi import BackgroundTasks, status, Request

from sqlalchemy.orm import Session

from app import models, schemas
from app.utils import auth, pagination


async def get_message_list(request: Request, db: Session, room_id: int, user_id: int, page: int, page_size: int):
    messages = db.query(models.Message).filter(models.Message.room_id == room_id)
    ps_messages = await pagination.paginate(messages, page, page_size)

    returning_value = await pagination.generate_next_or_prev_url(ps_messages.count(), page, page_size, str(request.url))

    return schemas.MessageListSchema(
        **returning_value,
        results=await pagination.get_results(ps_messages, schemas.MessageSchema)
    )


async def create_message(reqeust: Request, db: Session, room_id: int, user_id: int, data: schemas.MessageCreateSchema):
    data.sender_id = user_id
    # data.receiver_id = receiver_id
    message = models.Message(**data.dict())
    db.add(message)
    db.commit()
    return data