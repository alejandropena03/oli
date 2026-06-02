from scripts.configure_openrouter_key import sanitize_api_key


def test_sanitize_api_key_strips_bearer_prefix():
    assert sanitize_api_key("Bearer sk-or-test") == "sk-or-test"
    assert sanitize_api_key("Authorization: Bearer sk-or-test") == "sk-or-test"
    assert sanitize_api_key('"sk-or-test"') == "sk-or-test"

