# Potential Inc

## Multivendor

---

# Live URL

[https://multivendor-1k0o.onrender.com](https://multivendor-1k0o.onrender.com)

# API Documentation
[Multivendor.postman_collection.json](Multivendor.postman_collection.json)

# Accounts
- Admin
    - email: admin@admin.com
    - password: admin
- Seller One
    - email: seller1@gmail.com
    - password: admin@123%23
- Seller Two
    - email: seller2@gmail.com
    - password: admin@123%23
- Customer One
    - email: user1@gmail.com
    - password: admin@123%23
- Customer Two
    - email: user2@gmail.com
    - password: admin@123%23

## Prerequisites

Before getting started, make sure you have the following installed:

- Python (3.12 recommended)

## Local Setup

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone git@github.com:nhridoy/multivendor.git
cd multivendor
```

### Step 2: Create a Virtual Environment

Create and activate a virtual environment to isolate your project dependencies:

```bash
python3 -m venv env
source env/bin/activate      # On Unix or MacOS
# OR
env\Scripts\activate         # On Windows
```

### Step 3: Install Dependencies

Install the required Python dependencies using pip:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Django Application

Run the Django application using the ASGI server:

```bash
python manage.py runserver
```

## API Reference

####  Authentication Endpoints:
| HTTP      | Endpoints                   | Action                 |
|-----------|-----------------------------|------------------------|
| **POST**  | `api/auth/login/seller/`    | To login a Seller      |
| **POST**  | `api/auth/login/user/`      | To login a User        |
| **POST**  | `api/auth/login/admin/`     | To login a Admin       |
| **POST**  | `/api/auth/register/`       | To register a user     |
| **GET**   | `/api/auth/profile/`        | To Get Profile         |
| **PATCH** | `/api/auth/profile/`        | To Update Profile      |
| **POST**  | `/api/auth/logout/`         | To logout              |
| **GET**   | `/api/auth/admin/user/`     | User List for Admin    |
| **GET**   | `/api/auth/admin/user/:id/` | User Details for Admin |
| **PATCH** | `/api/auth/admin/user/:id/` | User Update for Admin  |

####  Category Endpoints:
| HTTP       | Endpoints                      | Action                |
|------------|--------------------------------|-----------------------|
| **POST**   | `api/products/categories/`     | To Create a Category  |
| **GET**    | `api/products/categories/`     | To Get All Categories |
| **GET**    | `api/products/categories/:id/` | To Get a Category     |
| **PATCH**  | `api/products/categories/:id/` | To Update a Category  |
| **DELETE** | `api/products/categories/:id/` | To Delete a Category  |

####  Sub Category Endpoints:
| HTTP       | Endpoints                          | Action                    |
|------------|------------------------------------|---------------------------|
| **POST**   | `api/products/sub-categories/`     | To Create a Sub Category  |
| **GET**    | `api/products/sub-categories/`     | To Get All Sub Categories |
| **GET**    | `api/products/sub-categories/:id/` | To Get a Sub Category     |
| **PATCH**  | `api/products/sub-categories/:id/` | To Update a Sub Category  |
| **DELETE** | `api/products/sub-categories/:id/` | To Delete a Sub Category  |

####  Product Endpoints:
| HTTP       | Endpoints           | Action              |
|------------|---------------------|---------------------|
| **POST**   | `api/products/`     | To Create a Product |
| **GET**    | `api/products/`     | To Get All Products |
| **GET**    | `api/products/:id/` | To Get a Product    |
| **PATCH**  | `api/products/:id/` | To Update a Product |
| **DELETE** | `api/products/:id/` | To Delete a Product |

####  Cart Endpoints:
| HTTP       | Endpoints                            | Action                   |
|------------|--------------------------------------|--------------------------|
| **POST**   | `api/orders/cart/`                   | To Add a Product to Cart |
| **GET**    | `api/orders/cart/`                   | To Get Cart              |
| **GET**    | `api/orders/cart/:id/`               | To Get Cart Details      |
| **DELETE** | `api/orders/cart/:id/`               | To Delete Cart           |
| **GET**    | `api/orders/cart/increase-quantity/` | To Increase Quantity     |
| **GET**    | `api/orders/cart/decrease-quantity/` | To Decrease Quantity     |

####  Order Endpoints:
| HTTP     | Endpoints             | Action                    |
|----------|-----------------------|---------------------------|
| **POST** | `api/orders/`         | To Create an Order        |
| **GET**  | `api/orders/`         | To Get All Orders         |
| **GET**  | `api/orders/:id/`     | To Get an Order Details   |
| **GET**  | `api/order-item/`     | List For Seller and Admin |
| **GET**  | `api/order-item/:id/` | Get For Seller and Admin  |

## Notes

- Knock me on slack for environment variables.
---