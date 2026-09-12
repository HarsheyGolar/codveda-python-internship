from pathlib import Path

from .crypto import decrypt_data, encrypt_data
from .exceptions import DecryptionError, EncryptionError, FileOperationError
from .key_manager import load_key


def encrypt_file(
    input_path: Path,
    output_path: Path,
    key_path: Path,
) -> None:
    """Encrypt a file and write the encrypted data to the output path."""

    if not input_path.is_file():
        raise FileOperationError(
            f"Input file not found: {input_path}"
        )

    try:
        data = input_path.read_bytes()
    except OSError as error:
        raise FileOperationError(
            f"Could not read input file: {input_path}"
        ) from error

    key = load_key(key_path)

    try:
        encrypted_data = encrypt_data(data, key)
    except EncryptionError:
        raise
    except Exception as error:
        raise EncryptionError(
            f"Could not encrypt file: {input_path}"
        ) from error

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(encrypted_data)
    except OSError as error:
        raise FileOperationError(
            f"Could not write encrypted file: {output_path}"
        ) from error


def decrypt_file(
    input_path: Path,
    output_path: Path,
    key_path: Path,
) -> None:
    """Decrypt a file and write the original data to the output path."""

    if not input_path.is_file():
        raise FileOperationError(
            f"Input file not found: {input_path}"
        )

    try:
        encrypted_data = input_path.read_bytes()
    except OSError as error:
        raise FileOperationError(
            f"Could not read encrypted file: {input_path}"
        ) from error

    key = load_key(key_path)

    try:
        decrypted_data = decrypt_data(encrypted_data, key)
    except DecryptionError:
        raise
    except Exception as error:
        raise DecryptionError(
            f"Could not decrypt file: {input_path}"
        ) from error

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(decrypted_data)
    except OSError as error:
        raise FileOperationError(
            f"Could not write decrypted file: {output_path}"
        ) from error