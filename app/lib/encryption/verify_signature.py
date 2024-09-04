import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv("app/.env")


def verify_signature(payload: bytes, signature: str | None) -> bool:
    """
    Verify the HMAC hex digest of the incoming payload against the provided signature.

    :param payload: The raw payload bytes from the request.
    :param signature: The signature from the request headers.
    :return: True if the signatures match, False otherwise.
    """
    SECRET_TOKEN = str(os.getenv("SECRET_HMAC_KEY"))

    # Compute the HMAC hex digest using the secret token and the payload
    computed_hash = hmac.new(
        SECRET_TOKEN.encode(), payload, hashlib.sha256  # noqa
    ).hexdigest()
    # The signature in the header is prefixed with 'sha256=', so we remove it
    expected_signature = f"sha256={computed_hash}"

    # Securely compare the computed hash with the signature
    return hmac.compare_digest(expected_signature, str(signature))
