from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import CustomerLoginForm, CustomerPasswordChangeForm, CustomerPasswordResetForm, CustomerSetPasswordForm

urlpatterns = [

    path('set/', views.setsession, name='set'),
    path('get/', views.getsession, name='get'),
    path('del/', views.deletesession, name='del'),

    # path('', views.home),

    path('mobile/<slug:data>', views.mobile, name='mobile-data'),
    path('mobile/', views.mobile, name='mobile'),

    path('laptop/<slug:data>', views.laptop, name='laptop-data'),
    path('laptop/', views.laptop, name='laptop'),

    path('', views.ProductView.as_view(), name="home"),

    # path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    # path('registration/', views.customer-registration, name='customer-registration'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),

    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # path('address/', views.address, name='profile'),
    path('address/', views.AddressView.as_view(), name='address'),

    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.ShowCartView.as_view(), name='show-cart'),
    path('plus-cart/', views.PlusCart.as_view(), name='plus-cart'),
    path('minus-cart/', views.MinusCart.as_view(), name='minus-cart'),
    path('remove-cart/', views.RemoveCart.as_view(), name='remove-cart'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment-done/', views.PaymentDoneView.as_view(), name='payment-done'),

    path('orders/', views.OrderPlacedView.as_view(), name='orders'),
    path('buy/', views.buy_now, name='buy-now'),

    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='app/login.html', authentication_form=CustomerLoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='app/change_password.html',
        form_class=CustomerPasswordChangeForm,
        success_url='/change-password/done/'),
         name='change-password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/change_password_done.html'),
         name='change-password-done'),

    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='app/reset_password.html',
        form_class=CustomerPasswordResetForm),
         name='reset-password'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/reset_password_done.html'),
         name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/reset_password_confirm.html',
        form_class=CustomerSetPasswordForm),
         name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/reset_password_complete.html'),
         name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
