from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register-trades/', views.register_trade, name='register_trade'),
    path('trades/', views.list_trades, name='trades'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('help/', views.help, name='help'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url= 'index'), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('delete-trade/<int:trade_id>/', views.delete_trade, name='delete_trade'),
    path('trades/<int:trade_id>/', views.trade_detail, name='trade_detail'),
    path('trade/<int:trade_id>/delete/', views.delete_trade, name='delete_trade'),
    path('trade/<int:trade_id>/close/', views.close_trade, name='close_trade')
]