from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Core App
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('potions/', views.PotionListView.as_view(), name='potion_list'),
    path('potions/<int:pk>/', views.PotionDetailView.as_view(), name='potion_detail'),
    path('potions/brew/', views.PotionCreateView.as_view(), name='potion_create'),
    path('potions/<int:pk>/edit/', views.PotionUpdateView.as_view(), name='potion_update'),
    path('potions/<int:pk>/delete/', views.PotionDeleteView.as_view(), name='potion_delete'),
    path('potions/<int:pk>/fav/', views.toggle_favorite, name='toggle_favorite'),
]
