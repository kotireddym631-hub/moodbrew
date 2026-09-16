import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application

if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        from potions.models import EmotionIngredient
        if EmotionIngredient.objects.count() == 0:
            call_command('seed_data')
    except Exception as e:
        print(f"Vercel init: {e}")
