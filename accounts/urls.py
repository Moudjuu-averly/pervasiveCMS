from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns = [
    re_path(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'registration/index.html'}, name='login'),
    re_path(r'^$', views.logout, {'template_name': 'pervasive/index.html'}, name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile'),
    re_path(r'^edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'^update/$', views.edit_view, name='edit_view'),
    re_path(r'^edit/display/$', views.edit_display, name='edit_display'),
    re_path(r'^edit/contacts/$', views.edit_contacts, name='edit_contacts'),
    re_path(r'^edit/media/$', views.edit_media, name='edit_media'),
    re_path(r'^edit/profile_image/$', views.edit_profile_image, name='edit_profile_image'),
    re_path(r'^edit/profile_cover/$', views.edit_cover_image, name='edit_cover_image'),
    re_path(r'^change-password/$', views.change_password, name='change_password'),
    re_path(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name=
        'registration/reset_password.html' ), {'post_reset_redirect':
            'accounts:password_reset_done', 'email_template_name':
                'registration/reset_password_email.html'}, name='reset_password'),
    re_path(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name=
        'registration/password_reset_done.html'), {},
        name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(), {'post_reset_redirect': 'registration/password_reset_complete'},
        name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
