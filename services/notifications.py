import sys
import subprocess

def notify(title: str, message: str):
    try:
        if sys.platform == "darwin":
            subprocess.run([
                "osascript", "-e",
                f'display notification "{message}" with title "{title}"'
            ])
        elif sys.platform.startswith("win"):
            # Simple fallback; use win10toast for nicer toasts
            pass
        else:
            subprocess.run(["notify-send", title, message])
    except Exception:
        pass