# Generated by Django 3.2 on 2022-06-16 12:08

import account.models
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=256, verbose_name='password')),
                ('first_name', models.CharField(blank=True, help_text='Enter name', max_length=40, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z ]*$', 'Only characters are allowed.')], verbose_name='first name')),
                ('last_name', models.CharField(blank=True, help_text='Enter name', max_length=40, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z ]*$', 'Only characters are allowed.')], verbose_name='last name')),
                ('phone_number', models.CharField(blank=True, max_length=40, null=True, validators=[django.core.validators.RegexValidator('^[0-9 ]*$', 'Only numbers are allowed.')], verbose_name='phone number')),
                ('usertype', models.CharField(blank=True, choices=[('superuser', 'superuser'), ('user', 'user')], max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('subject', models.CharField(max_length=50, verbose_name='subject')),
                ('message', models.CharField(max_length=256, verbose_name='message')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contact',
                'db_table': 'contact',
            },
        ),
        migrations.CreateModel(
            name='PageCommon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50, unique=True, verbose_name='key')),
                ('content', django_quill.fields.QuillField(blank=True, null=True, verbose_name='content')),
                ('image', models.ImageField(upload_to=account.models.upload_image_to, verbose_name='image')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='title')),
                ('subtitle', models.CharField(blank=True, max_length=100, null=True, verbose_name='subtitle')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'page common',
                'verbose_name_plural': 'pages common',
                'db_table': 'Page_common',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('subtitle', models.CharField(blank=True, max_length=1000, verbose_name='subtitle')),
                ('video', models.FileField(max_length=256, upload_to=account.models.upload_video_to, validators=[account.models.validate_file_extension], verbose_name='video')),
                ('order', models.IntegerField(verbose_name='order')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('upload_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL, verbose_name='upload by')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
                'db_table': 'video',
            },
        ),
        migrations.CreateModel(
            name='LinkManagement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=account.models.upload_image_to, verbose_name='image')),
                ('type', models.CharField(choices=[('social', 'social'), ('videogame', 'videogame'), ('metaverse', 'metaverse')], max_length=30, verbose_name='type')),
                ('key', models.CharField(max_length=20, verbose_name='key')),
                ('link', models.CharField(max_length=500, verbose_name='link')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='account.pagecommon', verbose_name='page')),
            ],
            options={
                'verbose_name': 'link management',
                'verbose_name_plural': 'links management',
                'db_table': 'link_management',
            },
        ),
    ]
