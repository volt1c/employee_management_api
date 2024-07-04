# Employee Management API
![pylint workflow](https://github.com/volt1c/employee_management_api/actions/workflows/pylint.yml/badge.svg)

## Instruction

### 1. Install Packages
```shell
$ pip install -r requirements.txt
```

### 2. Create database

### 3. Correct environment variables file
Set your database URI and jwt secret key
```dotenv
# .env
# Host Config
HOST='0.0.0.0'
PORT=80
ENV='production'
DEBUG=False

# Database Config
SQLALCHEMY_DATABASE_URI_DEV='mysql://username:password@address/database_name'
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Auth Config
JWT_SECRET_KEY='some_jwt_secret_key'

# Routes Config
ROUTE_ADMIN_REGISTRATION=True
```

### 4. Run application

### 5. Register Admins
Send new admin to `<your_url>/api/auth/register`
```json
{
  "username": "<username>",
  "password": "<password>",	  
  "email": "<email>"
}
```

### 6. Disable admins registration
```dotenv
# .env
...
ROUTE_ADMIN_REGISTRATION=False
```

### 7. Restart application