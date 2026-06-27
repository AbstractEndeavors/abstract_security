import getpass, bcrypt, secrets, string
from datetime import datetime, timezone, timedelta


def add_delta(dt: datetime = None, *, days=0, hours=0, minutes=0, seconds=0, milliseconds=0) -> datetime:
    """Return `dt` (default: now, in UTC) offset by the given delta."""
    dt = dt or datetime.now(timezone.utc)
    return dt + timedelta(days=days, hours=hours, minutes=minutes,
                          seconds=seconds, milliseconds=milliseconds)
