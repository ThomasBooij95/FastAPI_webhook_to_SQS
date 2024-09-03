import os
import pytz
import datetime as dt
import hmac
import hashlib


def UNIX_timestamp_to_datetime(
    unix_timestamp: float, time_zone: str = "UTC"
) -> dt.datetime:
    """
    Convert a Unix timestamp to a Python datetime object with UTC timezone.

    Args:
        unix_timestamp (float): The Unix timestamp to convert.

    Returns:
        datetime.datetime or None: The converted datetime object with UTC timezone,
                                   or None if the conversion fails.
    """
    try:
        original_timezone = pytz.timezone(time_zone)
        datetime_from_stamp = dt.datetime.fromtimestamp(
            unix_timestamp, tz=original_timezone
        )
        datetime_utc = datetime_from_stamp.astimezone(pytz.utc)
        return datetime_utc

    except (ValueError, TypeError):
        # print(f"Invalid timestamp ({e}), returning None")
        return None  # type: ignore


def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Verify the HMAC hex digest of the incoming payload against the provided signature.

    :param payload: The raw payload bytes from the request.
    :param signature: The signature from the request headers.
    :return: True if the signatures match, False otherwise.
    """
    SECRET_TOKEN = os.environ("SECRET_HMAC_KEY")
    # Compute the HMAC hex digest using the secret token and the payload
    computed_hash = hmac.new(SECRET_TOKEN.encode(), payload, hashlib.sha256).hexdigest()
    # The signature in the header is prefixed with 'sha256=', so we remove it
    expected_signature = f"sha256={computed_hash}"

    # Securely compare the computed hash with the signature
    return hmac.compare_digest(expected_signature, signature)


if __name__ == "__main__":
    # Example JSON payload as a byte string
    payload = b'"Hello World!"'
    SECRET_TOKEN = os.getenv("SECRET_HMAC_KEY")

    # Simulated correct signature (for demonstration purposes, normally this would come from the request headers)
    computed_hash = hmac.new(SECRET_TOKEN.encode(), payload, hashlib.sha256).hexdigest()
    # signature = f"sha256={computed_hash}"
    signature = (
        f"sha256=a6353e505082e0614d4f1760c1d25e523ee34141bd2d2e5ef1e4648fc1ed128b"
    )

    # Now, use the verify_signature function to check the signature
    is_valid = verify_signature(payload, signature)
    print("Is the signature valid?", is_valid)
