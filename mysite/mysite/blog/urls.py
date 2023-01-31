from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('list/', views.post_list, name="list"),
    path('write/', views.post_write, name="write"),
    path('view/<int:pk>', views.post_view, name="view"),
    path("modify/<int:pk>", views.post_modify, name="modify"),
    path("update/", views.post_update, name="update"),
    path("remove/<int:pk>", views.post_remove, name="remove"),
]