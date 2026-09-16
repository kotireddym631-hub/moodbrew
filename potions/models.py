from django.db import models
from django.conf import settings
from django.urls import reverse


class EmotionIngredient(models.Model):
    """
    A predefined emotional ingredient used to brew mood potions.
    Each represents a core feeling with its own visual identity.
    """
    name = models.CharField(max_length=60, unique=True)
    emoji = models.CharField(max_length=10, default='✨')
    color_hex = models.CharField(max_length=7, default='#FFD93D', help_text='Display color for UI chips')
    css_class = models.CharField(max_length=40, default='chip-joy', help_text='CSS class name for styling')

    class Category(models.TextChoices):
        POSITIVE = 'POSITIVE', 'Positive Vibes'
        NEUTRAL = 'NEUTRAL', 'Neutral / Mixed'
        HEAVY = 'HEAVY', 'Heavy Feels'

    category = models.CharField(max_length=10, choices=Category.choices, default=Category.POSITIVE)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Potion(models.Model):
    """
    An emotional potion brewed from a combination of mood ingredients.
    Each potion is a personal journal entry capturing a moment's emotional recipe.
    """
    brewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='potions',
        help_text='The alchemist who brewed this potion'
    )
    title = models.CharField(
        max_length=150,
        help_text='Give your potion a creative name'
    )
    ingredients = models.ManyToManyField(
        EmotionIngredient,
        related_name='used_in_potions',
        help_text='Select the emotions that went into this brew'
    )
    vibe_rating = models.PositiveSmallIntegerField(
        default=5,
        help_text='Overall vibe from 1 (rough day) to 10 (absolutely magical)'
    )
    reflection = models.TextField(
        blank=True,
        help_text='Write about why you feel this way, what happened, or what you need'
    )
    is_favorite = models.BooleanField(
        default=False,
        help_text='Bookmark this as a favorite brew'
    )
    brewed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-brewed_at']

    def __str__(self):
        return f"🧪 {self.title} (vibe: {self.vibe_rating}/10)"

    def get_absolute_url(self):
        return reverse('potion_detail', kwargs={'pk': self.pk})

    @property
    def vibe_label(self):
        """Human-friendly label for the vibe score."""
        labels = {
            range(1, 3): '💀 Rough',
            range(3, 5): '😶 Meh',
            range(5, 7): '🙂 Okay',
            range(7, 9): '😊 Good',
            range(9, 11): '✨ Magical',
        }
        for rng, label in labels.items():
            if self.vibe_rating in rng:
                return label
        return '🧪 Unknown'

    @property
    def vibe_percentage(self):
        """Vibe as a 0-100 percentage for progress bars."""
        return max(0, min(100, self.vibe_rating * 10))

    @property
    def ingredient_count(self):
        return self.ingredients.count()
