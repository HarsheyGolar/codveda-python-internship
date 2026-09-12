from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, TypeVar

import typer  # type: ignore[reportMissingImports]
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from .exceptions import CipherVaultError
from .file_handler import decrypt_file, encrypt_file
from .key_manager import (
    DEFAULT_KEY_PATH,
    generate_key,
    key_exists,
    load_key,
    save_key,
)

#────────────────────────────────────────────────────────────────
# App configuration
#────────────────────────────────────────────────────────────────

APP_NAME = "CipherVault"
VERSION = "0.1.0"

console = Console(
    theme = Theme(
        {
            "brand": "bold bright_cyan",
            "brand2": "bold medium_purple1",
            "success": "bold spring_green3",
            "error": "bold red3",
            "warning": "bold gold3",
            "info": "bold cyan",
            "muted": "grey62",
            "path": "underline bright_cyan",
        }
    ),
    highlight=False
)

T = TypeVar("T")

app = typer.Typer(
    name="ciphervault",
    help="Secure local file encryption and decryption.",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=False,
)

#────────────────────────────────────────────────────────────────
# Branding
#────────────────────────────────────────────────────────────────

BANNER = r"""
   ╔══════════════════════════════════════════════════════════╗
   ║                                                          ║
   ║       ██████╗ ██╗██████╗ ██╗  ██╗███████╗██████╗       ║
   ║      ██╔════╝ ██║██╔══██╗██║  ██║██╔════╝██╔══██╗      ║
   ║      ██║      ██║██████╔╝███████║█████╗  ██████╔╝      ║
   ║      ██║      ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗      ║
   ║      ╚██████╗ ██║██║     ██║  ██║███████╗██║  ██║      ║
   ║       ╚═════╝ ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ║
   ║                                                          ║
   ║                 SECURE LOCAL FILE VAULT                  ║
   ╚══════════════════════════════════════════════════════════╝
   """

def show_banner() -> None:
    """Display the CipherVault Startup banner."""
    console.print(Align.center(f"[brand]{BANNER}[/brand]"))
    console.print(
        Align.center(
            f"[muted]v{VERSION} • local-first • zero cloud • secure by design[/muted]"
        )
    )
    console.print()

def section_header(title: str, icon: str) -> None:
    """Display a consistent section header."""
    console.print()
    console.print(
        Rule(
            f"[brand2]{icon} {APP_NAME} • {title}[/brand2]",
            style="medium_purple1",
        )
    )
    console.print()

def success_panel(title: str, message: str) -> None:
    """Display a successfull operation."""
    console.print(
        Panel(
            message,
            title=f"[success]✔ {title}[/success]",
            border_style="spring_green3",
            padding=(1, 2),
        )
    )

def error_panel(title: str, message: str) -> None:
    """Display an error."""
    console.print(
        Panel(
            message,
            title=f"[error]✖ {title}[/error]",
            border_style="red3",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )

# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────

def format_size(num_bytes: int) -> str:
    """Convert bytes into a human_readable size."""
    size = float(num_bytes)

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            if unit == "B":
                return f"{size:.0f} {unit}"
            return f"{size:.2f} PB"

def run_with_status(
        message: str,
        func: callable[..., T],
        *args,
        **kwargs,
) -> T:
    """Run a function with an animated terminal spinner."""
    with console.status(
        f"[brand2]{message}[/brand2]",
        spinner="dots12",
    ):
        return func(*args, **kwargs)

def validate_file(filepath: str) -> Path:
    """Validate that a  path points to a real file."""
    path = Path(filepath)

    if not path.is_file():
        raise IsADirectoryError(
            f"Expected a file, but received a directory: {path}"
        )

    return path

def resolve_output_path(
    input_path: Path,
    mode: str,
) -> Path:
    """Generate a sensible output filename."""
    if mode == "encrypt":
        return input_path.with_name(
            f"{input_path.name}.cvault"
        )

    # decrypt
    if input_path.name.endswith(".cvault"):
        original_name = input_path.name[:-7]
        return input_path.with_name(original_name)

    return input_path.with_name(
        f"{input_path.stem}.decrypted{input_path.suffix}"
    )


def ensure_output_safe(output_path: Path, force: bool) -> None:
    """Prevent accidental overwriting unless explicitly requested."""
    if output_path.exists() and not force:
        raise CipherVaultError(
            f"Output file already exists: {output_path}\n"
            "Use --force to overwrite it."
        )


def show_status() -> None:
    """Display current CipherVault status."""
    section_header("Vault Status", "◆")

    table = Table(
        box=box.ROUNDED,
        border_style="medium_purple1",
        padding=(0, 2),
    )

    table.add_column("Component", style="info")
    table.add_column("Status")
    table.add_column("Details", style="muted")

    key_path = Path(DEFAULT_KEY_PATH)

    table.add_row(
        "Vault",
        "[success]READY[/success]",
        "Local filesystem",
    )

    table.add_row(
        "Encryption",
        "[success]ACTIVE[/success]",
        "Fernet",
    )

    if key_exists(key_path):
        table.add_row(
            "Master Key",
            "[success]AVAILABLE[/success]",
            str(key_path),
        )
    else:
        table.add_row(
            "Master Key",
            "[warning]MISSING[/warning]",
            "Run generate-key",
        )

    console.print(table)


# ─────────────────────────────────────────────────────────────────────────────
# Interactive dashboard
# ─────────────────────────────────────────────────────────────────────────────

def interactive_menu() -> None:
    """Launch the interactive CipherVault dashboard."""
    while True:
        console.clear()
        show_banner()
        show_status()

        console.print()

        menu = Table(
            box=None,
            show_header=False,
            padding=(0, 1),
        )

        menu.add_column("Key", style="brand2", width=6)
        menu.add_column("Action", style="white")

        menu.add_row("1", "🔑  Generate / manage master key")
        menu.add_row("2", "🔒  Encrypt a file")
        menu.add_row("3", "🔓  Decrypt a file")
        menu.add_row("4", "📄  Inspect file information")
        menu.add_row("5", "↻   Refresh dashboard")
        menu.add_row("6", "✕   Exit")

        console.print(
            Panel(
                menu,
                title="[brand]CipherVault Dashboard[/brand]",
                border_style="medium_purple1",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[brand2]› Select an action[/brand2]",
            choices=["1", "2", "3", "4", "5", "6"],
        )

        try:
            if choice == "1":
                interactive_generate_key()
            elif choice == "2":
                interactive_encrypt()
            elif choice == "3":
                interactive_decrypt()
            elif choice == "4":
                interactive_info()
            elif choice == "5":
                continue
            elif choice == "6":
                console.print("\n[muted]Goodbye. Stay secure. 🔐[/muted]\n")
                return

        except CipherVaultError as error:
            error_panel("Operation Failed", str(error))

        except KeyboardInterrupt:
            console.print("\n[warning]Operation cancelled.[/warning]")

        Prompt.ask(
            "\n[muted]Press Enter to return to the dashboard[/muted]",
            default="",
            show_default=False,
        )


def interactive_generate_key() -> None:
    """Generate a master key from the dashboard."""
    section_header("Key Generation", "🔑")

    key_path = Path(
        Prompt.ask(
            "Key path",
            default=str(DEFAULT_KEY_PATH),
        )
    )

    if key_path.exists():
        if not Confirm.ask(
            "[warning]Key already exists. Overwrite it?[/warning]",
            default=False,
        ):
            console.print("[muted]Cancelled.[/muted]")
            return

    key = run_with_status(
        "Generating secure encryption key...",
        generate_key,
    )

    save_key(key, key_path)

    success_panel(
        "Key Generated",
        (
            f"Master key saved to:\n"
            f"[path]{key_path.resolve()}[/path]\n\n"
            "[warning]Keep this key safe. Losing it means losing access "
            "to encrypted data.[/warning]"
        ),
    )


def interactive_encrypt() -> None:
    """Encrypt a file from the interactive menu."""
    section_header("Encrypt File", "🔒")

    input_path = validate_file(
        Prompt.ask("File to encrypt")
    )

    key_path = Path(
        Prompt.ask(
            "Key path",
            default=str(DEFAULT_KEY_PATH),
        )
    )

    output_path = Path(
        Prompt.ask(
            "Output file",
            default=str(resolve_output_path(input_path, "encrypt")),
        )
    )

    ensure_output_safe(output_path, force=False)

    if not Confirm.ask(
        f"[warning]Encrypt {input_path.name}?[/warning]",
        default=True,
    ):
        console.print("[muted]Cancelled.[/muted]")
        return

    run_with_status(
        "Encrypting file...",
        encrypt_file,
        input_path,
        output_path,
        key_path,
    )

    success_panel(
        "Encryption Complete",
        (
            f"Source\n[path]{input_path.resolve()}[/path]\n\n"
            f"Encrypted output\n[path]{output_path.resolve()}[/path]"
        ),
    )


def interactive_decrypt() -> None:
    """Decrypt a file from the interactive menu."""
    section_header("Decrypt File", "🔓")

    input_path = validate_file(
        Prompt.ask("Encrypted file")
    )

    key_path = Path(
        Prompt.ask(
            "Key path",
            default=str(DEFAULT_KEY_PATH),
        )
    )

    output_path = Path(
        Prompt.ask(
            "Output file",
            default=str(resolve_output_path(input_path, "decrypt")),
        )
    )

    ensure_output_safe(output_path, force=False)

    if not Confirm.ask(
        f"[warning]Decrypt {input_path.name}?[/warning]",
        default=True,
    ):
        console.print("[muted]Cancelled.[/muted]")
        return

    run_with_status(
        "Decrypting file...",
        decrypt_file,
        input_path,
        output_path,
        key_path,
    )

    success_panel(
        "Decryption Complete",
        (
            f"Encrypted source\n[path]{input_path.resolve()}[/path]\n\n"
            f"Restored output\n[path]{output_path.resolve()}[/path]"
        ),
    )


def interactive_info() -> None:
    """Show file information from the interactive menu."""
    filepath = validate_file(
        Prompt.ask("File path")
    )

    show_file_info(filepath)


# ─────────────────────────────────────────────────────────────────────────────
# CLI commands
# ─────────────────────────────────────────────────────────────────────────────

@app.callback(invoke_without_command=True)
def cli_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show CipherVault version.",
    ),
) -> None:
    
    """🔐 CipherVault — secure local file encryption."""
    if version:
        console.print(
            f"[brand]{APP_NAME}[/brand] v{VERSION}"
        )
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        interactive_menu()


@app.command("generate-key")
def generate_key_command(
    output: str = typer.Option(
        str(DEFAULT_KEY_PATH),
        "--output",
        "-o",
        help="Where to save the master key.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing key.",
    ),
) -> None:
    """🔑 Generate a new master encryption key."""
    section_header("Key Generation", "🔑")

    output_path = Path(output)

    if output_path.exists() and not force:
        error_panel(
            "Key Already Exists",
            (
                f"[path]{output_path}[/path] already exists.\n\n"
                "Use [brand2]--force[/brand2] only when you intentionally "
                "want to replace the old key."
            ),
        )
        raise typer.Exit(code=1)

    key = run_with_status(
        "Generating secure encryption key...",
        generate_key,
    )

    save_key(key, output_path)

    success_panel(
        "Key Generated",
        (
            f"Saved to\n"
            f"[path]{output_path.resolve()}[/path]\n\n"
            "[warning]Keep this key safe.[/warning]"
        ),
    )


@app.command()
def encrypt(
    file: str = typer.Argument(
        ...,
        help="Path to the file to encrypt.",
    ),
    key: str = typer.Option(
        str(DEFAULT_KEY_PATH),
        "--key",
        "-k",
        help="Path to the master key.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path. Defaults to <file>.cvault.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing output file.",
    ),
) -> None:
    """🔒 Encrypt a file."""
    section_header("Encrypt", "🔒")

    input_path = validate_file(file)
    key_path = Path(key)

    if not key_path.is_file():
        error_panel(
            "Master Key Not Found",
            (
                f"Key not found at:\n"
                f"[path]{key_path.resolve()}[/path]\n\n"
                "Run [brand2]ciphervault generate-key[/brand2] first."
            ),
        )
        raise typer.Exit(code=1)

    output_path = (
        Path(output)
        if output
        else resolve_output_path(input_path, "encrypt")
    )

    ensure_output_safe(output_path, force)

    console.print(
        f"[info]Source[/info]  [path]{input_path.resolve()}[/path]"
    )
    console.print(
        f"[info]Output[/info]  [path]{output_path.resolve()}[/path]"
    )
    console.print(
        f"[info]Key[/info]     [path]{key_path.resolve()}[/path]"
    )
    console.print()

    try:
        run_with_status(
            "Encrypting...",
            encrypt_file,
            input_path,
            output_path,
            key_path,
        )

    except CipherVaultError as error:
        error_panel("Encryption Failed", str(error))
        raise typer.Exit(code=1)

    success_panel(
        "Encryption Complete",
        (
            f"Encrypted file created:\n"
            f"[path]{output_path.resolve()}[/path]"
        ),
    )


@app.command()
def decrypt(
    file: str = typer.Argument(
        ...,
        help="Path to the .cvault file.",
    ),
    key: str = typer.Option(
        str(DEFAULT_KEY_PATH),
        "--key",
        "-k",
        help="Path to the master key.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path. Automatically restored when omitted.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing output file.",
    ),
) -> None:
    """🔓 Decrypt a CipherVault file."""
    section_header("Decrypt", "🔓")

    input_path = validate_file(file)
    key_path = Path(key)

    if not key_path.is_file():
        error_panel(
            "Master Key Not Found",
            f"Key not found at [path]{key_path.resolve()}[/path]",
        )
        raise typer.Exit(code=1)

    output_path = (
        Path(output)
        if output
        else resolve_output_path(input_path, "decrypt")
    )

    ensure_output_safe(output_path, force)

    console.print(
        f"[info]Source[/info]  [path]{input_path.resolve()}[/path]"
    )
    console.print(
        f"[info]Output[/info]  [path]{output_path.resolve()}[/path]"
    )
    console.print(
        f"[info]Key[/info]     [path]{key_path.resolve()}[/path]"
    )
    console.print()

    try:
        run_with_status(
            "Decrypting...",
            decrypt_file,
            input_path,
            output_path,
            key_path,
        )

    except CipherVaultError as error:
        error_panel(
            "Decryption Failed",
            (
                f"{error}\n\n"
                "[muted]The key may be incorrect or the encrypted "
                "data may be corrupted.[/muted]"
            ),
        )
        raise typer.Exit(code=1)

    success_panel(
        "Decryption Complete",
        (
            f"Restored file created:\n"
            f"[path]{output_path.resolve()}[/path]"
        ),
    )


@app.command()
def status() -> None:
    """📊 Show CipherVault status."""
    show_banner()
    show_status()


def show_file_info(filepath: Path) -> None:
    """Render detailed file information."""
    section_header("File Information", "📄")

    stat = filepath.stat()

    table = Table(
        box=box.ROUNDED,
        border_style="medium_purple1",
        show_header=False,
        padding=(0, 2),
    )

    table.add_column(style="info", justify="right")
    table.add_column(style="white")

    table.add_row("Name", filepath.name)
    table.add_row("Path", str(filepath.resolve()))
    table.add_row("Size", format_size(stat.st_size))
    table.add_row(
        "Modified",
        time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(stat.st_mtime),
        ),
    )

    console.print(table)


@app.command()
def info(
    file: str = typer.Argument(
        ...,
        help="Path to inspect.",
    ),
) -> None:
    """📄 Show information about a file."""
    filepath = validate_file(file)
    show_file_info(filepath)

def main() -> None:
    """Launch the CipherVault CLI."""
    app()

if __name__ == "__main__":
    app()