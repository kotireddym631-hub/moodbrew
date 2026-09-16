from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='vibe_stars')
def vibe_stars(rating):
    """Renders a vibe rating as a row of star emojis."""
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return ''
    filled = min(rating, 10)
    empty = 10 - filled
    return '⭐' * filled + '☆' * empty


@register.filter(name='vibe_emoji')
def vibe_emoji(rating):
    """Returns a single representative emoji for the vibe score."""
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return '🧪'
    emojis = {1: '💀', 2: '😣', 3: '😶', 4: '😐', 5: '🙂',
              6: '😌', 7: '😊', 8: '🥰', 9: '🤩', 10: '✨'}
    return emojis.get(rating, '🧪')


@register.filter(name='chip_html')
def chip_html(ingredient):
    """Renders an emotion ingredient as a styled chip span."""
    return mark_safe(
        f'<span class="emotion-chip {ingredient.css_class}">'
        f'{ingredient.emoji} {ingredient.name}'
        f'</span>'
    )


@register.filter(name='percentage')
def percentage(value, maximum=10):
    """Convert a value to a percentage of a maximum."""
    try:
        return max(0, min(100, int(float(value) / float(maximum) * 100)))
    except (TypeError, ValueError, ZeroDivisionError):
        return 0
