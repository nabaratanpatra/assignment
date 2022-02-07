
from Retail_Scenario.validation import validation_check, validation_insert, validation_insert_id, validation_update
from Utilities import db
from flask import jsonify,request
from timeit import default_timer as timer
from datetime import datetime
from Utilities import db
import hashlib
from flask_jwt_extended import create_access_token,decode_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


def give_response(data,message,start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    response = {
        "start_time": start_time.strftime("%H:%M:%S.%f"),
        "success": True,
        "data": data,
        "message":message,
        "end_time": end_time.strftime("%H:%M:%S.%f"),
        "duration":duration.total_seconds()
    }
    return response

def give_response_access_token(message,access_token,start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    response = {
        "start_time": start_time.strftime("%H:%M:%S.%f"),
        "success": True,
        "message":message,
        "end_time": end_time.strftime("%H:%M:%S.%f"),
        "duration":duration.total_seconds(),
        "access_token":access_token
    }
    return response

def test_authorization():
    auth = str(request.headers['Authorization']).split(' ')[1]
    output= decode_token(auth)['sub']
    return output

def give_hash(input):
    hash = hashlib.md5(input.encode())
    return hash.hexdigest()

def check_employee():
    print("checking")
    Customer_Email = test_authorization()
    print(Customer_Email)
    query = "select Customer_Email from customers where Customer_Email = '%s';"%(input[Customer_Email])
    print(query)
    output = db.get_all(query)
    print("USER IS PRESENT")
    if output[0][0]==1:
        return True
    else:
        return "user not found"


def retail_login():
    start_time = datetime.now()
    input = {}
    input = request.get_json()
    v= validation_check(input)
    if isinstance(v,bool):
            query = f"select password from customers where Customer_Email = '{input['Customer_Email']}'"
            messages = db.get_all(query)
            print("------------")
            if give_hash(input['Password']) == messages[0][0]:
                print("HELLO")
                access_token = create_access_token(identity=input['Customer_Email'])
                return jsonify(give_response_access_token(message="login successful",access_token=access_token, start_time=start_time))
            else:
                return jsonify(give_response(data=messages, message="wrong username or password", start_time=start_time))
    else:
        return jsonify({ "message" : v })


def order_details():
        start_time = datetime.now()
        auth = str(request.headers['Authorization']).split(' ')[1]
        output= decode_token(auth)['sub']
        query = f"select c.Customer_Name,c.Contact,c.Gender,c.Address,p.Product_Name, p.Product_Model,p.Availability,p.Ratings,p.Type from Customers c left join Customer_Orders co on c.Customer_ID = co.Customer_ID left join Products p on co.Product_ID = p.Product_ID where c.Customer_Email = '%s';"%(output)
        var = db.get_all_id(query)
        return jsonify(give_response(data=var, message='operation successful', start_time=start_time))
        # else:
        #     return jsonify(give_response(data=[], message='operation falied', start_time=start_time))


def update_order():
    start_time = datetime.now()
    if isinstance(check_employee(),bool):
        input = {}
        input = request.get_json()
        v= validation_update(input)
        if isinstance(v,bool):
            query = "UPDATE Customer_Orders SET Quantity = '%s' WHERE Customer_ID = %s;"%(input["Quantity"],input["Customer_ID"])
            messages = db.update(query)
            return jsonify(give_response(data=messages, message="row is updated", start_time=start_time))
        else:
            return jsonify({ "message" : v })
    else:
        return jsonify(give_response(data=[], message="operation falied", start_time=start_time))



def place_order():
    start_time = datetime.now()
    auth = str(request.headers['Authorization']).split(' ')[1]
    input= decode_token(auth)['sub']
    v= validation_update(input)
    if isinstance(v,bool):
        input = {}
        input = request.get_json()
        query = f"insert into Customer_Orders('Customer_ID','Product_ID','Quantity') values ('{input['Customer_ID']}','{input['Product_ID']}','{input['Quantity']}');"
        print(query)
        messages = db.update(query)
        return jsonify(give_response(data=messages, message="row is updated", start_time=start_time))
    else:
        return jsonify(give_response(data=[], message="operation falied", start_time=start_time))




def delete_order():
    start_time = datetime.now()
    auth = str(request.headers['Authorization']).split(' ')[1]
    input= decode_token(auth)['sub']
    print(input)
    value = request.args
    v= validation_insert_id(value)
    inputs = {}
    inputs = request.get_json()
    print(v)
    if isinstance(v,bool):
        print("---------------")
        query1 = "select Quantity from Customer_Orders where Product_ID  = %s;"%(inputs["Product_ID"])
        messages1 = db.get_all(query1)
        print(messages1)
        query = "DELETE FROM Customer_Orders WHERE Product_ID  = %s;"%(inputs["Product_ID"])
        messages = db.delete(query)
        print(messages)
        query2 = "update Products set Availability = Availability + 'message1' where Product_ID = ;"%(inputs["Product_ID"])
        messages2 = db.update(query2)
        return jsonify(give_response(data=messages2, message="Deleted the data", start_time=start_time))
    else:
        return jsonify({ "message" : v })





def read_products():
        start_time = datetime.now()
        input = {}
        input = request.get_json()
        query = f"select Ratings, Type, PRODUCT_PRICE, Product_Name from products where {input['col']} = '{input['details']}';"
        var = db.get_all(query)
        return jsonify(give_response(data=var, message='operation successful', start_time=start_time))
