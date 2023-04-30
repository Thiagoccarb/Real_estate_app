import hashlib


def md5_encrypter(file: bytes) -> str:
    md5 = hashlib.md5()
    md5.update(file)
    return md5.hexdigest()
