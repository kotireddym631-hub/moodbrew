from django.contrib import admin
from .models import EmotionIngredient, Potion


@admin.register(EmotionIngredient)
class EmotionIngredientAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'name', 'category', 'color_hex', 'css_class')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Potion)
class PotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'brewer', 'vibe_rating', 'is_favorite', 'ingredient_count', 'brewed_at')
    list_filter = ('vibe_rating', 'is_favorite', 'brewed_at')
    search_fields = ('title', 'reflection', 'brewer__username')
    filter_horizontal = ('ingredients',)
    readonly_fields = ('brewed_at', 'updated_at')
