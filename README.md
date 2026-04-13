# BookMarket

BookMarket is a web application developed in Django that implements a marketplace specialized in buying and selling second-hand books. The platform features a hybrid account system, allowing users to seamlessly transition between buyer and seller roles within a single account.

## Deployment

The application is hosted on PythonAnywhere and can be accessed at:
https://bookmarket.pythonanywhere.com/

### Test Credentials

To evaluate the different access levels and interfaces, use the following credentials:

| Role | Username | Password |
| :--- | :--- | :--- |
| Buyer | ferreirag07 | g07buyer |
| Seller | patriciag | pg123seller |
| Buyer & Seller | francisca18 | buyer&seller |
| Administrator | admin | admin1 |

## Features

* **Buyer Functions:** Browse and search book listings, manage favorites, complete purchases, track purchase history, submit reviews, and contact sellers via an integrated chat system.
* **Seller Functions:** Publish and manage book listings, track active inventory, mark items as sold, communicate with buyers, and access an analytical dashboard displaying sales metrics and average ratings.
* **Admin Functions:** Monitor platform-wide statistics via a custom analytical dashboard, inspect individual user activity profiles, and quickly access the Django Admin interface for backend data management.

## Local Setup

To configure and run this project in a local environment, follow these instructions:

1. Clone the repository from GitHub:
   ```bash
   git clone [https://github.com/BeatrizF26/TPW-Project-1.git](https://github.com/BeatrizF26/TPW-Project-1.git)
   cd TPW-Project-1
   ```

2. Create and activate a virtual environment.

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. Start the local development server:
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at `http://127.0.0.1:8000/`.