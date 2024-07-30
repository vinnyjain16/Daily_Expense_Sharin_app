# Daily_Expense_Sharin_app

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd daily-expenses-app
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:
    ```sh
    export FLASK_APP=run.py
    export FLASK_ENV=development
    ```

5. **Run the application**:
    ```sh
    flask run
    ```

6. **Run the tests**:
    ```sh
    pytest
    ```

## API Endpoints

### User Endpoints
- `POST /user`: Create a new user.
- `GET /user/<int:id>`: Retrieve user details by ID.

### Expense Endpoints
- `POST /expense`: Add a new expense.
- `GET /expense/<int:user_id>`: Retrieve expenses for a user by user ID.
- `GET /balance-sheet`: Retrieve the balance sheet.

## Configuration

The configuration is managed through the `config.py` file. You can set environment variables to override the default settings.

## Documentation

- **Database Models**: Located in `app/models.py`.
- **Routes**: Located in `app/routes.py`.
- **Tests**: Located in the `tests` directory.

## License

This project is licensed under the MIT License.
