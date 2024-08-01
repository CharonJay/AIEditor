from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView)

from backend import settings
from .views import (CustomUserViewSet, GetFilesCreateByUserView,
                    CreateFilesView, DeleteFilesView, GetFilesTrashByUserView, UpdateFilesView,
                    GetDocumentView, UpdateDocumentView, DocumentTemplateViewSet, LogoutView, CustomTokenObtainPairView,
                    )
from .views import upload_avatar, get_avatar
router = DefaultRouter()
router.register(r'template', DocumentTemplateViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('filesMenu/create/<str:creator>/', GetFilesCreateByUserView.as_view(), name='files-by-creator'),
    path('filesMenu/trash/<str:creator>/', GetFilesTrashByUserView.as_view(), name='files-by-creator'),
    path('files/createfile/', CreateFilesView.as_view(), name='create-file'),
    path('files/updatefile/<int:pk>/', UpdateFilesView.as_view(), name='update-file'),
    path('files/deletefile/<int:id>/', DeleteFilesView.as_view(), name='delete-file'),
    path('document/get/<int:fid>/', GetDocumentView.as_view(), name='get-document'),
    path('document/update/<int:fid>/', UpdateDocumentView.as_view(), name='update-document'),
    path('', include(router.urls)),
    path('logout/<int:user_id>/', LogoutView.as_view(), name='logout'),
    path('upload_avatar/', upload_avatar, name='upload-avatar'),
    re_path(r'^media/avatars/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
