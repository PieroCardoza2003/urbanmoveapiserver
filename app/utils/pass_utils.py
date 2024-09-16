import hashlib
import secrets

# Generar una clave segura y hacer un hash SHA-256
clave_segura = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

print(clave_segura)
