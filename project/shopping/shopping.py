# THIS IS MVC PYTHON PROGRAM FOR MAINTAIN THE SHOPPING LIST => run this in port 5001
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_paginate import Pagination, get_page_parameter, get_page_args
from werkzeug.exceptions import abort


# The global request object to access incoming request data that will be submitted via an HTML form.
# The url_for() function to generate URLs.
# The flash() function to flash a message when a request is processed.
# The redirect() function to redirect the client to a different location.
app = Flask(__name__)
app.config['SECRET_KEY']  = 'my secret key'

def get_db_connection():
    conn = sqlite3.connect("c:\\sqlite\\testdb.db")
    conn.row_factory = sqlite3.Row
    return conn

# get one contact
def get_one_item(item_id):
    conn = get_db_connection()
    item = conn.execute('select * from item_list where item_id = ?', (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item



def model_viewitem():
    try: 
        conn = get_db_connection()
        myList = conn.execute('select * from item_list').fetchall()
       

        conn.close()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return myList


def model_additem(form):
        err_msg = ""
        date_added = form['date_added']
        item = form['item_name']
        item_catg = form['item_catg']
        item_qty = form['item_qty']
        qty_type = form['qty_type']
        store = form['store']
        order_type = form['order_type']
        needed_by = form['needed_by']
        comment = form['comment']
        
        if not item or item is None:
            err_msg = "Item name is missing!"
        elif not item_catg:
            err_msg = "Item Catg is required!"
        elif not item_qty:
            err_msg = "Qty is required!"
        elif not store: 
            err_msg = "Store is required!"
        else: 
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO item_list (create_date, item_name, item_catg, item_qty, qty_type, store, order_type, needed_by, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)',
                         (date_added, item, item_catg, item_qty, qty_type, store, order_type, needed_by, comment))
                conn.commit()
                conn.close()
            except Error as e:
                err_msg = e
            finally:
                if conn:
                    conn.close()
        return err_msg

def model_edititem(form):
    err_msg = ""
    item_id = form['item_id']
    date_added = form['date_added']
    item = form['item_name']
    item_catg = form['item_catg']
    item_qty = form['item_qty']
    qty_type = form['qty_type']
    store = form['store']
    order_type = form['order_type']
    needed_by = form['needed_by']
    comment = form['comment']
    if not item or item is None:
            err_msg = "Item name is missing!"
    elif not item_catg:
            err_msg = "Item Catg is required!"
    elif not item_qty:
            err_msg = "Qty is required!"
    elif not store: 
            err_msg = "Store is required!"
    else: 
        try:
            conn = get_db_connection()
            conn.execute('UPDATE item_list SET create_date = ? , item_name = ?, item_catg = ?, item_qty = ?, qty_type = ?, store = ?, order_type = ?,  needed_by = ?, comment = ?'
                     ' WHERE item_id = ?',
                        (date_added, item, item_catg, item_qty, qty_type, store, order_type, needed_by, comment, item_id))
            conn.commit()
            conn.close()
        except Error as e:
            err_msg = e
        finally:
            if conn:
                conn.close()
                
    return err_msg

def model_checkitem(form):
    err_msg = ""
    isChecked = form['isChecked']
    try:
        conn = get_db_connection()
        conn.execute('UPDATE item_list SET isChecked = ?'
                    ' WHERE item_id = ?',
                    (isChecked))
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = e
    finally:
        if conn:
            conn.close()
    return err_msg


def model_deleteitem(item_id):
    err_msg=""
    item = get_one_item(item_id)
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM item_list WHERE item_id = ?', (item_id,))
        conn.commit()
        conn.close()
        #flash('"{}" was successfully deleted!'.format(item['item_id']))
    except Error as e:
        err_msg = e
        if conn:
            conn.close()
    return err_msg 


def viewitem(thisList):

    return render_template('viewitem_v1.html', viewList=thisList)



@app.route('/')
# list page - get all items with exception handling
def controller_viewitem():
    """ controller to manage '/' route """
    # call model to get data 
    myList = model_viewitem()
    # call view to combine data with HTML 
    response = viewitem(myList)
    return response


@app.route('/additem', methods=('GET', 'POST'))
def controller_additem():
    err_msg = ""
    if request.method == "POST":
        err_msg = model_additem(request.form)
        if not err_msg or err_msg is None:
            return redirect(url_for('controller_viewitem'))
    return render_template('additem_v1.html', error_msg = err_msg)

# # edit item
@app.route('/<int:item_id>/edititem', methods=('GET', 'POST'))
def controller_edititem(item_id):
    err_msg = ""
    item = get_one_item(item_id)
    if request.method == "POST":  #and "Update" in request.form:
        err_msg = model_edititem(request.form)
        if not err_msg or err_msg is None:
            return redirect(url_for('controller_viewitem'))
    return render_template('edititem.html', edititem = item, error_msg = err_msg)
    
# # delete item
@app.route('/<int:item_id>/deleteitem', methods=('GET', 'POST'))
def controller_deleteitem(item_id):
    err_msg = ""
    item = get_one_item(item_id)
    err_msg = model_deleteitem(item_id)
    if not err_msg or err_msg is None:
        # response = controller_viewitem()
        # return response
        return redirect(url_for('controller_viewitem'))
  
    return render_template('edititem.html', edititem = item, error_msg = err_msg)
    

      