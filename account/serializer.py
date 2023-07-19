from django.db.models import Max
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from account.models import Contact, Logo, PageCommon, LinkManagement, User, Video, Linktype
from django.db import transaction

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255 ,write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    usertype = serializers.CharField(max_length=255,read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user and not user.is_active:
            raise serializers.ValidationError(
                "Account has been deactivated. \n Please contact your company's admin to restore your account.")

        if not user:
            raise serializers.ValidationError(
                    'Email or Password is wrong.'
                )

        refresh = RefreshToken.for_user(user)
        data = {
            "usertype":str(user.usertype),
            "access": str(refresh.access_token),
            "refresh": str(refresh)
            }

        return data

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id","email","password","usertype","first_name","last_name","phone_number"]


class VideoSerializer(serializers.ModelSerializer):

    video = serializers.CharField()

    class Meta:
        model = Video
        fields = ["id","title","subtitle","video","videoname","order","upload_by","is_visible"]

class VideoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ["id","title","subtitle","video","videoname","order","upload_by","is_visible"]
        read_only_fields = ["id","upload_by","videoname","order"]

    def create(self, validated_data):
        print(validated_data)
        instance = self.Meta.model(**validated_data)
        instance.upload_by = self.context['request'].user
        count = Video.objects.aggregate(Max('order'))['order__max']
        if count == None:
            count = '0' 
        instance.order = int(count) + 1
        # instance.order = int(Video.objects.aggregate(Max('order'))['order__max']) + 1
        instance.save()
        return instance
    
class VideoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ["id","title","subtitle","video","videoname","order","upload_by","is_visible"]

    def update(self, instance, validated_data):
        # print(validated_data)
        if 'is_visible' in validated_data and validated_data['is_visible'] == False:
                validated_data['order'] = int(Video.objects.aggregate(Max('order'))['order__max']) + 1 
        return super(VideoUpdateSerializer,self).update(instance, validated_data)

class PageGetSerializer(serializers.ModelSerializer):

    # content = QuillHtmlField()
    image = serializers.CharField()
    link = serializers.SerializerMethodField('links')

    class Meta:
        model = PageCommon
        fields = ['id','key','content','image','title','subtitle','link']

    def links(self, obj):
        links = LinkManagement.objects.filter(page=obj)
        # links = links.filter(page=obj)
        data = []
        for item in links:
            type = Linktype.objects.get(name=item.type)
            data.append(
                {
                    "id":item.id,
                    "image":str(item.image),
                    "type":type.name,
                    "type_id":type.id,
                    "link_title":type.title,
                    "link":item.link
                }
            )
        return data
class PageSerializer(serializers.ModelSerializer):

    # content = QuillHtmlField()
    # image = serializers.CharField()
    # link = serializers.SerializerMethodField('links')

    class Meta:
        model = PageCommon
        fields = ['id','key','content','image','title','subtitle']

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message'] 


class LinkSerializer(serializers.ModelSerializer):

    image = serializers.CharField()

    class Meta:
        model = LinkManagement
        fields = ['id','image','type','key','link','page']

class LinkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkManagement
        fields = ['id','image','type','key','link','page']

class LinkUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkManagement
        fields = ['id','image','type','key','link','page']
    
class LogoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Logo
        fields = ['id','title','description']

class LogoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Logo
        fields = ['id','title','description']

class LinkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Linktype
        fields = ['id','title','name'] 

class ChangeOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['id','order','is_visible']
        read_only_fields = ['id'] 
    
    def update(self, instance, validated_data):
        # print(validated_data)
        return super(ChangeOrderSerializer,self).update(instance, validated_data)