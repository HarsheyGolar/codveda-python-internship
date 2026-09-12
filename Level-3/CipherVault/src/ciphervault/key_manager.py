from pathlib import Path
from cryptography.fernet import Fernet

from .exceptions import InvalidKeyError, KeyNotFoundError

DEFAULT_KEY_PATH = Path("keys") / "master.key"

def generate_key() -> bytes:
    """Generate a new Fernet encryption key."""
    return Fernet.generate_key()

def save_key(key: bytes, key_path: Path = DEFAULT_KEY_PATH) -> None:
    """Save an encryption key to disk."""
    key_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        key_path.write_bytes(key)
    except OSError as error:
        raise InvalidKeyError(f"Could not save encryption key: {error}") from error

def load_key(key_path: Path = DEFAULT_KEY_PATH) -> bytes:
    """Load and validate an encryption key from disk."""
    if not key_path.exists():
        raise KeyNotFoundError(f"Encryption key not found: {key_path}")

    try:
        key = key_path.read_bytes()
        Fernet(key)
    except OSError as error:
        raise InvalidKeyError(f"could not read encryption key: {error}") from error
    except (ValueError, TypeError) as error:
        raise InvalidKeyError("The encryption key is invalid.") from error

    return key

def key_exists(key_path: Path = DEFAULT_KEY_PATH) -> bool:
    """Return True if the encryption key exists."""
    return key_path.is_file()