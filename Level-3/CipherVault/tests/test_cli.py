from pathlib import Path

from typer.testing import CliRunner

from ciphervault.cli import app, ensure_output_safe, resolve_output_path
from ciphervault.exceptions import CipherVaultError


runner = CliRunner()


def test_status_command(tmp_path, monkeypatch):
    """Status command should run successfully."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Vault" in result.stdout
    assert "Master Key" in result.stdout


def test_generate_key_command(tmp_path, monkeypatch):
    """Generate-key should create a master key."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["generate-key"])

    assert result.exit_code == 0

    key_path = tmp_path / "keys" / "master.key"
    assert key_path.exists()
    assert key_path.is_file()
    assert key_path.read_bytes()


def test_encrypt_and_decrypt_commands(tmp_path, monkeypatch):
    """CLI should encrypt and decrypt a file successfully."""
    monkeypatch.chdir(tmp_path)

    input_file = tmp_path / "secret.txt"
    encrypted_file = tmp_path / "secret.txt.cvault"
    restored_file = tmp_path / "restored_secret.txt"

    original_content = 'groq_api_key="fake-test-key-123"'
    input_file.write_text(original_content, encoding="utf-8")

    # Generate master key first.
    key_result = runner.invoke(app, ["generate-key"])
    assert key_result.exit_code == 0

    # Encrypt.
    encrypt_result = runner.invoke(
        app,
        [
            "encrypt",
            str(input_file),
            "--output",
            str(encrypted_file),
        ],
    )

    assert encrypt_result.exit_code == 0
    assert encrypted_file.exists()
    assert encrypted_file.read_bytes() != input_file.read_bytes()

    # Decrypt.
    decrypt_result = runner.invoke(
        app,
        [
            "decrypt",
            str(encrypted_file),
            "--output",
            str(restored_file),
        ],
    )

    assert decrypt_result.exit_code == 0
    assert restored_file.exists()
    assert restored_file.read_text(encoding="utf-8") == original_content


def test_info_command(tmp_path, monkeypatch):
    """Info command should display file information."""
    monkeypatch.chdir(tmp_path)

    test_file = tmp_path / "sample.txt"
    test_file.write_text("CipherVault test", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "info",
            str(test_file),
        ],
    )

    assert result.exit_code == 0
    assert "sample.txt" in result.stdout


def test_encrypt_missing_file(tmp_path, monkeypatch):
    """Encrypt should fail when the input path is not a valid file."""
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["generate-key"])

    result = runner.invoke(
        app,
        [
            "encrypt",
            str(tmp_path / "missing.txt"),
        ],
    )

    assert result.exit_code != 0
    assert "expected a file" in str(result.exception).lower()


def test_output_safety():
    """Existing output should be rejected without force."""
    output_path = Path("test-output.txt")

    try:
        output_path.write_text("existing", encoding="utf-8")

        try:
            ensure_output_safe(output_path, force=False)
            raise AssertionError("Expected CipherVaultError")
        except CipherVaultError as error:
            assert "already exists" in str(error)
            assert "--force" in str(error)
    finally:
        if output_path.exists():
            output_path.unlink()


def test_resolve_encrypt_output(tmp_path):
    """Encrypt output should use the .cvault extension."""
    input_file = tmp_path / "secret.txt"

    output = resolve_output_path(input_file, "encrypt")

    assert output == tmp_path / "secret.txt.cvault"


def test_resolve_decrypt_output(tmp_path):
    """Decrypt output should remove the .cvault extension."""
    encrypted_file = tmp_path / "secret.txt.cvault"

    output = resolve_output_path(encrypted_file, "decrypt")

    assert output == tmp_path / "secret.txt"


def test_resolve_output_for_non_cvault_file(tmp_path):
    """Decrypting a non-.cvault file should use a decrypted filename."""
    input_file = tmp_path / "secret.txt"

    output = resolve_output_path(input_file, "decrypt")

    assert output == tmp_path / "secret.decrypted.txt"