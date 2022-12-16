from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from api import ma, db
from api.auth import token_auth
from api.models.products.productModel import Product, Category


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        model = Product

    id = ma.auto_field(dump_only=True)
    productName = ma.String(required=True)
    categoryID = ma.String(required=True)
    productCategory = ma.Nested('CategorySchema', many=True)


class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        model = Category

    id = ma.auto_field(dump_only=True)
    catName = ma.String(required=True)
    catDetails = ma.String(required=True)
