from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel


app = FastAPI()


class MessageIn(BaseModel):
    author: str
    text: str


class MessagePatch(BaseModel):
    author: str | None = None
    text: str | None = None


class Message(BaseModel):
    id: int
    author: str
    text: str


messages: list[Message] = []
next_id = 1


def find_message(message_id: int) -> Message:
    for message in messages:
        if message.id == message_id:
            return message
    raise HTTPException(status_code=404, detail="Message not found")


@app.get("/messages", response_model=list[Message])
def list_messages() -> list[Message]:
    return messages


@app.post("/messages", response_model=Message, status_code=201)
def create_message(payload: MessageIn) -> Message:
    global next_id
    message = Message(id=next_id, author=payload.author, text=payload.text)
    messages.append(message)
    next_id += 1
    return message


@app.get("/messages/{message_id}", response_model=Message)
def get_message(message_id: int) -> Message:
    return find_message(message_id)


@app.put("/messages/{message_id}", response_model=Message)
def replace_message(message_id: int, payload: MessageIn) -> Message:
    message = find_message(message_id)
    message.author = payload.author
    message.text = payload.text
    return message


@app.patch("/messages/{message_id}", response_model=Message)
def patch_message(message_id: int, payload: MessagePatch) -> Message:
    message = find_message(message_id)
    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(message, field, value)

    return message


@app.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int) -> Response:
    messages.remove(find_message(message_id))
    return Response(status_code=204)
