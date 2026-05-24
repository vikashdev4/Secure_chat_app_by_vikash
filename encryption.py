from cryptography.fernet import Fernet

key = b'kQ9mFJ1l0P0m8WcXr4Qy6vT0s8zU3p2a1bC9dE5fG7H='
cipher = Fernet(key)

def encrypt(msg):
    return cipher.encrypt(msg.encode())

def decrypt(msg):
    return cipher.decrypt(msg).decode()