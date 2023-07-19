from django.urls import path, include
from rest_framework import routers
from account.views import *

router = routers.DefaultRouter()
router.register(r'user', UserViewset)
router.register(r'video', VideoViewset)
router.register(r'page', PagesViewset)
router.register(r'contact', ContactViewset)
router.register(r'link', LinkViewset)
router.register(r'logo', Logoviewset)
router.register(r'linktype', LinkTypeViewset)

urlpatterns = [
    path('', include(router.urls)),
    # path('<page>', PagesViewset.as_view({'get':'list'}))
]