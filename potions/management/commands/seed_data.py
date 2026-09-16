from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from potions.models import EmotionIngredient, Potion


EMOTIONS = [
    # Positive Vibes
    ('Joy', '😄', '#FFD93D', 'chip-joy', 'POSITIVE'),
    ('Peace', '🕊️', '#95E1D3', 'chip-peace', 'POSITIVE'),
    ('Love', '❤️', '#FF6B6B', 'chip-love', 'POSITIVE'),
    ('Energy', '⚡', '#FF8C42', 'chip-energy', 'POSITIVE'),
    ('Hope', '🌱', '#34D399', 'chip-hope', 'POSITIVE'),
    ('Excitement', '🎉', '#F15BB5', 'chip-excitement', 'POSITIVE'),

    # Neutral / Mixed
    ('Curiosity', '🔍', '#38BDF8', 'chip-curiosity', 'NEUTRAL'),
    ('Nostalgia', '📷', '#A78BFA', 'chip-nostalgia', 'NEUTRAL'),

    # Heavy Feels
    ('Anxiety', '😰', '#C084FC', 'chip-anxiety', 'HEAVY'),
    ('Sadness', '🌧️', '#60A5FA', 'chip-sadness', 'HEAVY'),
    ('Anger', '🔥', '#EF4444', 'chip-anger', 'HEAVY'),
    ('Exhaustion', '😴', '#94A3B8', 'chip-exhaustion', 'HEAVY'),
]


class Command(BaseCommand):
    help = 'Seeds the database with emotion ingredients and sample potions.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding MoodBrew...'))

        # Seed emotion ingredients
        created_emotions = 0
        for name, emoji, color, css, cat in EMOTIONS:
            _, created = EmotionIngredient.objects.get_or_create(
                name=name,
                defaults={
                    'emoji': emoji,
                    'color_hex': color,
                    'css_class': css,
                    'category': cat,
                }
            )
            if created:
                created_emotions += 1

        self.stdout.write(f"  [OK] {created_emotions} emotion ingredients seeded")

        # Create a demo user
        demo_user, user_created = User.objects.get_or_create(
            username='alchemist',
            defaults={'email': 'alchemist@moodbrew.dev'}
        )
        if user_created:
            demo_user.set_password('brew1234')
            demo_user.save()
            self.stdout.write(f"  [OK] Demo user 'alchemist' created (password: brew1234)")


        # Seed sample potions
        sample_potions = [
            {
                'title': 'Sunday Morning Sunbeam',
                'vibe_rating': 9,
                'reflection': 'Woke up to golden light through the curtains. Made pour-over coffee, put on that playlist I love. The whole morning felt like a warm hug. Dogs were being silly in the park. This is the good stuff.',
                'ingredients': ['Joy', 'Peace', 'Energy'],
                'is_favorite': True,
            },
            {
                'title': '3am Overthinking Elixir',
                'vibe_rating': 3,
                'reflection': 'Brain decided sleep is optional tonight. Replayed that conversation from two weeks ago for the fifth time. Why did I say that? Also randomly remembered something embarrassing from 2019. Cool, cool, cool.',
                'ingredients': ['Anxiety', 'Exhaustion', 'Nostalgia'],
                'is_favorite': False,
            },
            {
                'title': 'Post-Workout Euphoria',
                'vibe_rating': 8,
                'reflection': 'Hit a new deadlift PR today! Legs are jelly but the endorphins are immaculate. Treated myself to that smoothie place after. Body tired, soul happy.',
                'ingredients': ['Energy', 'Joy', 'Excitement'],
                'is_favorite': True,
            },
            {
                'title': 'Rainy Day Cocoon',
                'vibe_rating': 6,
                'reflection': 'Cancelled plans because rain. Part of me feels guilty but mostly I needed this. Rewatching Howl\'s Moving Castle with chai. Cozy but a little lonely.',
                'ingredients': ['Peace', 'Sadness', 'Nostalgia'],
                'is_favorite': False,
            },
            {
                'title': 'First Day Jitters Tonic',
                'vibe_rating': 5,
                'reflection': 'Starting the new thing tomorrow. Excited but also kind of terrified? Prepared everything I could. Now just sitting with the butterflies. They\'re not all bad butterflies though.',
                'ingredients': ['Anxiety', 'Hope', 'Curiosity', 'Excitement'],
                'is_favorite': False,
            },
            {
                'title': 'Kitchen Disaster Recovery Potion',
                'vibe_rating': 4,
                'reflection': 'Tried to make that pasta recipe and it was a catastrophe. Burnt the garlic, overcooked the noodles, sauce was mid. Ordered pizza instead. Tomorrow we try again.',
                'ingredients': ['Anger', 'Exhaustion', 'Hope'],
                'is_favorite': False,
            },
            {
                'title': 'Old Song Portal Serum',
                'vibe_rating': 7,
                'reflection': 'That song from 2016 came on shuffle and suddenly I was back in my old room, fairy lights on, talking to friends until 2am about nothing important. Miss that version of life sometimes. But this one is good too.',
                'ingredients': ['Nostalgia', 'Love', 'Peace', 'Sadness'],
                'is_favorite': True,
            },
        ]

        created_potions = 0
        for data in sample_potions:
            if not Potion.objects.filter(title=data['title'], brewer=demo_user).exists():
                potion = Potion.objects.create(
                    brewer=demo_user,
                    title=data['title'],
                    vibe_rating=data['vibe_rating'],
                    reflection=data['reflection'],
                    is_favorite=data['is_favorite'],
                )
                emotions = EmotionIngredient.objects.filter(name__in=data['ingredients'])
                potion.ingredients.set(emotions)
                created_potions += 1

        self.stdout.write(self.style.SUCCESS(
            f"MoodBrew seeded! {EmotionIngredient.objects.count()} emotions, "
            f"{created_potions} potions, demo user: alchemist/brew1234"
        ))
