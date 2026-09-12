from pathlib import Path

import pytest
from cryptography.fernet import Fernet

from ciphervault.exceptions import InvalidKeyError, KeyNotFoundError
from ciphervault.key_manager import(
    generate_key,
    key_exists,
    load_key,
    save_key,
)

def test_generate_key():
    key = generate_key()

    assert isinstance(key, bytes)
    assert Fernet(key)

def test_save_and_load_key(tmp_path: Path):
    key_path = tmp_path / "master.key"

    key = generate_key()
    save_key(key, key_path)

    loaded_key = load_key(key_path)

    assert key == loaded_key

def test_key_exists(tmp_path: Path):
    key_path = tmp_path / "master.key"

    assert key_exists(key_path) is False

    save_key(generate_key(), key_path)

    assert key_exists(key_path) is True

def test_load_missing_key(tmp_path: Path):
    key_path = tmp_path / "missing.key"

    with pytest.raises(KeyNotFoundError):
        load_key(key_path)

def test_load_invalid_key(tmp_path: Path):
    key_path = tmp_path / "invalid.key"
    key_path.write_bytes(b"not-a-valid-fernet-key")

    with pytest.raises(InvalidKeyError):
        load_key(key_path)