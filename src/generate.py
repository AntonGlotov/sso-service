import secrets
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
print(PasswordHash.hash(PasswordHash.recommended(), '1234'))

print(secrets.token_hex(32))




