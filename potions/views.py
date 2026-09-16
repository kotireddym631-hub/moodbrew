from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Q
from .models import Potion, EmotionIngredient
from .forms import PotionBrewForm, BrewerRegistrationForm


class RegisterView(CreateView):
    """Sign up page for new alchemists to join the lab."""
    form_class = BrewerRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"Welcome to the lab, {self.object.username}! 🧪 Start brewing your first potion.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Join the Lab'
        return ctx


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Personal alchemy dashboard — shows brewing stats, recent potions,
    most-used emotions, and overall vibe average.
    """
    template_name = 'potions/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_potions = Potion.objects.filter(brewer=self.request.user).prefetch_related('ingredients')

        total_brews = user_potions.count()
        favorites = user_potions.filter(is_favorite=True).count()
        avg_vibe = user_potions.aggregate(avg=Avg('vibe_rating'))['avg'] or 0
        avg_vibe = round(avg_vibe, 1)

        # Top emotions used across all this user's potions
        top_emotions = (
            EmotionIngredient.objects
            .filter(used_in_potions__brewer=self.request.user)
            .annotate(usage=Count('used_in_potions'))
            .order_by('-usage')[:6]
        )

        # Vibe distribution buckets
        rough = user_potions.filter(vibe_rating__lte=2).count()
        meh = user_potions.filter(vibe_rating__gte=3, vibe_rating__lte=4).count()
        okay = user_potions.filter(vibe_rating__gte=5, vibe_rating__lte=6).count()
        good = user_potions.filter(vibe_rating__gte=7, vibe_rating__lte=8).count()
        magical = user_potions.filter(vibe_rating__gte=9).count()

        vibe_dist = [
            ('Rough 💀', rough, int(rough / total_brews * 100) if total_brews else 0),
            ('Meh 😶', meh, int(meh / total_brews * 100) if total_brews else 0),
            ('Okay 🙂', okay, int(okay / total_brews * 100) if total_brews else 0),
            ('Good 😊', good, int(good / total_brews * 100) if total_brews else 0),
            ('Magical ✨', magical, int(magical / total_brews * 100) if total_brews else 0),
        ]

        ctx.update({
            'total_brews': total_brews,
            'favorites': favorites,
            'avg_vibe': avg_vibe,
            'top_emotions': top_emotions,
            'recent_potions': user_potions[:5],
            'vibe_dist': vibe_dist,
        })
        return ctx


class PotionListView(LoginRequiredMixin, ListView):
    """Browse and search all personal potions with filtering."""
    model = Potion
    template_name = 'potions/potion_list.html'
    context_object_name = 'potions'
    paginate_by = 9

    def get_queryset(self):
        qs = Potion.objects.filter(
            brewer=self.request.user
        ).prefetch_related('ingredients')

        q = self.request.GET.get('q', '').strip()
        vibe_min = self.request.GET.get('vibe_min', '').strip()
        fav_only = self.request.GET.get('fav', '').strip()
        emotion = self.request.GET.get('emotion', '').strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(reflection__icontains=q)
            )
        if vibe_min and vibe_min.isdigit():
            qs = qs.filter(vibe_rating__gte=int(vibe_min))
        if fav_only == '1':
            qs = qs.filter(is_favorite=True)
        if emotion:
            qs = qs.filter(ingredients__name__iexact=emotion).distinct()

        return qs.order_by('-brewed_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['emotions_list'] = EmotionIngredient.objects.all()
        ctx['current_q'] = self.request.GET.get('q', '')
        ctx['current_vibe_min'] = self.request.GET.get('vibe_min', '')
        ctx['current_fav'] = self.request.GET.get('fav', '')
        ctx['current_emotion'] = self.request.GET.get('emotion', '')
        return ctx


class PotionDetailView(LoginRequiredMixin, DetailView):
    """Deep dive into a single potion — ingredients, vibe, reflection."""
    model = Potion
    template_name = 'potions/potion_detail.html'
    context_object_name = 'potion'

    def get_queryset(self):
        return Potion.objects.filter(
            brewer=self.request.user
        ).prefetch_related('ingredients')


class PotionCreateView(LoginRequiredMixin, CreateView):
    """Brew a new emotional potion."""
    model = Potion
    form_class = PotionBrewForm
    template_name = 'potions/potion_form.html'

    def form_valid(self, form):
        form.instance.brewer = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"🧪 \"{self.object.title}\" brewed successfully! Vibe: {self.object.vibe_label}")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = '🧪 Brew New Potion'
        ctx['submit_label'] = 'Brew It!'
        ctx['emotions_grouped'] = self._group_emotions()
        return ctx

    def _group_emotions(self):
        grouped = {}
        for em in EmotionIngredient.objects.all():
            grouped.setdefault(em.get_category_display(), []).append(em)
        return grouped


class PotionUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing potion's recipe."""
    model = Potion
    form_class = PotionBrewForm
    template_name = 'potions/potion_form.html'

    def get_queryset(self):
        return Potion.objects.filter(brewer=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"✏️ \"{self.object.title}\" updated!")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'✏️ Edit: {self.object.title}'
        ctx['submit_label'] = 'Save Changes'
        ctx['emotions_grouped'] = self._group_emotions()
        return ctx

    def _group_emotions(self):
        grouped = {}
        for em in EmotionIngredient.objects.all():
            grouped.setdefault(em.get_category_display(), []).append(em)
        return grouped


class PotionDeleteView(LoginRequiredMixin, DeleteView):
    """Confirm and discard a potion."""
    model = Potion
    template_name = 'potions/potion_confirm_delete.html'
    context_object_name = 'potion'
    success_url = reverse_lazy('potion_list')

    def get_queryset(self):
        return Potion.objects.filter(brewer=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.warning(request, f"🗑️ \"{obj.title}\" has been discarded.")
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_favorite(request, pk):
    """Quick toggle a potion's favorite status."""
    potion = get_object_or_404(Potion, pk=pk, brewer=request.user)
    potion.is_favorite = not potion.is_favorite
    potion.save(update_fields=['is_favorite'])
    icon = '⭐' if potion.is_favorite else '☆'
    messages.info(request, f"{icon} \"{potion.title}\" {'bookmarked!' if potion.is_favorite else 'unbookmarked.'}")
    next_url = request.GET.get('next') or potion.get_absolute_url()
    return redirect(next_url)
