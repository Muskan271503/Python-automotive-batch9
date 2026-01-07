# login.py
import hashlib
import time
from getpass import getpass


class SecureLoginSystem:
    def __init__(self, max_attempts=3, lock_duration=60):
        # username -> (hashed_password, is_locked, lock_until, failed_attempts)
        self.users = {
            'user1': (self._hash_password('password123'), False, 0, 0),
            'admin': (self._hash_password('secretadmin'), False, 0, 0)
        }
        self.max_attempts = max_attempts
        self.lock_duration = lock_duration

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validate_input(self, input_str: str) -> str:
        if not input_str or not input_str.strip():
            raise ValueError("Input cannot be empty or only whitespace.")
        return input_str.strip()

    def is_account_locked(self, username: str) -> bool:
        if username not in self.users:
            return False
        _, locked, lock_until, _ = self.users[username]
        if locked and time.time() < lock_until:
            return True
        if locked:  # Auto-unlock if time expired
            self.users[username] = (self.users[username][0], False, 0, 0)
        return False

    def lock_account(self, username: str):
        if username in self.users:
            lock_until = time.time() + self.lock_duration
            self.users[username] = (self.users[username][0], True, lock_until, 0)

    def reset_attempts(self, username: str):
        if username in self.users:
            hash_pw, locked, lock_until, _ = self.users[username]
            self.users[username] = (hash_pw, locked, lock_until, 0)

    def increment_attempts(self, username: str):
        if username in self.users:
            hash_pw, locked, lock_until, attempts = self.users[username]
            self.users[username] = (hash_pw, locked, lock_until, attempts + 1)

    def authenticate(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        stored_hash, _, _, _ = self.users[username]
        return stored_hash == self._hash_password(password)

    def attempt_login(self, username: str, password: str) -> dict:
        try:
            self.validate_input(username)
            self.validate_input(password)
        except ValueError as e:
            return {"success": False, "message": str(e), "locked": False}

        if self.is_account_locked(username):
            return {"success": False, "message": "Account is temporarily locked.", "locked": True}

        # Successful login
        if self.authenticate(username, password):
            self.reset_attempts(username)
            return {"success": True, "message": "Login successful!", "locked": False}

        # Failed login (wrong password OR non-existent user)
        # Only increment attempts if the username actually exists
        if username in self.users:
            self.increment_attempts(username)
            _, _, _, attempts = self.users[username]
            if attempts >= self.max_attempts:
                self.lock_account(username)
                return {"success": False, "message": "Too many failed attempts. Account locked.", "locked": True}

        # Always return the same generic message for security
        return {"success": False, "message": "Invalid username or password.", "locked": False}

    def run_interactive_login(self):
        attempts = 0
        username = ""

        print("=== Secure Login System ===\n")

        while attempts < self.max_attempts:
            try:
                username = self.validate_input(input("Enter username: "))

                if self.is_account_locked(username):
                    print("Account is temporarily locked. Try again later.")
                    return False

                password = getpass("Enter password: ")
                password = self.validate_input(password)

                result = self.attempt_login(username, password)

                if result["success"]:
                    print(f"\n{result['message']}")
                    return True

                if "locked" in result["message"].lower():
                    print(f"\n{result['message']}")
                    print(f"Account '{username}' locked for {self.lock_duration} seconds.")
                    return False

                attempts += 1
                remaining = self.max_attempts - attempts
                attempt_word = "attempt" if remaining == 1 else "attempts"
                print(f"{result['message']} {remaining} {attempt_word} remaining.\n")

            except ValueError as e:
                print(f"Error: {e}\n")

        return False


if __name__ == "__main__":
    system = SecureLoginSystem(max_attempts=3, lock_duration=30)
    system.run_interactive_login()