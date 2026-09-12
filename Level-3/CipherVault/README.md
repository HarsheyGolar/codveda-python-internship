# 🔐 CipherVault

> **A Local-First CLI Utility for Secure File Encryption and Decryption**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: Fernet](https://img.shields.io/badge/Security-Fernet%20%28AES-128%29-brightgreen)](#cryptography)
[![Status: Active Development](https://img.shields.io/badge/Status-Active-success)](#)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#-key-features)
- [Security Architecture](#-security-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
  - [Interactive Dashboard](#interactive-dashboard)
  - [CLI Commands](#cli-commands)
- [Project Structure](#-project-structure)
- [Technical Details](#-technical-details)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## Overview

**CipherVault** is a professional-grade, privacy-focused command-line tool designed for secure local file encryption and decryption. Built on industry-standard cryptography practices, it provides a seamless experience for protecting sensitive files without relying on external cloud services.

### Core Philosophy

- 🏠 **Local-First**: All encryption happens on your machine—nothing is sent to the cloud
- 🔒 **Zero Cloud**: Complete privacy through local-only operations
- ✅ **Secure by Design**: Industry-standard AES-128 encryption via Fernet
- 💻 **Developer-Friendly**: Simple CLI interface with an optional interactive dashboard
- 📦 **Zero External Dependencies** (beyond cryptography): Lightweight and dependency-conscious

---

## ✨ Key Features

### Core Encryption Capabilities
| Feature | Description |
|---------|-------------|
| **File Encryption** | AES-128 symmetric encryption with Fernet |
| **File Decryption** | Seamless restoration of encrypted files |
| **Key Management** | Generate, store, and manage encryption keys |
| **File Inspection** | View detailed metadata about files |

### User Interface
| Feature | Description |
|---------|-------------|
| **Interactive Dashboard** | User-friendly menu-driven interface |
| **CLI Commands** | Full command-line control for automation |
| **Rich Output** | Beautiful terminal formatting with progress indicators |
| **Status Monitoring** | Real-time system status and component health |

### Developer-Oriented
| Feature | Description |
|---------|-------------|
| **Modular Architecture** | Clean separation of concerns (CLI, crypto, file ops, key management) |
| **Exception Handling** | Custom exceptions for clear error diagnostics |
| **Type Hints** | Full Python type annotations for IDE support |
| **Comprehensive Testing** | Unit tests for core functionality |

---

## 🔐 Security Architecture

### Encryption Specification

CipherVault uses **Fernet** (symmetric encryption) from the `cryptography` library:

```
Algorithm:        AES-128 in CBC mode
Authentication:   HMAC using SHA256
Key Derivation:   SHA256 (built into Fernet)
Timestamp:        Included in ciphertext (prevents replay attacks)
```

### Key Management Best Practices

1. **Key Generation**: Cryptographically secure random generation
2. **Key Storage**: Plain-text key file (keep secure, don't commit to version control)
3. **Key Protection**: Store keys in restricted directories with appropriate file permissions
4. **Key Recovery**: Keep backup copies in secure, offline locations

### Data Protection Flow

```
┌─────────────────┐
│  Original File  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Read file contents (bytes) │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Load encryption key        │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Apply Fernet encryption    │
│  (AES-128 + HMAC-SHA256)    │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Write encrypted file       │
│  (*.cvault extension)       │
└─────────────────────────────┘
```

---

## 📦 Installation

### System Requirements

- **Python**: 3.10 or higher
- **OS**: Linux, macOS, Windows
- **Disk Space**: ~10MB for package installation

### Installation Methods

#### Method 1: From Repository (Development)

```bash
# Clone the repository
git clone https://github.com/HarsheyGolar/codveda-python-internship.git
cd Level-3/CipherVault

# Install in development mode with dependencies
pip install -e .
```

#### Method 2: Using pip with requirements.txt

```bash
cd Level-3/CipherVault
pip install -r requirements.txt
```

#### Method 3: Manual Setup

```bash
# Install dependencies
pip install cryptography>=43.0.0 typer rich

# Run directly
python -m ciphervault
```

### Verify Installation

```bash
# Check version
ciphervault --version

# View help
ciphervault --help
```

---

## 🚀 Quick Start

### 30-Second Setup

```bash
# 1. Generate a master encryption key
ciphervault generate-key

# 2. Encrypt a file
ciphervault encrypt path/to/sensitive-file.txt

# 3. View the encrypted file
ls -lh sensitive-file.txt.cvault

# 4. Decrypt when needed
ciphervault decrypt sensitive-file.txt.cvault
```

### What Just Happened?

1. **Key Generation**: Created `keys/master.key` with a secure 32-byte Fernet key
2. **Encryption**: Read your file, encrypted with AES-128, saved as `.cvault`
3. **Decryption**: Restored the original file by decrypting with your master key

---

## 📖 Usage Guide

### Interactive Dashboard

Launch the interactive dashboard for a guided experience:

```bash
# No arguments = interactive mode
ciphervault
```

This displays a beautiful terminal UI with menu options:

```
╔══════════════════════════════════════════════════════════╗
║                   CIPHER VAULT DASHBOARD                ║
║              1. 🔑  Generate / manage master key         ║
║              2. 🔒  Encrypt a file                       ║
║              3. 🔓  Decrypt a file                       ║
║              4. 📄  Inspect file information             ║
║              5. ↻   Refresh dashboard                   ║
║              6. ✕   Exit                                 ║
╚══════════════════════════════════════════════════════════╝
```

#### Features:
- ✅ Step-by-step guidance for each operation
- ✅ Real-time progress indicators
- ✅ Confirmation prompts for safety
- ✅ Detailed status information

---

### CLI Commands

#### `ciphervault generate-key`

Generate a new master encryption key.

**Usage:**
```bash
ciphervault generate-key [OPTIONS]
```

**Options:**
```
-o, --output PATH    Path to save the master key (default: keys/master.key)
-f, --force          Overwrite existing key without confirmation
--help               Show this message and exit
```

**Examples:**
```bash
# Generate with default location
ciphervault generate-key

# Generate with custom location
ciphervault generate-key -o ~/.ciphervault/main.key

# Force overwrite existing key
ciphervault generate-key --force
```

---

#### `ciphervault encrypt`

Encrypt a file using your master key.

**Usage:**
```bash
ciphervault encrypt FILE [OPTIONS]
```

**Arguments:**
```
FILE    Path to the file to encrypt (required)
```

**Options:**
```
-k, --key PATH       Path to master key (default: keys/master.key)
-o, --output PATH    Output file path (default: <file>.cvault)
-f, --force          Overwrite existing output without confirmation
--help               Show this message and exit
```

**Examples:**
```bash
# Simple encryption
ciphervault encrypt document.pdf

# With custom key and output
ciphervault encrypt document.pdf -k ~/.keys/backup.key -o encrypted.bin

# Overwrite existing encrypted file
ciphervault encrypt document.pdf --force
```

**Output:**
```
✔ Encryption Complete
Encrypted file created:
/absolute/path/to/document.pdf.cvault
```

---

#### `ciphervault decrypt`

Decrypt a `.cvault` file back to its original form.

**Usage:**
```bash
ciphervault decrypt FILE [OPTIONS]
```

**Arguments:**
```
FILE    Path to the .cvault file (required)
```

**Options:**
```
-k, --key PATH       Path to master key (default: keys/master.key)
-o, --output PATH    Output file path (auto-detected if omitted)
-f, --force          Overwrite existing output without confirmation
--help               Show this message and exit
```

**Examples:**
```bash
# Decrypt with automatic filename restoration
ciphervault decrypt document.pdf.cvault

# Specify custom output location
ciphervault decrypt document.pdf.cvault -o restored.pdf

# Use alternative key
ciphervault decrypt file.cvault -k ~/.keys/backup.key
```

**Output:**
```
✔ Decryption Complete
Restored file created:
/absolute/path/to/document.pdf
```

---

#### `ciphervault info`

Display detailed information about a file.

**Usage:**
```bash
ciphervault info FILE
```

**Arguments:**
```
FILE    Path to the file to inspect
```

**Example Output:**
```
╔════════════════════════════════════════╗
║      FILE INFORMATION                  ║
├────────────────────────────────────────┤
│ Name        │ document.pdf             │
│ Path        │ /home/user/documents/... │
│ Size        │ 2.45 MB                  │
│ Modified    │ 2026-09-12 14:23:45      │
╚════════════════════════════════════════╝
```

---

#### `ciphervault status`

Show CipherVault system status and component health.

**Usage:**
```bash
ciphervault status
```

**Example Output:**
```
╔════════════════════════════════════════╗
║      VAULT STATUS                      ║
├────────────────────────────────────────┤
│ Vault      │ READY                    │
│ Encryption │ ACTIVE (Fernet)          │
│ Master Key │ AVAILABLE (/path/to/key) │
╚════════════════════════════════════════╝
```

---

### Version Information

```bash
ciphervault --version
# Output: CipherVault v0.1.0
```

---

## 📁 Project Structure

```
Level-3/CipherVault/
│
├── README.md                    # This file - comprehensive documentation
├── LICENSE                      # MIT License
├── pyproject.toml              # Python project configuration
├── requirements.txt            # Python dependencies
│
├── src/
│   └── ciphervault/            # Main package
│       ├── __init__.py         # Package metadata
│       ├── __main__.py         # Entry point for python -m ciphervault
│       ├── cli.py              # Command-line interface & interactive dashboard
│       ├── crypto.py           # Encryption/decryption logic
│       ├── key_manager.py      # Key generation & management
│       ├── file_handler.py     # File I/O operations
│       └── exceptions.py       # Custom exception classes
│
├── tests/                      # Unit tests (test suite)
│   └── [test files]
│
├── keys/                       # Encryption keys (NOT committed to git)
│   └── master.key             # Default master encryption key
│
├── examples/                   # Example files for documentation
│   └── [sample files]
│
└── .gitignore                 # Git ignore rules (keys, caches, etc.)
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `cli.py` | Typer application, interactive dashboard, command implementations, rich output |
| `crypto.py` | Fernet encryption/decryption, cryptographic operations |
| `key_manager.py` | Key generation, loading, saving, validation |
| `file_handler.py` | File reading/writing, integration of crypto + key operations |
| `exceptions.py` | Custom exception classes for error handling |

---

## 🔧 Technical Details

### Dependencies

```
cryptography>=43.0.0    # Industry-standard cryptographic library
typer>=0.9.0            # CLI framework
rich>=13.0.0            # Terminal output formatting
```

### Python Version Support

- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12+

### Supported Platforms

- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ macOS (Intel & Apple Silicon)
- ✅ Windows (PowerShell, CMD)

---

## 🔌 API Reference

### Core Functions

#### `crypto.encrypt_data(data: bytes, key: bytes) -> bytes`

Encrypt raw bytes using Fernet encryption.

```python
from ciphervault.crypto import encrypt_data
from ciphervault.key_manager import load_key

key = load_key()
plaintext = b"Hello, World!"
ciphertext = encrypt_data(plaintext, key)
```

#### `crypto.decrypt_data(encrypted_data: bytes, key: bytes) -> bytes`

Decrypt Fernet-encrypted bytes.

```python
from ciphervault.crypto import decrypt_data
from ciphervault.key_manager import load_key

key = load_key()
plaintext = decrypt_data(ciphertext, key)
```

#### `key_manager.generate_key() -> bytes`

Generate a new cryptographically secure Fernet key.

```python
from ciphervault.key_manager import generate_key, save_key

key = generate_key()
save_key(key, path="my_key.key")
```

#### `file_handler.encrypt_file(input_path: Path, output_path: Path, key_path: Path) -> None`

Encrypt a file on disk.

```python
from pathlib import Path
from ciphervault.file_handler import encrypt_file

encrypt_file(
    Path("document.pdf"),
    Path("document.pdf.cvault"),
    Path("keys/master.key")
)
```

#### `file_handler.decrypt_file(input_path: Path, output_path: Path, key_path: Path) -> None`

Decrypt a file on disk.

```python
from pathlib import Path
from ciphervault.file_handler import decrypt_file

decrypt_file(
    Path("document.pdf.cvault"),
    Path("document.pdf"),
    Path("keys/master.key")
)
```

### Exception Classes

```python
from ciphervault.exceptions import (
    CipherVaultError,           # Base exception
    EncryptionError,            # Encryption failed
    DecryptionError,            # Decryption failed
    InvalidKeyError,            # Key is invalid
    KeyNotFoundError,           # Key file not found
    FileOperationError,         # File I/O error
)
```

---

## ⚙️ Configuration

### Key Storage Locations

By default, CipherVault stores keys in:

```
./keys/master.key          # Default location
~/.ciphervault/key.pem     # Recommended secure location
/etc/ciphervault/key       # System-wide (requires sudo)
```

### Custom Configuration

Set custom key paths via CLI options:

```bash
# Use alternative key for encryption
ciphervault encrypt file.txt -k ~/.secure/my_key.key

# Generate key in custom location
ciphervault generate-key -o /var/ciphervault/production.key
```

### Environment Setup

For system-wide usage, add alias:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias cv="ciphervault"

# Use as: cv encrypt file.txt
```

---

## 💡 Examples

### Example 1: Encrypt Sensitive Documents

```bash
# Workflow: Protect important files
ciphervault generate-key

# Encrypt tax returns
ciphervault encrypt ~/Documents/2025_tax_return.pdf
ciphervault encrypt ~/Documents/bank_statements.csv

# Verify encryption
ls -lh ~/Documents/*.cvault

# Later: Decrypt when needed
ciphervault decrypt ~/Documents/2025_tax_return.pdf.cvault
```

### Example 2: Backup Automation

```bash
#!/bin/bash
# Script to encrypt nightly backups

BACKUP_DIR="~/backups"
ENCRYPTED_DIR="~/encrypted_backups"
KEY_PATH="~/.ciphervault/backup.key"

# Create backup
tar -czf "$BACKUP_DIR/backup_$(date +%Y%m%d).tar.gz" ~/important_data

# Encrypt all new backups
for file in "$BACKUP_DIR"/*.tar.gz; do
    ciphervault encrypt "$file" -k "$KEY_PATH" -o "$ENCRYPTED_DIR/$(basename $file).cvault"
done

echo "✅ Backup encryption complete"
```

### Example 3: Python Integration

```python
from pathlib import Path
from ciphervault.file_handler import encrypt_file, decrypt_file
from ciphervault.key_manager import generate_key, save_key

# Generate and save key
key = generate_key()
key_path = Path("my_keys/app.key")
save_key(key, key_path)

# Encrypt sensitive data file
encrypt_file(
    input_path=Path("config.secrets.yaml"),
    output_path=Path("config.secrets.yaml.cvault"),
    key_path=key_path
)

# Later: decrypt for use
decrypt_file(
    input_path=Path("config.secrets.yaml.cvault"),
    output_path=Path("config.secrets.yaml"),
    key_path=key_path
)
```

### Example 4: Interactive Workflow

```bash
# Start interactive dashboard
ciphervault

# Follow prompts:
# 1. Select "2" to encrypt file
# 2. Enter: ~/Documents/credentials.json
# 3. Confirm encryption
# 4. View success message with output path
```

---

## 🐛 Troubleshooting

### Issue: "Master Key Not Found"

**Problem**: Error message when running encrypt/decrypt without generating a key first.

**Solution**:
```bash
ciphervault generate-key
```

---

### Issue: "The key may be incorrect or the data may be corrupted"

**Problem**: Decryption fails with this error.

**Causes & Solutions**:
1. **Wrong Key**: Verify you're using the correct key file
2. **Corrupted File**: The encrypted file may be damaged; try with a backup
3. **File Modification**: The encrypted file was modified after encryption

**Debug**:
```bash
# Check file integrity
ciphervault info encrypted_file.cvault

# Verify key matches
ciphervault info keys/master.key
```

---

### Issue: "Output file already exists"

**Problem**: Encryption/decryption fails because output file exists.

**Solution**:
```bash
# Option 1: Use --force flag
ciphervault encrypt file.txt --force

# Option 2: Specify different output
ciphervault encrypt file.txt -o file_v2.txt.cvault

# Option 3: Remove existing file
rm file.txt.cvault
ciphervault encrypt file.txt
```

---

### Issue: Permission Denied on Key File

**Problem**: Cannot read/write key file.

**Solution**:
```bash
# Fix permissions (Linux/macOS)
chmod 600 keys/master.key
chmod 700 keys/

# On Windows, use File Properties > Security
```

---

### Issue: "File not found" Errors

**Problem**: Input file doesn't exist or path is incorrect.

**Solution**:
```bash
# Use absolute paths
ciphervault encrypt /absolute/path/to/file.txt

# Check file exists
ls -l /path/to/file.txt

# Use quotes for paths with spaces
ciphervault encrypt "/path/to/my file.txt"
```

---

## 📝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional encryption algorithms (AES-256, ChaCha20)
- [ ] Batch file encryption/decryption
- [ ] Key rotation utilities
- [ ] Configuration file support
- [ ] Web UI dashboard
- [ ] Integration tests
- [ ] Performance benchmarks

### Development Setup

```bash
# Clone repository
git clone https://github.com/HarsheyGolar/codveda-python-internship.git
cd Level-3/CipherVault

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black src/
pylint src/
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Harshey Golar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 Support & Questions

- 📧 **Issues**: Use [GitHub Issues](https://github.com/HarsheyGolar/codveda-python-internship/issues)
- 💬 **Discussions**: Available on the repository
- 🔗 **Documentation**: See this README for comprehensive guides

---

## 🙏 Acknowledgments

- Built with [Fernet](https://cryptography.io/en/latest/fernet/) from `cryptography`
- CLI powered by [Typer](https://typer.tiangolo.com/)
- Terminal UI enhanced with [Rich](https://rich.readthedocs.io/)
- Developed as part of Codveda Python Internship Program

---

**🔐 Stay secure. Encrypt responsibly. Protect your data.** 🔐

---

<div align="center">

**[Back to Top](#-ciphervault)** • 
**[View on GitHub](https://github.com/HarsheyGolar/codveda-python-internship/tree/main/Level-3/CipherVault)**

Last Updated: 2026-09-12 | Version: 0.1.0

</div>
