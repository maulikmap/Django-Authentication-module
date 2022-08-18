from django.urls import path
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Authentication urlpatterns
    path("", LoginView.as_view(), name="login_view"),
    path("logout/", logout_view, name="logout_view"),
    path("register/", RegisterView.as_view(), name="register_view"),
    path("post_register/", RegisterView.as_view(), name="post_register"),

    # Dashboard urlpattern
    path("dashboard/", DashboardView.as_view(), name="dashboard_view"),

    # User management urlpatterns
    path("user_profile/", UserProfileView.as_view(), name="user_profile"),
    path("create/", CreateUserView.as_view(), name="create_view"),
    path("edit/<int:pk>", EditUserView.as_view(), name="edit_view"),
    path("delete/<int:pk>", DeleteUserView.as_view(), name="delete_view"),

    #Forgot password
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
    template_name = "registration/password_reset_form.html", 
    success_url = reverse_lazy("password_reset_complete")), 
    name="password_reset_confirm"),  # 3
    path('reset_password/',auth_views.PasswordResetView.as_view(
    template_name = "registration/password_reset.html", 
    success_url = reverse_lazy("password_reset_done"), email_template_name = 'registration/forgot_password_email.html'), 
    name="reset_password"),     # 1
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(
    template_name = "registration/password_reset_sent.html"), 
    name="password_reset_done"),    # 2
    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_done.html"), 
    name="password_reset_complete"),   # 4

    # Error handling urlpatterns
    path("error401/", error401_view, name="error401_view"),
    path("error_register/", error_register, name="error_register"),
]