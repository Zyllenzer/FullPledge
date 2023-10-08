from django.db import models
from django.contrib.auth.hashers import make_password
from rest_framework import serializers,viewsets
# Create your models here.
from website_proj7_08_2023_bookFullpledge import settings

# Create your models here.


  


class UserSite(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=
                              250, unique=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=1024)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(UserSite, self).save(*args, **kwargs)
    def __str__(self):
        return self.username
class Role(models.Model):
     user_ref = models.ForeignKey(UserSite, on_delete=models.CASCADE)
     user_role = models.BooleanField(default=False)
     admin_role = models.BooleanField(default=False)
     def __str__(self):
        return self.user_ref.email


class NonFictionBook(models.Model):
    id = models.AutoField(primary_key=True)
    user_ref = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    author = models.CharField(max_length=250)
    current_page =models.IntegerField(blank=True, null=True)
    last_page= models.IntegerField(blank=True, null=True)
    bookImage = models.FileField(upload_to="uploads/book-img/", null=True, blank=True)
    bookFile = models.FileField(upload_to="uploads/book-file/", null=True, blank=True)
    book_name = models.CharField(max_length=250)
    date_modified = models.DateField(auto_now=True, null=True,blank=True)


class BookUpdate(models.Model):
     id = models.AutoField(primary_key=True)
     user = models.CharField(max_length=250, null=True)
     book_title = models.CharField(max_length=250, null=True)
     actions = models.CharField(max_length=250 , null=True)
     date_action_created = models.DateField(auto_now_add=True , null=True)


class TodoUpdate(models.Model):
     id = models.AutoField(primary_key=True)
     user = models.CharField(max_length=250)
     description = models.CharField(max_length=250)
     actions = models.CharField(max_length=250)
     date_action_created = models.DateField(auto_now_add=True)

class NonficSerializer(serializers.HyperlinkedModelSerializer):
        """
        bookFile_url = serializers.SerializerMethodField()
        bookImage_url = serializers.SerializerMethodField()
        def get_bookFile_url(self, obj):
            request = self.context.get('request')
            if obj.bookFile:
                absolute_url = obj.bookFile.url
                base_url = request.build_absolute_uri('/')
                relative_url = absolute_url.replace(base_url, '', 1)
                return relative_url
            return None
        def get_bookImage_url(self, obj):
            request = self.context.get('request')
            if obj.bookImage:
                absolute_url = obj.bookImage.url
                base_url = request.build_absolute_uri('/')
                relative_url = absolute_url.replace(base_url, '', 1)
                return relative_url
            return None  
        """
        class Meta:
            model = NonFictionBook
            fields = ('id','author', 'bookImage', "bookFile",'book_name',"last_page","current_page","date_modified")
            #fields = ('id','author', 'bookImage_url', "bookFile_url",'book_name')
  
   
class NonficViewSet(viewsets.ModelViewSet):
    queryset = NonFictionBook.objects.all()
    serializer_class = NonficSerializer


class TodoList(models.Model):
     id = models.AutoField(primary_key=True)
     user_ref = models.ForeignKey(UserSite, on_delete=models.CASCADE)
     task_description = models.CharField(max_length=250)
     completed = models.BooleanField(default=False)
     due_date = models.DateField()
     

class TodoListSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
          model = TodoList
          fields = ('id','task_description','completed', 'due_date')

class TodoListViewSet(viewsets.ModelViewSet):
     queryset = TodoList.objects.all()
     serializer_class = TodoListSerializer


class SiteVisited(models.Model):
     id = models.AutoField(primary_key=True)
     date_visited = models.DateField(auto_created=True)
     number_visitor = models.IntegerField()

