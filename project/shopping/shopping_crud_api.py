# THIS IS THE CRUD OPERATION ON ITEM_LIST TABLE => RUN THIS IN PORT 5000
# database in sqllite (local) 
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin


# init app
app = Flask (__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# just to test the initial api call
# @app.route('/', methods=['GET'])
# def get():
#    return jsonify({'msg': 'my first app call'})

# this is my current programming folder which is C:\Users\nimis\Desktop\Nimisha\projects\shopping>
basedir = os.path.abspath(os.path.dirname(__file__))
# database
# conn = sqlite3.connect("c:\\sqlite\\testdb.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..\\..\\..\\..\\..\\..\\sqlite\\testdb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize DB
db = SQLAlchemy(app) 

# init marshmellow
ma = Marshmallow(app)

# Interestingly my table is item_list, python is sensing underscore in ItemList
# ItemList Class and Model
class ItemList(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.String(255))
    item_name = db.Column(db.String(50))
    item_catg = db.Column(db.String(50))
    item_qty = db.Column(db.Integer)
    qty_type = db.Column(db.String(50))
    store = db.Column(db.String(50))
    order_type = db.Column(db.String(50))
    needed_by = db.Column(db.String(10))
    comment = db.Column(db.String(255))
    isChecked = db.Column(db.Boolean) 

    def __init__(self, create_date, item_name, item_catg, item_qty, qty_type, store, order_type, needed_by, comment, isChecked):  
        self.create_date = create_date
        self.item_name = item_name
        self.item_catg = item_catg
        self.item_qty = item_qty
        self.qty_type = qty_type
        self.store = store
        self.order_type = order_type
        self.needed_by = needed_by
        self.comment = comment
        self.isChecked = isChecked
    # __repr__ method to make every single post object is printable to the console, good practice for debug
    def __repr__(self):
        return '<Item_List %s>' % self.item_name

# create marshmellow schema based on ItemList model
class ItemSchema(ma.Schema):
    class Meta:
        fields = ("item_id", "create_date", "item_name", "item_catg", "item_qty", "qty_type", "store", "order_type", "needed_by", "comment", "isChecked")
        model = ItemList


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"

# create an item
@app.route('/item', methods=['POST'])
def add_item():
    create_date=request.json['create_date']
    item_name=request.json['item_name']
    item_catg=request.json['item_catg']
    item_qty=request.json['item_qty']
    qty_type=request.json['qty_type']
    store=request.json['store']
    order_type=request.json['order_type']
    needed_by=request.json['needed_by']
    comment=request.json['comment']
    isChecked=request.json['isChecked']

    new_item = ItemList(str(create_date),str(item_name), str(item_catg), str(item_qty), str(qty_type), str(store), str(order_type), str(needed_by), str(comment), isChecked)

    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item)

# get items
@app.route('/item', methods=['GET'])
def get_items():
    all_items = ItemList.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result)

# get one item
@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    item = ItemList.query.get(id)
    return item_schema.jsonify(item)

# update an item
@app.route('/item/<id>', methods=['PUT'])
def update_item(id):
    item = ItemList.query.get(id)
    # getdata from json
    create_date=request.json['create_date']
    item_name=request.json['item_name']
    item_catg=request.json['item_catg']
    item_qty=request.json['item_qty']
    qty_type=request.json['qty_type']
    store=request.json['store']
    order_type=request.json['order_type']
    needed_by=request.json['needed_by']
    comment=request.json['comment']
    isChecked=request.json['isChecked']

    # update data in table
    item.create_date = str(create_date)
    item.item_name = str(item_name)
    item.item_catg = str(item_catg)
    item.item_qty = str(item_qty)
    item.qty_type = str(qty_type)
    item.store = str(store)
    item.order_type = str(order_type)
    item.needed_by = str(needed_by)
    item.comment = str(comment)
    item.isChecked = isChecked
    # save the update in database
    db.session.commit()

    return item_schema.jsonify(item)

# update an item when done
@app.route('/itemdone/<id>', methods=['PUT'])
def update_done(id):
    item = ItemList.query.get(id)
    # getdata from json
    isChecked=request.json['isChecked']

    # update data in table
    item.isChecked = isChecked
    # save the update in database
    db.session.commit()

    return item_schema.jsonify(item)

# run server
if __name__ == '__main__':
    app.run(debug=True)


