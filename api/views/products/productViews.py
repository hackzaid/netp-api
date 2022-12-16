from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from api.models.products.productModel import Product, Category
from api.schemas.products.productSchema import ProductSchema, CategorySchema
from api.auth import token_auth
from api.decorators import paginated_response

product = Blueprint('product', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@product.route('/products/all')
@response(product_schema)
def get_products():
    """Get All Products"""
    return Product.select()


@product.route('/category/all')
@response(category_schema)
def get_categories():
    """Get All Categories"""
    return Category.select()
