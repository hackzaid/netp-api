from api.app import ma
from marshmallow import post_load


class BaseResponse(ma.Schema):
    class Meta:
        ordered = True

    message = ma.String()
    has_error = ma.Boolean()
    redirect_url = ma.String()

    @post_load()
    def make_request(self, data):
        return self.BaseResponse(**data)
