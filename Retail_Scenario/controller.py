from Retail_Scenario.validation import validation_check, validation_insert, validation_insert_id, validation_read, validation_update
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
    query = f"select Customer_Email from customers where Customer_Email = '{input[Customer_Email]}';"
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
            inputarray = []
            inputarray.append(input["Customer_Email"])
            query = "select password from customers where Customer_Email = %s"
            messages = db.get_all(query, inputarray)
            #  print("------------")
            if give_hash(input['Password']) == messages[0][0]:
                print("HELLO")
                access_token = create_access_token(identity=input['Customer_Email'])
                return jsonify(give_response_access_token(message="login successful",access_token=access_token, start_time=start_time))
            else:
                return jsonify(give_response(data=messages, message="wrong username or password", start_time=start_time))
    else:
        return jsonify({ "message" : v })


def place_order():
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
        query = f"select Customer_ID from Customers where Customer_Email = '{input}'"
        messages = db.get_all(query)
        print(messages[0][0])
        query1 = f"insert into Customer_Orders(Customer_ID,Product_ID,Quantity) values ('{messages[0][0]}', {inputs['Product_ID']} , {inputs['Quantity']});"
        print(query1)
        messages1 = db.update(query1)
        print(messages1)
        query3 = f"update Products set Availability = Availability - {inputs['Quantity']} where Product_ID = '{inputs['Product_ID']}';"
        messages3 = db.update(query3)
        return jsonify(give_response(data=messages3, message="row is updated", start_time=start_time))
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
        query = f"select Customer_ID from Customers where Customer_Email = '{input}'"
        messages = db.get_all(query)
        print(messages[0][0])
        query1 =f"select Quantity from Customer_Orders where Customer_ID = '{messages[0][0]}' and Product_ID  = {inputs['Product_ID']};"
        print(query1)
        messages1 = db.get_all(query1)
        print(messages1[0][0])
        query2 = f"DELETE FROM Customer_Orders WHERE Product_ID  = '{inputs['Product_ID']}';"
        messages2 = db.delete(query2)
        print(messages2)
        query3 = f"update Products set Availability = Availability + '{messages1[0][0]}' where Product_ID = '{inputs['Product_ID']}';"
        messages3 = db.update(query3)
        return jsonify(give_response(data=messages3, message="Deleted the data", start_time=start_time))
    else:
        return jsonify({ "message" : v })


def __read_products(input):
    if input == None or "COLUMN" in input.keys():
        inputarray = []
        query = "select Ratings, Type, PRODUCT_PRICE, Product_Name from products "
        if "COLUMN" in input.keys():
            query = query + "ORDER BY {}".format(input["COLUMN"])               
            print(query)
            results = db.get_all(query, inputarray)
        return results
    elif len(input)>0:
        inputarray = []
        query = "select Ratings, Type, PRODUCT_PRICE, Product_Name from products where"
        if "Ratings" in input.keys():
            inputarray.append(input["Ratings"])
            query = query + " Ratings=%s and "                                                     
        if "Type" in input.keys():
            inputarray.append(input["Type"])
            query = query + "Type = %s and "
        if "PRODUCT_PRICE" in input.keys():
            inputarray.append(input["PRODUCT_PRICE"])
            query = query + "PRODUCT_PRICE > %s and "
        if "Product_Name" in input.keys():
            inputarray.append(input["Product_Name"])
            query = query + "Product_Name=%s and "
        query=query[:-4]
        if "COLUMN" in input.keys():
            query = query + "ORDER BY {}".format(input["COLUMN"]) 
        # if "PAGE" in input.keys():
        #     query = query + " LIMIT %s ; "
        print(query)
        results = db.get_all(query, inputarray)
        return results


def read_products():
    input = {}
    input = request.get_json()
    start_time = datetime.now()
    results = __read_products(input)
    return jsonify(give_response(data=[results], message='operation successful', start_time=start_time))


def __order_details(input):
        auth = str(request.headers['Authorization']).split(' ')[1]
        output= decode_token(auth)['sub']
        inputarray = []
        query = " select c.Customer_Name"
        #  p.Product_Name, p.Product_Model,p.Availability,p.Ratings,p.Type  
        if "Contact" in input.keys():
            query = query + ",c.{}".format(input["Contact"])
        if "Gender" in input.keys():
            query = query + ",c.{}".format(input["Gender"])
        if "Address" in input.keys():
            query = query + ",c.{}".format(input["Address"])
        if "Product_Model" in input.keys():
            query = query + ",p.{}".format(input["Product_Model"])
        if "Availability" in input.keys():
            query = query + ",p.{}".format(input["Availability"])
        if "Ratings" in input.keys():
            query = query + ",p.{}".format(input["Ratings"])
        if "Type" in input.keys():
            query = query + ",p.{}".format(input["Type"])
        inputarray.append(output)
        query = query + " from Customers c left join Customer_Orders co on c.Customer_ID = co.Customer_ID left join Products p on co.Product_ID = p.Product_ID where c.Customer_Email = %s; "
        print(query)
        results = db.get_all(query, inputarray)
        return results

def array__order_details(input):
        input = input.split(',')
        auth = str(request.headers['Authorization']).split(' ')[1]
        output= decode_token(auth)['sub']
        inputarray = []
        print(input[1])
        query = " select c.Customer_Name"
        #  p.Product_Name, p.Product_Model,p.Availability,p.Ratings,p.Type  
        if "Contact" in input:
            query = query + ",c.Contact"
        if "Gender" in input:
            query = query + ",c.Gender"
            print(query)
        if "Address" in input:
            query = query + ",c.Address"
        if "Product_Model" in input:
            query = query + ",p.Product_Model"
        if "Availability" in input:
            query = query + ",p.Availability"
        if "Ratings" in input:
            query = query + ",p.Ratings"
        if "Type" in input:
            query = query + ",p.Type"
        inputarray.append(output)
        query = query + " from Customers c left join Customer_Orders co on c.Customer_ID = co.Customer_ID left join Products p on co.Product_ID = p.Product_ID where c.Customer_Email = %s; "
        print(query)
        results = db.get_all(query, inputarray)
        return results



def array_order_details():
    start_time = datetime.now()
    input = ''
    COLUMN = request.args.get("COLUMN")
    if (COLUMN != None):
        input= COLUMN
    print(input)
    results = array__order_details(input)
    return jsonify(give_response(data=[results], message='operation successful', start_time=start_time))
 

def order_details():
        start_time = datetime.now()
        input = {}
        Contact = request.args.get("Contact")
        if (Contact != None):
            input["Contact"]= Contact
        Gender = request.args.get("Gender")
        if (Gender != None):
            input["Gender"]= Gender
        Address = request.args.get("Address")
        if (Address != None):
            input["Address"]= Address
        Product_Model = request.args.get("Product_Model")
        if (Product_Model != None):
            input["Product_Model"]= Product_Model
        Availability = request.args.get("Availability")
        if (Availability != None):
            input["Availability"]= Availability
        Ratings = request.args.get("Ratings")
        if (Ratings != None):
            input["Ratings"]= Ratings
        Type = request.args.get("Type")
        if (Type != None):
            input["Type"]= Type
        results = __order_details(input)
        return jsonify(give_response(data=[results], message='operation successful', start_time=start_time))


# def order_details():
#         start_time = datetime.now()
#         auth = str(request.headers['Authorization']).split(' ')[1]
#         output= decode_token(auth)['sub']
#         # query = f"select c.Customer_Name, c.Contact,c.Gender,c.Address,p.Product_Name, p.Product_Model,p.Availability,p.Ratings,p.Type from Customers c left join Customer_Orders co on c.Customer_ID = co.Customer_ID left join Products p on co.Product_ID = p.Product_ID where c.Customer_Email = '{output}';"
        
#         input = {}
#         input = request.get_json()
#         x = True
#         baseQuery = "select "
#         if input['Customer_Name']:
#             if x:
#                 baseQuery = baseQuery + " c.%s, " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" c.{input['Customer_Name']} " 
#         if input['Contact']:
#             if x:
#                 baseQuery = baseQuery + f" c.{input['Contact']}," 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" c.{input['Contact']} " 
#         if input['Gender']:
#             if x:
#                 baseQuery = baseQuery + f" c.{input['Gender']}, " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" c.{input['Gender']} " 
#         if input['Address']:
#             if x:
#                 baseQuery = baseQuery + f" c.{input['Address']} " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" c.{input['Address']},"
#         if input['Product_Model']:
#             if x:
#                 baseQuery = baseQuery + f" p.{input['Product_Model']} " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" p.{input['Product_Model']}," 
#         if input['Availability']:
#             if x:
#                 baseQuery = baseQuery + f" p.{input['Availability']} " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" p.{input['Availability']}," 
#         if input['Ratings']:
#             if x:
#                 baseQuery = baseQuery + f" p.{input['Ratings']} " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" p.{input['Ratings']}, " 
#         if input['Type']:
#             if x:
#                 baseQuery = baseQuery + f" p.{input['Type']} " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" p.{input['Type']}, " 

#         baseQuery = baseQuery + f"from Customers c left join Customer_Orders co on c.Customer_ID = co.Customer_ID left join Products p on co.Product_ID = p.Product_ID where c.Customer_Email = '{output}';"
#         print(baseQuery)
#         var = db.get_all(baseQuery)
#         return jsonify(give_response(data=var, message='operation successful', start_time=start_time))


        # var = db.get_all_id(query)
        # print(var)
        # # for row in var:
        # #     print "%s, %s" % (row["name"], row["category"])
        # return jsonify(give_response(data=[var], message='operation successful', start_time=start_time))




# def read_products():
#         start_time = datetime.now()
#         input = {}
#         input = request.get_json()
#         x = True
#         baseQuery = "select Ratings, Type, PRODUCT_PRICE, Product_Name from products "
#         if input['Ratings']:
#             if x:
#                 baseQuery = baseQuery + f" where Ratings = '{input['Ratings']}' " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" where Ratings = '{input['Ratings']}'"
#         if input['Type']:
#             if x:
#                 baseQuery = baseQuery + f" where Type = '{input['Type']}' " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" and  Type = '{input['Type']}'"
#         if input['PRODUCT_PRICE']:
#             if x:
#                 baseQuery = baseQuery + f" where PRODUCT_PRICE = '{input['PRODUCT_PRICE']}' " 
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" and  PRODUCT_PRICE = '{input['PRODUCT_PRICE']}'"
#         if input['Product_Name']:
#             if x:
#                 baseQuery = baseQuery + f" where Product_Name = '{input['Product_Name']}'"
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" and  Product_Name = '{input['Product_Name']}'"
#         if input['col']:
#             if x:
#                 baseQuery = baseQuery + f" ORDER BY {input['col']}  "
#                 x = False
#             else:
#                 baseQuery = baseQuery + f" ORDER BY {input['col']}  "
#         if input['limit']:
#                 baseQuery = baseQuery + f" limit {input['limit']}"
#                 if input['offset']:
#                     baseQuery = baseQuery + f" offset {input['offset']}"
#         baseQuery = baseQuery + ";"
#         #query = f"select Ratings, Type, PRODUCT_PRICE, Product_Name from products where Ratings = IFNULL(null,'{input['Ratings']}') and Type = IFNULL(null,'{input['Type']}') and PRODUCT_PRICE = IFNULL(null,'{input['PRODUCT_PRICE']}') or Product_Name = IFNULL(null,'{input['Product_Name']}') ;"
#         # query = f"select Ratings, Type, PRODUCT_PRICE, Product_Name from products where (Ratings='{input['details']}' OR '{input['details']}' IS NULL) and (Type='{input['details2']}' OR '{input['details2']}' IS NULL);"
#         print(baseQuery)
#         var = db.get_all(baseQuery)
#         return jsonify(give_response(data=var, message='operation successful', start_time=start_time))
