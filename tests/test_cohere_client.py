import pytest
from kindgen import cohere_client


def test_api_key():
    """Test if Cohere API Key is working by making an actual request"""
    try:
        response = cohere_client.generate(prompt="sample prompt", max_tokens=3)
        assert response is not None
    except Exception as e:
        pytest.fail(f"API Key test failed: {e}")
