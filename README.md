# assignment

USE CASE: Retail Scenario
A retail company sells various phones and tablets. The company has registered users that can log in and view the information about the products that they have bought till date.
Users can also find products based on various filters based on the Rating, Type, Price and Name of the product.
Given an excel file with all the required information, create a database with all the Customer, Product and Orders data. This use case requires 5 routes:

•	Login
•	Get Customer Order Details (After user Authentication)
•	Place Order (After user Authentication)
•	Cancel Order (After user Authentication)
•	Get Products (No Authentication needed)

 
1.	Load the CSV files into the database. The database schema should have the following structure:
Retail Database
Tables:
●      Customers [Customer ID (varchar), Customer Name (varchar), Contact(integer), Gender (Enum), Address(varchar), Customer Email(varchar), Password (varchar)]
●      Customer Orders [Customer ID (varchar), Product ID (int), Quantity(int)]
●      Products [Product ID (int), Product Name (varchar), Product Model (varchar), Availability (int), Ratings (int), Type (Enum)]
 
        	
2.	 Customer authentication
Create a login route, with the input as email and password. Validate the email and password from the customer table.
Refer to the list of emails and passwords. The password is stored in md5 format in the Customer Table. Once the validation is successfully completed, generate a JSON Web Token containing the email as payload.
Input: JSON [Email, Password]
Output: JSON Web token (if authenticated) / Error Message (Failed Authentication)
3.	Create a route to find the customer and product details using Customer Order table.
Customer can view only their own Order details.
Clients can send a request with fields that they need. For example - Customer Name, Contact, Gender, Address, Product Name, Product Model, Availability, Ratings, Type.
Input:
1.	Specify the field names of choice in request params.
a.	Can take any fields Products table
        	Output:
1.	Order Details of authenticated customer.
a.	Information related the field params given in input field only be listed, if no field mentioned display all the details related to product and customer
4.	Place Order
1.	Create a route that will create an order.
2.	After creation product availability value should be updated in the product table. (Product availability – Quantity ordered)
Input:
a. 	Product ID
b. 	Quantity

5.	Cancel Order
1.	Create a route that will delete an order.
2.	After deletion product availability value should be updated in the product table. (Product availability + Quantity ordered)
Customer can delete only their own orders.
Input:
a. 	Product ID 

6.	Get Products (No need Authentication)
Apply filters on the Products table to get products information.
        	These filters are dynamic, they can be enabled or disabled according to the user.
Input:
a. 	Pagination params,
b. 	Sort(field),
c. 	Filter
1.	Rating,
2.	Type,
3.	Product Price,
4.	Product Name

NOTE:
        	1. If the sort param is used, then the output should be ordered based on the column on which sort is specified.
        	2. Rating, Type-- non mandatory fields which act as filters.
3. Product Price, Product Name -- non mandatory fields act as search filters
        	        	One or more filters can be applied to get product information.
        	Output: Records matching the filter and sorted in respective field specified.

Non-Functional Requirements
1. Maintain a git repository with proper commit messages. Introduce and explain your application in the ReadMe part of your git repository.
2. Deploy your application in server.
