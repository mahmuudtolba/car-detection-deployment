# accept the input params/data payload
# output the score, class, latency

from pydantic import BaseModel
from pydantic import EmailStr, HttpUrl 

class ImageDataInput(BaseModel):
    url: list[HttpUrl]
    user_id: EmailStr


class ImageDataOutput(BaseModel):
    model_name: str
    url: list[HttpUrl]
    image: list[str]
    scores: list[float]
    prediction_time: int





