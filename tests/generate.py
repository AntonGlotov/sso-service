from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

hasher = PasswordHash((BcryptHasher(rounds=10),))