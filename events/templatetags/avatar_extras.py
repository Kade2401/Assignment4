from django import template
import hashlib

register = template.Library()

@register.filter
def avatar_hue(value: str) -> int:
    """
    Стабильный оттенок (0..359) на основе строки (username).
    """
    if not value:
        return 210
    digest = hashlib.md5(value.encode("utf-8")).hexdigest()
    return int(digest[:2], 16) * 360 // 256
