from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
import math
from flask import Flask, flash, request, redirect, url_for

from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('sellerReviewOutput', __name__)


@bp.route('/sellerReviewOutput/<int:sellerId>/<int:orderBy>', methods=["GET", "POST"])
def sellerReviewOutput(sellerId, orderBy):
    if orderBy == None:
        orderBy = 5
    else:
        orderBy = int(orderBy)
    
    activePage = request.args.get('activePage')
    if activePage == None:
        activePage = 1
    else:
        activePage = int(activePage)
    if activePage == 1: 
        offset = 0
    else:
        offset = (activePage-1)*10
    allSellerReviews = SellerReview.get_by_sellerId(sellerId, orderBy)
    total = len(allSellerReviews)

    seller_reviews = SellerReview.getOff(sellerId, offset, orderBy)
    pages = math.ceil(total/10)
    avgRating = SellerReview.getAverageRating(sellerId)
    num = SellerReview.getNumberRatings(sellerId)
    top3 = SellerReview.getTop3(sellerId, orderBy)
    return render_template('sellerReviewOutput.html', top3=top3, seller_reviews=seller_reviews, activePage = activePage, pages = pages, sellerId=sellerId, orderBy=orderBy, avgRating=avgRating, num=num)

@bp.route('/addSellerUpvotes/<int:userId>/<int:sellerId>/<int:orderBy>', methods=["GET", "POST"])
def addSellerUpvotes(userId, sellerId, orderBy):
    SellerReview.addUpvotes(userId, sellerId)
    return redirect(url_for('sellerReviewOutput.sellerReviewOutput', sellerId=sellerId, orderBy=orderBy))

    
    
    
    
    
    


    
    
    
    
    
    
