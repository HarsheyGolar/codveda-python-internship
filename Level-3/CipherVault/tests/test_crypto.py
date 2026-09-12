import pytest
from cryptography.fernet import Fernet

from ciphervault.crypto import decrypt_data, encrypt_data
from ciphervault.exceptions import DecryptionError, EncryptionError


def test_encrypt_and_decrypt_round_trip():
    data = b"secret message"
    key = Fernet.generate_key()

    encrypted = encrypt_data(data, key)

    assert encrypted != data
    assert decrypt_data(encrypted, key) == data


def test_encrypt_invalid_key_raises_encryption_error():
    with pytest.raises(EncryptionError):
        encrypt_data(b"secret message", b"not-a-valid-fernet-key")


def test_decrypt_wrong_key_raises_decryption_error():
    key = Fernet.generate_key()
    wrong_key = Fernet.generate_key()
    encrypted = encrypt_data(b"secret message", key)

    with pytest.raises(DecryptionError):
        decrypt_data(encrypted, wrong_key)

