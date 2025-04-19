from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('reservation/', views.book_table, name='reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('modify-reservation/<int:reservation_id>/', views.modify_reservation, name='modify_reservation'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('online-order/', views.online_order, name='online_order'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('cart-preview/', views.cart_preview, name='cart_preview'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order-history/', views.order_history, name='order_history'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('toggle-favorite/<int:order_id>/', views.toggle_favorite_order, name='toggle_favorite'),
    path('reorder/<int:order_id>/', views.reorder, name='reorder'),
    path('api/order-status/<int:order_id>/', views.order_status_api, name='order_status_api'),
]
