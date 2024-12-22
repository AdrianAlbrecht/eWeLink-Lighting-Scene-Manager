from django.urls import path
from . import views

urlpatterns = [
    # AUTHORIZE PART
    path('<int:pk>/authorize_app/', views.authorize_app),
    path('<int:pk>/use_code/', views.use_code),
    path('<int:pk>/refresh_tokens/', views.refresh_tokens),
    # GET DEVICE LIST & SIMPLE STATUS
    path('<int:pk>/device/', views.get_device_list),
    path('<int:pk>/device/<str:name>/', views.get_device_status),
    # Scene list, details & create
    path('<int:pk>/scene/', views.get_scene_list),
    path('<int:pk>/scene/<str:name>/', views.get_scene_details),
    path('<int:pk>/scene_create/', views.create_scene),
    path('<int:pk>/scene_create_by_form/', views.create_scene_form),
    # Edit Scene
    path('<int:pk>/scene/<str:name>/edit/', views.edit_scene_form),
    # Lunch Scene
    path('<int:pk>/scene/<str:name>/activate', views.scene_activate),
]