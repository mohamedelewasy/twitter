from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .views import (
    login_view,
    password_change_view,
    profile_view,
)
app_name = 'account'
urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),

    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('<username>/', profile_view, name='profile'),

    path('password/change/', password_change_view, name='password_change'),
    path('password/change/done/', TemplateView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', success_url=reverse_lazy('profile:password_reset_done'), subject_template_name='registration/subject_template_name.txt'), name='password_reset'),        
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
