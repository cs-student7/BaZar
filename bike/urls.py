from django.urls import path
from . import views

app_name = 'bike'

urlpatterns = [
    path('', views.bike_list, name='bike_list'),
    # path('', views.background, name='background'),  ← DELETE THIS LINE
    path('learn-more/', views.learn_more, name='learn_more'),
    path('details/<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('test-ride/', views.test_ride, name='test_ride'),
    path('add-to-cart/<int:bike_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('design/', views.design_bike, name='design_bike'),
    path('save-design/', views.save_design, name='save_design'),
    path('designs/', views.design_list, name='design_list'),
    path('design/<int:design_id>/', views.get_design, name='get_design'),
    path('design/<int:design_id>/update/', views.update_design, name='update_design'),
    path('design/<int:design_id>/delete/', views.delete_design, name='delete_design'),
]