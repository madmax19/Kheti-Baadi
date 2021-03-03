from flask import Flask, request, jsonify
from app import app, db
from models import *
from query3 import query3
from query4 import query4
from query6 import query6
import json
import os
import random
import smtplib


@app.route("/")
def home():
    return "Home"


@app.route("/fetchr", methods=['GET'])
def fetchr():
    res = Resources.query.all()
    msg = {"status": "success", "msg": {
        "money": res.rmoney_spent,
        "product": res.rproduct_name,
        "quantity": res.rquantity,
    }}
    return jsonify(msg)


@app.route("/fetchy", methods=['GET'])
def fetchy():
    res = Yield.query.all()
    msg = {"status": "success", "msg": {
        "crop_quantity": res.ycrop_quantity,
        "crop_name": res.ycrop_name,
        "year": res.ycrop_year,
    }}
    return jsonify(msg)


@app.route("/login", methods=['POST'])
def login():
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))

    rmoney_spent = request_data['money_spent']
    rproduct_name = request_data['product_name']
    rquantity = request_data['resources_quantity']

    ycrop_name = request_data['crop']
    ycrop_quantity = request_data['crop_quantity']
    ycrop_year = request_data['crop_year']
    note = request_data['note']
    msg = ""
    if ycrop_name and ycrop_quantity and ycrop_name:
        y = Yield()
        y.ycrop_name = ycrop_name
        y.ycrop_quantity = ycrop_quantity
        y.ycrop_year = ycrop_year
        y.note = note

    r = Resources()
    r.rmoney_spent = rmoney_spent
    r.rproduct_name = rproduct_name
    r.rquantity = rquantity

    msg = {"status": "success"}
    return jsonify(msg)


def change(sentence):
    str = "around me"
    if(str in sentence):
        return sentence.replace(str, "")
    return sentence


@app.route('/web', methods=['POST'])
def scrape():
    msg = ""
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))

    sentence = request_data['sentence'].lower()
    if(("where" in sentence and ("find" in sentence or "buy" in sentence)) or "search" in sentence):
        sentence = change(sentence)
        html = query3.make_request(sentence)
        data = query3.parse_content(html)
        if data:
            msg = {"status": {"type": "success", "data": 3, "message": data}}
        else:
            msg = {"status": {"type": "failure", "message": "Missing Data"}}
        return jsonify(msg)

    elif("retailers" in sentence and ("which" in sentence or "who" in sentence)):
        sentence = change(sentence)

        html = query4.make_request(sentence)
        data = query4.parse_content(html)
        if data:
            msg = {"status": {"type": "success", "data": 4, "message": data}}
        else:
            msg = {"status": {"type": "failure", "message": "Missing Data"}}
        return jsonify(msg)

    elif("what" in sentence and "price" in sentence and "mandi" in sentence):
        sentence = change(sentence)

        html = query6.make_request()
        data = query6.parse_content(html)
        if data:
            msg = {"status": {"type": "success", "data": 6, "message": data}}
        else:
            msg = {"status": {"type": "failure", "message": "Missing Data"}}
        return jsonify(msg)

    elif("news" in sentence):
        sentence = change(sentence)
        html = news.make_request()
        data = news.parse_content(html)
        if data:
            msg = {"status": {"type": "success", "data": 0, "message": data}}
        else:
            msg = {"status": {"type": "failure", "message": "Missing Data"}}
        return jsonify(msg)
