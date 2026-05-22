from ai_commit.redact import redact


def test_redacts_openai_key():
    s = "sk-1234567890abcdefghijklmnopqrstuvwxyz1234"
    assert "sk-1234" not in redact(s)


def test_redacts_github_token():
    s = "token: ghp_abcdefghijklmnopqrstuvwxyz0123456789"
    assert "ghp_" not in redact(s)


def test_redacts_password_field():
    s = 'password: "supersecret123"'
    assert "supersecret123" not in redact(s)


def test_redacts_aws():
    s = "AWS_ACCESS=AKIAIOSFODNN7EXAMPLE"
    assert "AKIA" not in redact(s)


def test_keeps_normal_code():
    s = "def add(a, b):\n    return a + b"
    assert redact(s) == s
