from .imports import *


# -------------------------
# CORE (single source of truth)
# -------------------------
def now() -> datetime:
    return datetime.now(timezone.utc)


def add_delta(
    dt: datetime = None,
    *,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    milliseconds=0
) -> datetime:
    dt = dt or now()

    return dt + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds
    )


# -------------------------
# TIMESTAMP ADAPTERS
# -------------------------
def to_timestamp(dt: datetime = None) -> float:
    dt = dt or now()
    return dt.timestamp()


def from_timestamp(ts: float) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


# -------------------------
# STRING ADAPTERS
# -------------------------
def to_iso(dt: datetime = None) -> str:
    return (dt or now()).isoformat()


def from_string(date_str: str, fmt: str) -> datetime:
    return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)

def get_sleep(seconds: float = 0.0):
    try:
        seconds = float(seconds)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid sleep value: {seconds}")

    if seconds <= 0:
        return

    time.sleep(seconds)
