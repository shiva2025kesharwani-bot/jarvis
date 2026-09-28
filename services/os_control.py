import os
import subprocess
import sys

def open_file(path: str):
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def set_volume(level: int):
    """Best-effort volume control (0-100)."""
    level = max(0, min(100, level))
    try:
        if sys.platform.startswith("win"):
            # requires nircmd or pycaw; placeholder
            pass
        elif sys.platform == "darwin":
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        else:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{level}%"])
    except Exception:
        pass