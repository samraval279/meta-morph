from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from requests import request
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.decorators import action
from meta_morph.global_resposne import ResponseInfo
from django.shortcuts import get_object_or_404, render
from account.serializer import *
from account.models import *
# Create your views here.

def myindex(request):
    return HttpResponse("Meta Morph server is running")

class UserViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','post','put','delete']

    action_serializers = {
        'login':LoginSerializer
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_authenticated_user(self):
        user = get_object_or_404(self.queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, user)
        return user

    def list(self, request):

        response = super(UserViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):

        response = super(UserViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):
        print(request)
        super(UserViewset, self).create(request)

        res = ResponseInfo({}, "User successfully added", True, 200)
        return Response(res.custom_success_payload())


    def update(self, request, pk):

        super(UserViewset, self).update(request, pk=pk)

        res = ResponseInfo({}, "User successfully updated", True, 200)
        return Response(res.custom_success_payload())



    def destroy(self, request, pk ):

        super(UserViewset).destroy(request,pk=pk)

        res = ResponseInfo({}, "User successfully deleted", True, 200)
        return Response(res.custom_success_payload())

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny,])
    def login(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):       
            res=ResponseInfo(serializer.data,'Logged In', True, 200)
            return Response(res.custom_success_payload())

    @action(methods=['get'], detail=False,permission_classes=[permissions.IsAuthenticated,])
    def get_user(self, request, pk=None):
        """
        get logged in user
        """
        serializer = self.get_serializer(self.get_authenticated_user())
        # prepare response
        res = ResponseInfo(serializer.data, "Sucess", True, 200)
        return Response(res.custom_success_payload())


class VideoViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    http_method_names = ['get','post','put','delete']

    action_serializers = {
        'create': VideoCreateSerializer,
        'update': VideoUpdateSerializer,
        'change_order': ChangeOrderSerializer
    }

    def get_permissions(self):
        if self.action == "create" or self.action == "update" or self.action == "destroy":
            self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]
        return super(VideoViewset, self).get_permissions()

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            qs = self.queryset.all()
        else:
            qs = self.queryset.filter(is_visible=True)
        return qs

    def list(self, request):
        response = super(VideoViewset, self).list(request)
        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
        

    def retrieve(self, request, pk):
      
        response = super(VideoViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = ResponseInfo({}, "Video successfully added", True, 200)
            return Response(res.custom_success_payload())

    def update(self, request, pk):

        # super(VideoViewset,self).update(request, pk=pk)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        res = ResponseInfo({}, "Video successfully updated", True, 200)
        return Response(res.custom_success_payload())

    def destroy(self, request, pk):

        super(VideoViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Video successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    
    
    @action(methods=['put'], detail=False,permission_classes=[permissions.IsAdminUser and permissions.IsAuthenticated])
    def change_order(self,request,pk=None):
        for rec in request.data['data']:
            print(rec['id'])
            instance = Video.objects.get(id=rec['id'])
            serializer = self.get_serializer(instance, data=rec, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        res = ResponseInfo({}, "order successfully updated", True, 200)
        return Response(res.custom_success_payload())



class PagesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = PageCommon.objects.all()
    serializer_class = PageSerializer
    http_method_names = ['get','post','put','delete']
    lookup_field = "key"

    action_serializers = {
        'list':PageGetSerializer,
        'retrieve':PageGetSerializer
    }

    def get_permissions(self):
        if self.action == "create" or self.action == "update" or self.action == "destroy":
            self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

        return super(PagesViewset, self).get_permissions()

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    # def get_queryset(self):
    #     qs = self.queryset.all()
    #     return qs

    def list(self, request):
        
        response = super(PagesViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def retrieve(self, request, key):

        response = super(PagesViewset, self).retrieve(request, key=key)
        
        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        super(PagesViewset,self).create(request)
  
        res = ResponseInfo({}, "page data successfully added", True, 200)
        return Response(res.custom_success_payload())

    def update(self, request, key):

        super(PagesViewset,self).update(request, key=key)

        res = ResponseInfo({}, "page data successfully updated", True, 200)
        return Response(res.custom_success_payload())

    def destroy(self, request, key):

        super(PagesViewset,self).destroy(request, key=key)

        res = ResponseInfo({}, "page data successfully deleted", True, 200)
        return Response(res.custom_success_payload())

class ContactViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ['get','post','delete']

    # action_serializers = {
    # 'create':ContactCreateSerializer
    # }

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action == "destroy":
            self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

        return super(ContactViewset, self).get_permissions()

    def list(self, request):
        
        response = super(ContactViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def retrieve(self, request, pk):

        response = super(ContactViewset, self).retrieve(request, pk=pk)
        
        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):
        super(ContactViewset, self).create(request)
        try:
            msg_html = render_to_string('email.html', {'name':request.data['name'],'email':request.data['email'],'message':request.data['message']})

            send_mail(
                subject=request.data['subject'],
                message=request.data['message'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL,request.data['email']],
                html_message=msg_html
            )
            res = ResponseInfo({}, "email sent", True, 200)
            return Response(res.custom_success_payload())

        except:
            res = ResponseInfo({}, "email failed to sent", False, 400)
            return Response(res.custom_success_payload())
        
    
    def destroy(self, request, pk):

        super(ContactViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "contact record successfully deleted", True, 200)
        return Response(res.custom_success_payload())


# class LinkViewset(viewsets.ModelViewSet):
#     permission_classes = [permissions.AllowAny]
#     parser_classes = [MultiPartParser, JSONParser, FormParser]
#     queryset = LinkManagement.objects.all()
#     serializer_class = LinkSerializer
#     http_method_names = ['get','post','put','delete']

#     action_serializers = {
#         'update':LinkUpdateSerializer
#     }

#     def get_permissions(self):
#         if self.action == "create" or self.action == "update" or self.action == "destroy":
#             self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

#         return super(LinkViewset, self).get_permissions()

#     def get_serializer_class(self):
#         return self.action_serializers.get(self.action, self.serializer_class)

#     def list(self, request):
        
#         response = super(LinkViewset, self).list(request)

#         res = ResponseInfo(response.data, "success", True, 200)
#         return Response(res.custom_success_payload())

#     def retrieve(self, request, pk):

#         response = super(LinkViewset, self).retrieve(request, pk=pk)

#         res = ResponseInfo(response.data, "success", True, 200)
#         return Response(res.custom_success_payload())

#     def create(self, request):

#         super(LinkViewset, self).create(request)

#         res = ResponseInfo({}, "success", True, 200)
#         return Response(res.custom_success_payload())

#     def update(self, request, pk):

#         super(LinkViewset, self).update(request,pk=pk)

#         res = ResponseInfo({}, "link successfully updated", True, 200)
#         return Response(res.custom_success_payload())
    

#     def destroy(self, request, pk):

#         super(LinkViewset,self).destroy(request, pk=pk)

#         res = ResponseInfo({}, "link successfully deleted", True, 200)
#         return Response(res.custom_success_payload())


# class Logoviewset(viewsets.ModelViewSet):
#     permission_classes = [permissions.AllowAny]
#     parser_classes = [MultiPartParser, JSONParser, FormParser]
#     queryset = Logo.objects.all()
#     serializer_class = LogoSerializer
#     http_method_names = ['get','put']
    
#     action_serializers = {
#         'update':LogoUpdateSerializer
#     }

#     def get_serializer_class(self):
#         return self.action_serializers.get(self.action, self.serializer_class)

#     def get_permissions(self):
#         if self.action == "create" or self.action == "update" or self.action == "destroy":
#             self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

#         return super(Logoviewset, self).get_permissions()


#     def list(self, request):
        
#         response = super(Logoviewset, self).list(request)

#         res = ResponseInfo(response.data, "success", True, 200)
#         return Response(res.custom_success_payload())

#     def retrieve(self, request, pk):

#         response = super(Logoviewset, self).retrieve(request, pk=pk)

#         res = ResponseInfo(response.data, "success", True, 200)
#         return Response(res.custom_success_payload())

#     # def create(self, request):

#     #     super(Logoviewset, self).create(request)

#     #     res = ResponseInfo({}, "success", True, 200)
#     #     return Response(res.custom_success_payload())

#     def update(self, request, pk):

#         super(Logoviewset, self).update(request,pk=pk)

#         res = ResponseInfo({}, "link successfully updated", True, 200)
#         return Response(res.custom_success_payload())
    

#     # def destroy(self, request, pk):

#     #     super(Logoviewset,self).destroy(request, pk=pk)

#     #     res = ResponseInfo({}, "link successfully deleted", True, 200)
#     #     return Response(res.custom_success_payload())

class LinkViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = LinkManagement.objects.all()
    serializer_class = LinkSerializer
    http_method_names = ['get','post','put','delete']

    action_serializers = {
        'create':LinkCreateSerializer,
        'update':LinkUpdateSerializer
    }

    def get_permissions(self):
        if self.action == "create" or self.action == "update" or self.action == "destroy":
            self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

        return super(LinkViewset, self).get_permissions()

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def list(self, request):
        
        response = super(LinkViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def retrieve(self, request, pk):

        response = super(LinkViewset, self).retrieve(request, pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        super(LinkViewset, self).create(request)

        res = ResponseInfo({}, "success", True, 200)
        return Response(res.custom_success_payload())

    def update(self, request, pk):

        super(LinkViewset, self).update(request,pk=pk)

        res = ResponseInfo({}, "link successfully updated", True, 200)
        return Response(res.custom_success_payload())
    

    def destroy(self, request, pk):

        super(LinkViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "link successfully deleted", True, 200)
        return Response(res.custom_success_payload())


class Logoviewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    http_method_names = ['get','post','put']
    
    action_serializers = {
        'update':LogoUpdateSerializer
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_permissions(self):
        if self.action == "create" or self.action == "update" or self.action == "destroy":
            self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

        return super(Logoviewset, self).get_permissions()


    def list(self, request):
        
        response = super(Logoviewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def retrieve(self, request, pk):

        response = super(Logoviewset, self).retrieve(request, pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        super(Logoviewset, self).create(request)

        res = ResponseInfo({}, "logo successfully created", True, 200)
        return Response(res.custom_success_payload())

    def update(self, request, pk):

        super(Logoviewset, self).update(request,pk=pk)

        res = ResponseInfo({}, "logo successfully updated", True, 200)
        return Response(res.custom_success_payload())
    

    def destroy(self, request, pk):

        super(Logoviewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "link successfully deleted", True, 200)
        return Response(res.custom_success_payload())

class LinkTypeViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    queryset = Linktype.objects.all()
    serializer_class = LinkTypeSerializer
    http_method_names = ['get','post','put','delete']

    def get_permissions(self):
        if self.action == "create" or self.action == "update" or self.action == "destroy":
            self.permission_classes = [permissions.IsAdminUser and permissions.IsAuthenticated]

        return super(LinkTypeViewset, self).get_permissions()

    def list(self, request):
        
        response = super(LinkTypeViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def retrieve(self, request, pk):

        response = super(LinkTypeViewset, self).retrieve(request, pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        super(LinkTypeViewset, self).create(request)

        res = ResponseInfo({}, "type successfully created", True, 200)
        return Response(res.custom_success_payload())

    def update(self, request, pk):

        super(LinkTypeViewset, self).update(request,pk=pk)

        res = ResponseInfo({}, "type successfully updated", True, 200)
        return Response(res.custom_success_payload())
    

    def destroy(self, request, pk):

        super(LinkTypeViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "type successfully deleted", True, 200)
        return Response(res.custom_success_payload())
