class CipherVaultError(Exception):
    """Base  Exception for all CipherVault errors."""

class KeyError(CipherVaultError):
    """Raised when a key operation fails."""

class KeyNotFoundError(KeyError):
    """Raised when the encryption key cannot be found."""

class InvalidKeyError(KeyError):
    """Raised when the encryption key is invalid."""

class FileOperationError(CipherVaultError):
    """Raised when a file operation fails."""

class EncryptionError(CipherVaultError):
    """Raised when encryption fails."""

class DecryptionError(CipherVaultError):
    """Raised when decryption fails."""