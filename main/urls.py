
from django.urls import path,include
from . import views
from .models import NonficViewSet,TodoListViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', NonficViewSet)
router.register(r'Todolist',TodoListViewSet)
app_name ="main"
urlpatterns = [

#==================== Django REST Framework =========================
     path('route/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#=========================================================================
    path('', views.index ),
    path("home/",views.home, name="home"),
    path("login/", views.auth_login, name="auth_login"),
    path("signUp/", views.auth_signup, name="auth_signUp"),
    path("signUp/verification/<str:PostUsername>/<str:PostPassword>/", views.auth_verification, name="auth_verification"),
    path("signUp/verification/success", views.auth_success_verify, name="success_verify"),
# ======================== Site Pages ====================
    path('homeSite/<int:id>/', views.site_home, name="site_home"),

# ====================== Admin Pages ============================
   path('homeSite/admin/<int:id>/', views.admin_page, name="admin_page"),


#======================== Roles =================================
   path('homeSite/admin/<int:id>/roles/', views.role_page, name="role_page"),

    path('homeSite/admin/<int:id>/roles/add', views.role_page_ADD, name="role_page_ADD"),
# ======================= User Pages =====================
# ======================== Books ============================
# ======================= Nonfiction =========================
    path('home/books/<int:id>', views.user_books, name="user_books"),
    path("home/books/<int:id>/nonfiction",views.nonfic_books, name='nonfic_books' ),
       path("home/books/<int:id>/nonfiction/ADD", views.nonfic_books_ADD, name="nonfic_books_ADD"),
    path("home/books/<int:id>/nonfiction/GET", views.nonfic_books_GET, name="nonfic_books_GET"),
       path("home/books/<int:id>/nonfiction/DELETE", views.nonfic_books_DELETE, name="nonfic_books_DELETE"),
        path("home/books/<int:id>/nonfiction/EDIT", views.nonfic_books_EDIT, name="nonfic_books_EDIT"),
# ======================= Fiction ======================================
path("home/books/<int:id>/fiction", views.fiction_books, name="fiction_books"), 
 
# ======================== Art ===============================
    path('home/art/<int:id>', views.user_art, name="user_art"),
# ========================= Todo ===============================
   path("home/todo/<int:id>", views.user_todo, name="user_todo"),
   path("home/todo/<int:id>/GET", views.user_todo_GET, name="user_todo_GET"),
   path("home/todo/<int:id>/ADD", views.user_todo_ADD, name="user_todo_ADD"),
 path("home/todo/<int:id>/EDIT", views.user_todo_EDIT, name="user_todo_EDIT"),
  path("home/todo/<int:id>/DELETE", views.user_todo_DELETE, name="user_todo_DELETE"),

]

