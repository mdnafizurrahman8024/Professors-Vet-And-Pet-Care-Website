#!/usr/bin/env python
"""
Safe local development server launcher for Professor's Vet & Pet Care.

Why this exists
---------------
`python manage.py runserver` fails (or silently shows the wrong app / a blank
page / an error page) when:
  * port 8000 is already taken by another program,
  * dependencies are missing,
  * static/ or media/ folders do not exist yet,
  * pending migrations were never applied.

This script checks all of that first, picks a FREE port automatically and then
starts Django's dev server on it. New features can be added freely: as long as
`python manage.py check` passes, this launcher keeps working.

Usage:
    python run_server.py              # auto port (8000 if free, else next free)
    python run_server.py 8010         # force a port
    python run_server.py --noreload   # disable the auto-reloader
"""

import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFERRED_PORTS = range(8000, 8011)


def log(msg, color=False):
    if color and os.name == "nt":
        print(msg)
    else:
        print(msg)


def fail(msg):
    print("")
    print("  [ERROR] " + msg)
    print("")
    sys.exit(1)


def port_is_free(port):
    """True only if nothing is listening AND we are allowed to bind it."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # If something is listening, connect() succeeds -> port busy.
        s.settimeout(0.3)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def ensure_dependencies():
    missing = []
    for module in ("django", "dotenv", "whitenoise", "dj_database_url", "PIL"):
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    if not missing:
        return
    print("  Installing missing dependencies: " + ", ".join(missing))
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=ROOT)
    if result.returncode != 0:
        fail("Could not install dependencies. Run: python -m pip install -r requirements.txt")


def pick_port(argv):
    for arg in argv:
        if arg.isdigit():
            requested = int(arg)
            if not port_is_free(requested):
                fail("Port {} is already used by another program. Try: python run_server.py {}".format(
                    requested, requested + 1))
            return requested
    for candidate in PREFERRED_PORTS:
        if port_is_free(candidate):
            return candidate
    fail("No free port found between 8000 and 8010.")


def main():
    os.chdir(ROOT)
    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a for a in sys.argv[1:] if a.startswith("-")]

    print("")
    print("  Professor's Vet & Pet Care - starting local server...")
    print("  Python: " + sys.version.split()[0])

    ensure_dependencies()

    port = pick_port(argv)

    # Local run is always DEBUG=True; this also fixes CSRF / static / media
    # behaviour for http://127.0.0.1:<port> without touching .env.
    os.environ["DEBUG"] = "True"
    os.environ["DJANGO_PORT"] = str(port)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vetcare.settings")

    # Folders referenced by settings must exist, otherwise Django warns.
    for folder in ("static", "media"):
        (ROOT / folder).mkdir(exist_ok=True)

    # Fail fast on misconfiguration, before the browser shows an error page.
    check = subprocess.run([sys.executable, "manage.py", "check"], cwd=ROOT)
    if check.returncode != 0:
        fail("Django system check failed. Fix the errors above.")

    # Apply pending migrations (safe, only unapplied ones run).
    migrate = subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], cwd=ROOT)
    if migrate.returncode != 0:
        fail("Database migration failed. See the error above.")

    print("")
    print("  Local site  ->  http://127.0.0.1:{}/".format(port))
    print("  Admin panel ->  http://127.0.0.1:{}/admin/   (admin / admin)".format(port))
    print("  Press CTRL+C to stop.")
    print("")

    cmd = [sys.executable, "manage.py", "runserver", "127.0.0.1:{}".format(port)] + flags
    try:
        subprocess.run(cmd, cwd=ROOT)
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
