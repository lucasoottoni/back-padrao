from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .myrouter import MyCustomRouter
from .views import ChangePasswordView, CustomSignupView, LoginView, UserViewSet

routerAccount = SimpleRouter()
routerAccount.register('users',UserViewSet)
router = MyCustomRouter()
router.register('users', CustomSignupView)

urlpatterns = [

    #Token routes
    path('account/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('account/changepassword/', ChangePasswordView.as_view(), name='token_obtain_pair'),
    #path('account/djoser/',include('djoser.urls') ),
    #path('djosersssss/', CustomSignupView.as_view({'post': 'create'})),


    #Token routes - END   
]