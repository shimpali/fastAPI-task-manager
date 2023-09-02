from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Common logic to be shared by all models
    """
    pass


class IDModelMixin(BaseModel):
    id: int
