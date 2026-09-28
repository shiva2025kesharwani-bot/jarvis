import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assistant.router import CommandRouter

def test_time():
    router = CommandRouter({"llm": {"enabled": False}})
    out = router.handle("what time is it")
    assert "time" in out.lower()

def test_date():
    router = CommandRouter({"llm": {"enabled": False}})
    out = router.handle("what is today's date")
    assert "today" in out.lower() or "day" in out.lower()

if __name__ == "__main__":
    test_time()
    test_date()
    print("All tests passed.")