# Buddy Voice Assistant

A background voice assistant that wakes on a wake word and responds to voice commands.

## Setup

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file
copy .env.example .env        # Windows
cp .env.example .env          # Linux/macOS

# 4. Run
python main.py
```

Say **"Hey Jarvis"** to wake it up.

## Customizing wake word

Edit `config.yaml`:
- `alexa`
- `hey_mycroft`
- `hey_jarvis`

## Adding a skill

1. Copy `skills/custom_skill.py`
2. Rename it and modify `matches()` + `handle()`
3. Add it to `assistant/router.py`

## Running in background

**Windows (Task Scheduler):**
```powershell
$action = New-ScheduledTaskAction -Execute "pythonw.exe" `
  -Argument "C:\path\to\buddy-assistant\main.py" `
  -WorkingDirectory "C:\path\to\buddy-assistant"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "BuddyAssistant" -Action $action -Trigger $trigger
```

**Linux (systemd user service):** see `deploy/linux/buddy.service`

**macOS (launchd):** see `deploy/macos/com.buddy.assistant.plist`