import json
from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def normalize_registration_number(value):
    """Normalize user input without broadening the accepted number set."""
    return str(value).strip().upper()


def _collect_list_values(node):
    values = []
    if isinstance(node, list):
        values.extend(node)
    elif isinstance(node, dict):
        for child in node.values():
            values.extend(_collect_list_values(child))
    return values


@lru_cache(maxsize=1)
def get_valid_registration_numbers():
    path = settings.REGISTRATION_NUMBERS_FILE
    try:
        with path.open(encoding="utf-8") as source:
            data = json.load(source)
    except (OSError, json.JSONDecodeError) as exc:
        raise ImproperlyConfigured(
            f"Unable to load registration numbers from {path}"
        ) from exc

    return frozenset(
        normalize_registration_number(value)
        for value in _collect_list_values(data)
        if str(value).strip()
    )


def is_valid_registration_number(value):
    return normalize_registration_number(value) in get_valid_registration_numbers()
