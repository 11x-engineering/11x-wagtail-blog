#!/usr/bin/env python
import os
from pathlib import Path
import sys

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).absolute().parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
