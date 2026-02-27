import secrets
import string


def generate_share_code(length=10):
    """Generate a random alphanumeric share code."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
