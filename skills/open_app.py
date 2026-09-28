import os
import shutil
import subprocess
import sys
import webbrowser
import urllib.parse
from skills.base import BaseSkill

# Common web services that user might say without "open"
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://www.github.com",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "chatgpt": "https://chat.openai.com",
    "gemini": "https://gemini.google.com",
    "netflix": "https://www.netflix.com",
    "spotify web": "https://open.spotify.com",
}


def _search_start_menu(name):
    """Search Windows Start Menu shortcuts for an app."""
    if sys.platform != "win32":
        return None
    search_dirs = [
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs"),
    ]
    name_l = name.lower()
    best = None
    for base in search_dirs:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            for f in files:
                if not f.lower().endswith(".lnk"):
                    continue
                clean = f.lower().replace(".lnk", "")
                if name_l == clean:
                    return os.path.join(root, f)
                if name_l in clean and best is None:
                    best = os.path.join(root, f)
    return best


def _search_program_files(name):
    """Deep search in Program Files for an exe matching name."""
    if sys.platform != "win32":
        return None
    search_bases = [
        os.path.expandvars(r"%ProgramFiles%"),
        os.path.expandvars(r"%ProgramFiles(x86)%"),
        os.path.expandvars(r"%LocalAppData%"),
    ]
    name_l = name.lower()
    for base in search_bases:
        if not base or not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            depth = root[len(base):].count(os.sep)
            if depth > 3:
                dirs[:] = []
                continue
            for f in files:
                if f.lower() in (name_l + ".exe", name_l + ".cmd", name_l + ".bat"):
                    return os.path.join(root, f)
    return None


def find_app(name):
    """Try multiple strategies to locate an executable/shortcut."""
    name = name.strip().lower()
    if not name:
        return None

    # 1. Direct in PATH
    for ext in ["", ".exe", ".cmd", ".bat", ".com"]:
        found = shutil.which(name + ext)
        if found:
            return found

    # 2. Start Menu shortcut (most reliable for GUI apps)
    lnk = _search_start_menu(name)
    if lnk:
        return lnk

    # 3. Program Files deep search
    exe = _search_program_files(name)
    if exe:
        return exe

    return None


def launch_app(path):
    """Launch an app given its full path."""
    try:
        if sys.platform == "win32":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen([path])
        return True
    except Exception as e:
        print(f"Launch error: {e}", flush=True)
        return False


class OpenAppSkill(BaseSkill):
    def matches(self, text):
        # "open X", "launch X", "start X", "run X"
        triggers = ("open ", "launch ", "start ", "run ")
        if text.startswith(triggers):
            return True
        # Also allow single-word site names like "youtube"
        words = text.strip().split()
        if len(words) <= 2:
            for site in WEBSITES:
                if site in text:
                    return True
        return False

    def handle(self, text):
        target = text
        for trigger in ("open the", "open", "launch", "start", "run"):
            if target.startswith(trigger):
                target = target[len(trigger):].strip()
                break
        target = target.strip()

        if not target:
            return "What should I open?"

        # 1. Known website? Open in browser
        for site_name, url in WEBSITES.items():
            if site_name == target or target in site_name:
                webbrowser.open(url)
                return f"Opening {site_name}."

        # 2. Local app? Find it dynamically
        path = find_app(target)
        if path:
            if launch_app(path):
                return f"Opening {target}."
            return f"I found {target} but couldn't launch it."

        # 3. Not found → tell user
        return (f"Sorry, {target} is not installed on this computer. "
                f"Want me to search the web for it?")