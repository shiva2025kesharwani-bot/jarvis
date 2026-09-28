import os
import sys
import traceback

# Fix working directory (crucial for startup launch)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def main():
    try:
        from assistant.daemon import run_daemon
        run_daemon()
    except Exception:
        # Write crash log so we can debug
        with open("data/logs/crash.log", "a", encoding="utf-8") as f:
            f.write("\n\n=== CRASH ===\n")
            traceback.print_exc(file=f)


if __name__ == "__main__":
    main()