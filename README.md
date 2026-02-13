<!--
SPDX-FileCopyrightText: 2026 Alexandre Gomes Gaigalas <alganet@gmail.com>

SPDX-License-Identifier: ISC
-->

# apywire + starlette Example

This repository demonstrates how to build a modular, dependency-injected **starlette** application using **apywire**.

It showcases:
- **Declarative Dependency Injection**: Wiring components using `config.yaml`.
- **Compile-time DI**: Generates optimized python code (`container.py`) avoiding runtime overhead.
- **Database Integration**: Using `apsw` (SQLite) directly configured in YAML.
- **Migrations**: Simple migration runner wired as a service.
- **CLI Commands**: Unified entrypoint for running, compiling, and migrating.

## Project Structure

```
.
├── config.yaml          # Dependency graph definition (The Wiring)
├── requirements.txt     # Python dependencies
└── src
    ├── app.py           # Application entrypoint & CLI
    ├── container.py     # Auto-generated DI container (Do not edit manually)
    ├── handlers.py      # starlette request handlers (Controllers)
    └── services.py      # Business logic & Services
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Compile the Container**
   apywire compiles your `config.yaml` into `src/container.py`. You must run this whenever you change `config.yaml`.
   ```bash
   python src/app.py --compile
   ```

3. **Run Migrations**
   Initialize the SQLite database.
   ```bash
   python src/app.py --migrate
   ```

4. **Run the Application**
   Starts the Uvicorn server (with auto-reload enabled).
   ```bash
   python src/app.py --run
   ```

## Usage

- **Hello World**:
  ```bash
  curl http://127.0.0.1:8000/
  # {"message":"Hello World!"}
  ```

- **Get User**:
  ```bash
  curl http://127.0.0.1:8000/users/foo
  # {"user":{"screen_name":"foo","name":"Test User Foo!"}}
  ```

## How it Works

### 1. The Wiring (`config.yaml`)

We define our services and handlers in `config.yaml`. apywire resolves the dependency graph.

```yaml
# Define a database connection using apsw
apsw.Connection db:
  filename: "db.sqlite"

# Inject db into UserService
services.UserService users:
  db: "{db}"

# Inject db into MigrationService
services.MigrationService migrations:
  db: "{db}"

# Inject users service into UserHandler
handlers.UserHandler user_handler:
  users: "{users}"

# Routes verify their endpoints exist
starlette.routing.Route user_route:
  path: "/users/{screen_name}"
  endpoint: "{user_handler}"
  methods: ["GET"]

# The main starlette app
starlette.applications.starlette app:
  routes:
    - "{user_route}"
    - "{hello_route}"
    # ...
```

### 2. The Code

**`src/handlers.py`** receives fully initialized services in `__init__`.
```python
class UserHandler:
    def __init__(self, users: services.UserService):
        self.users = users

    async def __call__(self, scope, receive, send):
        # ... standardized ASGI handler ...
        user = self.users.get_user(screen_name)
        # ...
```

**`src/services.py`** receives the raw database connection.
```python
class UserService:
    def __init__(self, db):
        self.db = db # This is the apsw.Connection object from config.yaml
```

### 3. The Compilation

Running `python src/app.py --compile` reads `config.yaml` and generates `src/container.py`.
This file contains a `Compiled` class with lazy-loaded resources.

```python
# src/container.py (Snippet)
class Compiled:
    def db(self):
        if not hasattr(self, "_db"):
            self._db = apsw.Connection(filename='db.sqlite')
        return self._db
    # ...
```

The application at runtime (`src/app.py`) simply imports and uses this generated code, ensuring zero reflection overhead during request handling.
