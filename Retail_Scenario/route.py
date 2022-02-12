from flask import Blueprint
from Utilities.db import *
from Retail_Scenario.controller import *
bp = Blueprint("bp",__name__)

@bp.route("/")
def hello_world():
    return "<H1> PROJECT WITH PATRA <H1>"


bp.route("/login", methods=['POST'])(retail_login)

bp.route("/orderDetails", methods=['GET'])(order_details)

bp.route("/place_order", methods=['POST'])(place_order)

bp.route("/cancel_order", methods=['DELETE'])(delete_order)

bp.route("/read", methods=['GET'])(read_products)

bp.route("/reads", methods=['GET'])(array_order_details)
