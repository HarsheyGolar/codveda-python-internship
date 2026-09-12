from cryptography.fernet import Fernet, InvalidToken

from .exceptions import DecryptionError, EncryptionError

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypt plaintext data  using a Fernet Key."""
    try:
        cipher = Fernet(key)
        return cipher.encrypt(data)
    except(TypeError, ValueError)as error:
        raise EncryptionError("Could not encrypt the data.")from error

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypt encrypted data using a Fernet Key."""
    try:
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_data)
    except InvalidToken as error:
        raise DecryptionError(
            "could not decrypt the data. "
            "The key may be incorrect or the data may be corrupted."
        ) from error
    except (TypeError, ValueError) as error:
        raise DecryptionError("could not decrypt the data. ") from error
    