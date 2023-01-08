from api.schemas.baseResponse import BaseResponse
from api.app import ma


class ApplicationInfoSchema(ma.Schema):
    class Meta:
        ordered = True
