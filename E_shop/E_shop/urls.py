
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product', views.product, name = 'product'),
    path('search', views.search, name = 'search'),
    path('single-product/<str:id>', views.single_product, name = 'single_product'),
    path('', views.index, name = 'index'),
    path('base/', views.base, name = 'base'),
    path('registration', views.register, name = 'register'),
    path('login', views.auth_login, name = 'login'),
    path('logout', views.auth_logout, name = 'logout'),
    path('contact', views.contact, name='contact'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/checkout', views.checkout, name = 'checkout'),
    path('cart/place_order/', views.placeorder, name = 'placeholder'),
    path('cart/thankyou/', views.thankyou, name='thankyou'),
    path('aboutus/', views.aboutus, name='about'),
    path('your_order/', views.order, name='your_order'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
