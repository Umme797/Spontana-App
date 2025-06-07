from django.urls import path
from Spontana_App import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('home', views.home),

    path('activity/<int:aid>/', views.activity_detail, name='activity_detail'),

    path('activity_journal/', views.activity_journal),

    path('add_journal/', views.add_journal),
    
    path('activity_journal/add_journal/', views.add_journal),

    path('login', views.login_view),

    path('logout', views.logout_view),

    path('register', views.full_register, name='full_register'),

    path('user_profile', views.user_profile),

    path('verify-email/<str:email>/', views.verify_email, name='verify-email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
