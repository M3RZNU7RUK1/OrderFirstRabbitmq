# Order Management System

FastAPI application for order management with JWT authentication, admin panel and RabbitMQ notifications.

## Features

- User registration and login with JWT
- Order creation system (test mode)
- Admin panel for product management (login: daneska, password: pass)
- Order notifications via RabbitMQ
- PostgreSQL database

## Technologies

- Python 3.10+
- FastAPI
- PostgreSQL
- JWT (JSON Web Tokens)
- RabbitMQ
- Poetry (dependency management)

## Installation

### Requirements

- Docker
- Python 3.10+
- Poetry

### Setup

1. Clone the repository
2. Configure environment variables in `.env` file
3. Start RabbitMQ using Docker
4. Set up Python environment with Poetry
5. Configure PostgreSQL database

## Installation Commands

Clone repository and enter directory:
```bash
git clone https://github.com/GL1KK/OrderFirstRabbitmq.git
cd OrderFirstRabbitmq
```
Create and configure .env file:

```
cat > .env <<EOL
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_username
DB_PASS=your_db_password
DB_NAME=your_db_name
JWT_SECRET_KEY=your_jwt_secret_key
USERNAME_ADMIN=admin_username
PASSWORD_ADMIN=admin_password
TOKEN=your_notification_token
EOL
```

Start RabbitMQ in Docker:

```bash

docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.10.7-management
```
    Set up Python environment:

```bash

poetry install
poetry env activate
example: /home/daniil/.cache/pypoetry/virtualenvs/order-yRxfHGHV-py3.13/bin/activate
```
Running the Application

Start the FastAPI server:
```bash
uvicorn src.main:app --reload
```
<<<<<<< HEAD
=======
Start telegram-bot:
```bash
poetry run python -m src.bot.bot
```
### Authentication
- `POST /register` - User registration
- `POST /login` - User login

### Products (Admin only)
- `GET /search` - Product search
- `POST /add_item` - Add product
- `DELETE /del_item` - Delete product

### Orders
- `GET /find_orders` - Find user orders
- `POST /create_order` - Create order
- `DELETE /delete_order` - Delete order

### User Profile
- `GET /me` - Get user profile
>>>>>>> f39f188b069d85cffbb70bed4798719d6fca0c62

## Notification Format

New order notification example:

🛒 New Order!
📌 Order Number: 11
📋 Title: 342
💰 Price: 342 rub.
⏰ Delivery Time: 7:29am
👤 User ID: 1
📅 Created: 2025-07-09T16:36:01.593069
