"""meta_morph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from django.conf.urls import url
from drf_yasg import openapi
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account.views import myindex

admin.site.index_title = _('Meta Morph')
admin.site.site_header = _('Meta Morph')
admin.site.site_title = _('Meta Morph')

schema_view = get_swagger_view(title="Meta Morph API")

redoc_schema_view = get_schema_view(
   openapi.Info(
      title="Meta Morph APIs",
      default_version='v1',
      description="Meta Morph",
      terms_of_service="#",
   ),
   public=True,
#  permission_classes=(permissions.IsAuthenticated,),
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = i18n_patterns(
    url(r'^docs/$', redoc_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', redoc_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('jet/',include('jet.urls')),
    path('admin/', admin.site.urls),
    path('api/',include('account.urls')),
    path('', myindex, name='index'),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)