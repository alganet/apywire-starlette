# SPDX-FileCopyrightText: 2026 Alexandre Gomes Gaigalas <alganet@gmail.com>
#
# SPDX-License-Identifier: ISC

class UserService:
    def __init__(self, db):
        self.db = db

    def get_user(self, screen_name: str):
        row = self.db.execute(
            """
            SELECT screen_name, name FROM users
            WHERE screen_name = ?
            """,
            (screen_name,),
        ).fetchone()
        if row:
            return {"screen_name": row[0], "name": row[1]}
        return None


class MigrationService:
    def __init__(self, db):
        self.db = db

    def run(self):
        print(f"Migrating {self.db.filename}")
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                screen_name VARCHAR(255) PRIMARY KEY, name VARCHAR(255)
            )
            """)
        cursor.execute("""
            REPLACE INTO users (screen_name, name)
            VALUES ('foo', 'Test User Foo!')
            """)
        cursor.execute("""
            REPLACE INTO users (screen_name, name)
            VALUES ('bar', 'Test User Bar!')
            """)
        cursor.execute("""
            REPLACE INTO users (screen_name, name)
            VALUES ('baz', 'Test User Baz!')
            """)
        return True
