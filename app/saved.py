from flask import render_template
from flask_login import current_user
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for
from .models.product import Product
from .models.cart import Cart
from .models.user import User
from .models.saved import Saved
from flask import current_app 
from flask import Blueprint
bp = Blueprint('saved', __name__)

@bp.route('/saved')
def saved():
    if current_user.is_authenticated:
        userId = current_user.id
        user_saved = Saved.get(userId)
    else:
        userId = None
        user_saved = None

    return render_template('saved.html', userId=userId, user_saved = user_saved)

@bp.route('/savedAddProduct/<int:productId>', methods=["GET", "POST"])
def savedAddProduct(productId):
    if current_user.is_authenticated:
        userId = current_user.id
        if Saved.check(userId, productId): 
            Cart.remove_from_cart(userId, productId)
        else: 
            Saved.add_to_saved(userId, productId)
        user_saved = Saved.get(userId)
        return render_template('saved.html', userId=userId, user_saved=user_saved, productId = productId)
    else:
        return render_template('notLoggedIn.html')

@bp.route('/savedRemoveProduct/<int:productId>', methods=["GET", "POST"])
def savedRemoveProduct(productId):
    userId = current_user.id
    user_saved = Saved.remove_from_saved(userId, productId)
    user_saved = Saved.get(userId)
    return render_template('saved.html', userId=userId, user_saved=user_saved, productId = productId)

@bp.route('/savedSaveForLater/<int:productId>', methods=["GET", "POST"])
def savedSaveForLater(productId):
    userId = current_user.id
    if Saved.check(userId, productId): 
        Cart.remove_from_cart(userId, productId)
    else: 
        Saved.add_to_saved(userId, productId)
        Cart.remove_from_cart(userId, productId)
    user_saved = Saved.get(userId)
    return render_template('saved.html', userId=userId, user_saved=user_saved, productId = productId)
