import bcrypt


class PasswordManager:
    def __init__(self):
        self.rounds = 12  # number of hashing rounds
        self.salt = bcrypt.gensalt(rounds=self.rounds)

    def encrypt(self, password: str):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), self.salt)
        return hashed_password

    def verify(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
