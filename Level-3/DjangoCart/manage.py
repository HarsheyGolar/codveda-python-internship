import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangocart.settings")

    try:
        from django.core.management import execute_from_command_line  # pyright: ignore[reportMissingImports]
    except ImportError as exc:
        raise ImportError(
            "Couldn't import django. Make sure Django is Installed."
            "and your virtual environment is acivated"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__=="__main__":
    main()