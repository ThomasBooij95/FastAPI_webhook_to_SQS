import os
import pytz
import datetime as dt


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
