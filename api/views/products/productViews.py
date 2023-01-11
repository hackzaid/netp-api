from apifairy.decorators import other_responses
from flask import Blueprint, abort, g
from apifairy import authenticate, body, response
from flask_login import current_user

from api import db
from api.app import authorize
from api.models.products.productModel import Product, Category
from api.schemas.products.productSchema import ProductSchema, CategorySchema
from api.auth import token_auth, group_required
from api.decorators import paginated_response


product = Blueprint('product', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@product.route('/products/all', methods=['GET'])
@authenticate(token_auth)
@authorize.has_role('moderator')
@paginated_response(product_schema)
def get_products():
    """Get All Products"""
    user = token_auth.current_user()
    print(g.flask_httpauth_user)
    return Product.select()


@product.route('/category/all', methods=['GET'])
@authenticate(token_auth)
@authorize.has_role('admin')
@paginated_response(category_schema)
def get_categories():
    """Get All Categories"""
    return Category.select()


@product.route('/category', methods=['POST'])
@body(category_schema)
@response(category_schema)
def add_category(args):
    """ Add Category"""
    category = Category(**args)
    db.session.add(category)
    db.session.commit()
    return category


@product.route('/product', methods=['POST'])
@body(product_schema)
@response(product_schema)
def add_product(args):
    """ Add Product"""

    products = Product(**args)
    db.session.add(products)
    db.session.commit()
    return products
