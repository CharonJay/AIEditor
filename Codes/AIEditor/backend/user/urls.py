from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView)

from .views import (LoginView, RegisterView, GetFilesCreateByUserView,
                    CreateFilesView, DeleteFilesView, GetFilesTrashByUserView, UpdateFilesView,
                    GetDocumentView, UpdateDocumentView, DocumentTemplateViewSet, LogoutView, CustomTokenObtainPairView)

router = DefaultRouter()
router.register(r'template', DocumentTemplateViewSet)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='register'),
    path('filesMenu/create/<str:creator>/', GetFilesCreateByUserView.as_view(), name='files-by-creator'),
    path('filesMenu/trash/<str:creator>/', GetFilesTrashByUserView.as_view(), name='files-by-creator'),
    path('files/createfile/', CreateFilesView.as_view(), name='create-file'),
    path('files/updatefile/<int:pk>/', UpdateFilesView.as_view(), name='update-file'),
    path('files/deletefile/<int:id>/', DeleteFilesView.as_view(), name='delete-file'),
    path('document/get/<int:fid>/', GetDocumentView.as_view(), name='get-document'),
    path('document/update/<int:fid>/', UpdateDocumentView.as_view(), name='update-document'),
    path('', include(router.urls)),
    path('logout/<int:user_id>/', LogoutView.as_view(), name='logout'),
]
