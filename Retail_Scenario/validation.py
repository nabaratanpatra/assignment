from pickle import TRUE
from cerberus import Validator

def validation_insert(body):
   v = Validator()
   v.schema = {
         'Ratings': { 
            'type': 'string'
                     },
         'Type': { 
            'type': 'string'
                     },
         'PRODUCT_PRICE': {
            'type': 'string'
                  },
         "Product_Name": {
            "type": "string"
                  },
         "limit": {
            "type": "integer"
                  },
         "offset": {
            "type": "integer"
                  }
            }
   
   val= v.validate(body)
   if val:
      return True
   else:
      print(v.errors)
      return v.errors



def validation_read(body):
   v = Validator()
   v.schema = {
         'Ratings': { 
            'type': 'string'
                     },
         'Type': { 
            'type': 'string'
                     },
         'PRODUCT_PRICE': {
            'type': 'integer'
                  },
         "Product_Name": {
            "type": "string"
                  },
         "COLUMN": {
            "type": "integer"
                  },
         "PAGE": {
            "type": "integer"
                  }
            }
   
   val= v.validate(body)
   if val:
      return True
   else:
      return v.errors





def validation_update(body):
   v = Validator()
   v.schema = {
         'Product_ID': { 
            'type': 'integer',
            'minlength': 1
                     },
         'Quantity': { 
            'type': 'string',
            'minlength': 2
                     }
                  
            } 
   val= v.validate(body)
   if val:
      return True
   else:
      return v.errors


def validation_insert_id(body):
   v = Validator()
   v.schema = {
         'Product_ID': { 
            'type': 'string',
            'minlength': 1
                     }                  
            } 
   val= v.validate(body)
   if val:
      return True
   else:
      return v.errors


def validation_delete(body):
   v = Validator()
   v.schema = {
         'Customer_Email': { 
            'type': 'string',
            'minlength': 1,
                     }                  
            } 
   val= v.validate(body)
   if val:
      return True
   else:
      return v.errors

def validation_check(body):
   v = Validator()
   v.schema = {
         "Customer_Email": {
            "type": "string",
            "minlength": 8,
            "maxlength": 255,
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
                  },
         "Password": {
            "type": "string",
            "minlength": 4,
            "maxlength": 50
                  }
   }
   val= v.validate(body)
   if val:
      return True
   else:
      return v.errors
