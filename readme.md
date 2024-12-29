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

## Notes

- Knock me on slack for environment variables.
---