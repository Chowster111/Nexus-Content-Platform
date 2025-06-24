import subprocess

def test_lint():
    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode == 0, "Ruff linting failed"
