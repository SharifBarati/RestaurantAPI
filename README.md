# RestaurantAPI
This is a Django fully functional API project for a restaurant, aiming to enable client application developers to use the APIs to develop web and mobile applications. People with different roles will be able to browse, add, and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 

# Project Structure Description
This project is a RESTful API called LittleLemonAPI, designed to manage a restaurant system with core functionalities such as menu management, user carts, and order processing. It is built with a well-structured architecture that includes models for Categories, MenuItems, Cart, Orders, and OrderItems, ensuring a clear separation of concerns. All models are fully serialised, enabling efficient data validation and seamless communication between the backend and client applications. The API supports essential operations such as browsing menu items, adding items to a cart, and placing orders, making it a solid foundation for a scalable food ordering system.

# User groups
Primarily created two groups and you can edit them in the Django admin panel
•	Manager
•	Delivery crew
Users not assigned to a group will be considered customers. 

# API endpoints 
Here are all the required API routes for this project grouped into several categories.
User registration and token generation endpoints 
Djoser library is used in this project to automatically create the following endpoints and functionalities for you.

# User Registration & Authentication

The Djoser library is used to automatically generate authentication endpoints.

| Endpoint             | Role                                   | Method | Purpose 
|----------------------|----------------------------------------|--------|---------
| /api/users           | No role required                       | POST   | Creates a new user with name, email and password 
| /api/users/me/       | Authenticated user                     | GET    | Displays the current logged-in user 
| /auth/token/login/   | Valid username & password              | POST   | Generates authentication token 

# Menu Items Endpoints
| Endpoint                    | Role             | Method       | Purpose 
|-----------------------------|------------------|--------------|---------
| /api/menu-items             | Anyone           | GET          | Lists all menu items 
| /api/menu-items             | Manager          | POST         | 201 Create a new Menu Item | Returns 403 Unauthorized
| /api/menu-items/{id}        | All roles        | GET          | Retrieves a single menu item 
| /api/menu-items/{id}        | Manager          | DELETE       | delete a menu item, Returns 403 for Unauthorized 
| /api/menu-items/{id}        | Manager          | PUT, PATCH   | Updates a menu item 
| /api/menu-items/{id}        | Manager          | DELETE       | Deletes a menu item 

# User Group Management
| Endpoint                                     | Role     | Method | Purpose 
|----------------------------------------------|----------|--------|---------
| /api/groups/manager/users                    | Manager  | GET    | Returns all managers 
| /api/groups/manager/users                    | Manager  | POST   | Assigns user to manager group 
| /api/groups/manager/users/{userId}           | Manager  | DELETE | Removes user from manager group 
| /api/groups/delivery-crew/users              | Manager  | GET    | Returns all delivery crew 
| /api/groups/delivery-crew/users              | Manager  | POST   | Assigns user to delivery crew 
| /api/groups/delivery-crew/users/{userId}     | Manager  | DELETE | Removes user from delivery crew 

# 🛒 Cart Management
| Endpoint                    | Role     | Method | Purpose 
|-----------------------------|----------|--------|---------
| /api/cart/menu-items        | Customer | GET    | Retrieves cart items for current user 
| /api/cart/menu-items        | Customer | POST   | Adds item to cart 
| /api/cart/menu-items        | Customer | DELETE | Clears all cart items 

# Order Management
| Endpoint                    | Role                     | Method          | Purpose 
|-----------------------------|--------------------------|-----------------|---------
| /api/orders                 | Customer                 | GET             | Lists their orders 
| /api/orders                 | Customer                 | POST            | Creates a new order from cart items 
| /api/orders/{orderId}       | Customer                 | GET             | Retrieves a specific order 
| /api/orders                 | Manager, Delivery Crew   | GET             | Lists all orders 
| /api/orders/{orderId}       | Manager                  | PUT, PATCH      | Updates order (assign crew / status) 
| /api/orders/{orderId}       | Manager                  | DELETE          | Deletes order 
| /api/orders/{orderId}       | Delivery Crew            | PATCH           | Updates delivery status only 

# Notes
403 Unauthorized → Access denied based on user role
404 Not Found → Resource does not exist
Order status:
0 → Out for delivery
1 → Delivered

# Additional Implementation
Implementation of proper filtering, pagination and sorting capabilities is used for /api/menu-items and /api/orders endpoints.
Some throttling is applied for the authenticated users and anonymous or unauthenticated users. 

