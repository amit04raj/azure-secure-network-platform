from app.main import app


def test_application_metadata():
    assert app.title == "Azure Secure Network Platform"
    assert app.version == "1.0.0"
    assert "cloud security" in app.description.lower()
