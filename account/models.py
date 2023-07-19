import os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField

from meta_morph.storage_backend import MediaStorage

def upload_image_to(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    # filename = "%s.%s" % (instance.id, filename_ext)
    return 'images/%s' % (
        filename
    )

def upload_video_to(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    # filename = "%s.%s" % (instance.id, filename_ext)
    return 'videos/%s' % (
        filename
    )

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

ROLE_CHOICE  = [
    ('admin','admin'),
    # ('staff user','staff user')
    ('user','user')
]

class User(AbstractUser):
    id = models.AutoField(primary_key=True, )
    username = None
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    password = models.CharField(verbose_name=_('password'),max_length=256)
    first_name = models.CharField(max_length=40, 
                                validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only characters are allowed.')], 
                                help_text='Enter name', blank=True, null=True,verbose_name=_("first name"))
    last_name = models.CharField(max_length=40, 
                                validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only characters are allowed.')], 
                                help_text='Enter name', blank=True, null=True, verbose_name=_("last name"))
    phone_number = models.CharField(max_length=40, 
                        validators=[RegexValidator(r'^[0-9 ]*$', 'Only numbers are allowed.')], 
                        verbose_name=_('phone number'), blank=True, null=True)
    usertype = models.CharField(max_length=100, blank=True, null=True, choices=ROLE_CHOICE, )
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usertype']


    object = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        if self.usertype == 'superuser':
            self.is_superuser = True
            self.is_staff = True

        # elif self.userType == 'staff user':
        #     self.is_instructor = True
        #     self.is_superuser = False
        #     self.is_staff = True

        elif self.usertype == 'user':
            self.is_superuser = False
            self.is_staff = False
        super(User, self).save()

    
def validate_file_extension(value):

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', 'm4p', '.m4v', '.avi', '.wmv', '.mov', '.flv','.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Video(models.Model):
    id = models.AutoField(primary_key=True, )
    title = models.CharField(max_length=100,blank=True,null=True,verbose_name=_('title'))
    subtitle = models.CharField(max_length=1000,blank=True,null=True,verbose_name=_('subtitle'))
    video = models.FileField(upload_to=upload_video_to,max_length=256,blank=True,null=True,verbose_name=_('video'),validators=[validate_file_extension])
    order = models.IntegerField(blank=False,null=True,verbose_name=_('order'))
    videoname = models.CharField(max_length=256,null=True,verbose_name=_('video name'))
    # link = models.CharField(max_length=256,null=True,blank=True)
    is_visible = models.BooleanField(default=True)
    upload_by = models.ForeignKey('account.User', related_name='videos',on_delete=models.SET_NULL,null=True,blank=False,verbose_name=_('upload by'))
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'video'
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):

        if self.video:
            self.videoname = self.video.name
            super(Video,self).save(*args,**kwargs)
        else:
            super(Video,self).save(*args,**kwargs)

class Contact(models.Model):
    id = models.AutoField(primary_key=True,)
    name = models.CharField(max_length=50,null=False,blank=False,verbose_name=_('name'))
    email = models.EmailField(null=False,blank=False,verbose_name=_('email'))
    subject = models.CharField(max_length=50,blank=False,null=False,verbose_name=_('subject'))
    message = models.CharField(max_length=256,blank=False,null=False,verbose_name=_('message'))
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "contact"
        verbose_name = _('contact')
        verbose_name_plural = _('contact')


    def __int__(self):
        return self.id


class PageCommon(models.Model):
    id = models.AutoField(primary_key=True,)
    key = models.CharField(max_length=50,null=False,blank=False,unique=True,verbose_name=_('key'))
    content = models.CharField(max_length=2000,null=True,blank=True,verbose_name=_('content'))
    image = models.ImageField(upload_to=upload_image_to,null=True,blank=True,verbose_name=_('image'))
    title = models.CharField(max_length=100,null=True,blank=False,verbose_name=_('title'))
    subtitle = models.CharField(max_length=100,null=True,blank=True,verbose_name=_('subtitle'))
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Page_common"
        verbose_name = _('page common')
        verbose_name_plural = _('pages common')


    def __str__(self):
        return self.key

TYPE_CHOICE = [
    ("socialmedia", "socialmedia"),
    ("videogame", "videogame"),
    ("metaverse", "metaverse"),
]


class LinkManagement(models.Model):
    id = models.AutoField(primary_key=True,)
    image = models.ImageField(upload_to=upload_image_to,null=True,blank=True,verbose_name=_('image'))
    type = models.ForeignKey('account.Linktype',related_name='links',on_delete=models.RESTRICT,verbose_name=_('type'))
    key = models.CharField(max_length=20,null=True,blank=True,verbose_name=_('key'))
    link = models.CharField(max_length=500,null=False,blank=False,verbose_name=_('link'))
    page = models.ForeignKey('account.PageCommon', related_name='links',on_delete=models.CASCADE,verbose_name=_('page'))
    
    class Meta:
        db_table = "link_management"
        verbose_name = _('link management')
        verbose_name_plural = _('links management')

    def __str__(self):
        return self.link

class Linktype(models.Model):
    id = models.AutoField(primary_key=True,)
    title = models.CharField(max_length=100,null=True,blank=False,verbose_name=_('title'))
    name= models.CharField(max_length=30,verbose_name=_('name'))
    
    class Meta:
        db_table = "link_types"
        verbose_name = _('link type')
        verbose_name_plural = _('link types')

    def __str__(self):
        return self.name

class Logo(models.Model):
    id = models.AutoField(primary_key=True,)
    title = models.CharField(max_length=2000,null=True,blank=True,verbose_name=_('title'))
    description = models.CharField(max_length=2000,null=True,blank=False,verbose_name=_('description'))

    class Meta:
        db_table = "logo"
        verbose_name = _('logo')
        verbose_name_plural = _('logos')

    def __id__(self):
        return self.id