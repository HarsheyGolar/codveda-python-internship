from pathlib import Path

import pytest

from ciphervault.exceptions import (
    DecryptionError,
    FileOperationError,
    KeyNotFoundError,
)
from ciphervault.file_handler import decrypt_file, encrypt_file
from ciphervault.key_manager import generate_key, save_key


def test_encrypt_and_decrypt_file_round_trip(tmp_path: Path):
    input_path = tmp_path / "input" / "secret.bin"
    encrypted_path = tmp_path / "encrypted" / "secret.bin.enc"
    decrypted_path = tmp_path / "decrypted" / "secret.bin"
    key_path = tmp_path / "keys" / "master.key"
    original_data = b"secret file contents\x00\xff"

    input_path.parent.mkdir()
    input_path.write_bytes(original_data)
    save_key(generate_key(), key_path)

    encrypt_file(input_path, encrypted_path, key_path)

    assert encrypted_path.is_file()
    assert encrypted_path.read_bytes() != original_data

    decrypt_file(encrypted_path, decrypted_path, key_path)

    assert decrypted_path.read_bytes() == original_data


def test_encrypt_file_raises_for_missing_input(tmp_path: Path):
    missing_path = tmp_path / "missing.txt"
    output_path = tmp_path / "encrypted.txt"
    key_path = tmp_path / "master.key"
    save_key(generate_key(), key_path)

    with pytest.raises(FileOperationError, match="Input file not found"):
        encrypt_file(missing_path, output_path, key_path)


def test_decrypt_file_raises_for_missing_input(tmp_path: Path):
    missing_path = tmp_path / "missing.enc"
    output_path = tmp_path / "decrypted.txt"
    key_path = tmp_path / "master.key"
    save_key(generate_key(), key_path)

    with pytest.raises(FileOperationError, match="Input file not found"):
        decrypt_file(missing_path, output_path, key_path)


def test_encrypt_file_propagates_missing_key_error(tmp_path: Path):
    input_path = tmp_path / "input.txt"
    input_path.write_bytes(b"secret")

    with pytest.raises(KeyNotFoundError):
        encrypt_file(
            input_path,
            tmp_path / "encrypted.txt",
            tmp_path / "missing.key",
        )


def test_decrypt_file_raises_for_invalid_encrypted_data(tmp_path: Path):
    encrypted_path = tmp_path / "encrypted.bin"
    decrypted_path = tmp_path / "decrypted.txt"
    key_path = tmp_path / "master.key"
    encrypted_path.write_bytes(b"not encrypted data")
    save_key(generate_key(), key_path)

    with pytest.raises(DecryptionError):
        decrypt_file(encrypted_path, decrypted_path, key_path)


def test_encrypt_file_raises_when_output_cannot_be_written(tmp_path: Path):
    input_path = tmp_path / "input.txt"
    key_path = tmp_path / "master.key"
    output_parent = tmp_path / "output-blocker"
    input_path.write_bytes(b"secret")
    save_key(generate_key(), key_path)
    output_parent.write_bytes(b"this is a file, not a directory")

    with pytest.raises(FileOperationError, match="Could not write encrypted file"):
        encrypt_file(input_path, output_parent / "encrypted.txt", key_path)