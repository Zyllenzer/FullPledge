from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from django.core.signing import Signer, BadSignature
import math
from website_proj7_08_2023_bookFullpledge import settings
from django.contrib.auth.hashers import make_password, check_password
from .models import UserSite, NonFictionBook, NonficViewSet, NonficSerializer, TodoList, TodoListSerializer, Role, BookUpdate, TodoUpdate

def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def home(request):
    context ={}
    return render(request, 'main/home.html', context)

def auth_login(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        
        try:
            u = UserSite.objects.get(username =json_data['username'])
            security_pass = check_password(json_data['password'],u.password)       
            if(not security_pass):
                return JsonResponse({'msg':"Server err"}, status = 500)
            else:
                
                context ={
                    "id":u.id
                }
                return JsonResponse({"id":context}, status = 200)
        except:
            pass
    context = {}
    return render(request, 'main/login.html', context)

def auth_signup(request):
    if request.method == "POST":

        json_data = json.loads(request.body)
        if(json_data['username'] and json_data['password']):
            try:
                u  = UserSite.objects.filter(username =json_data['username'])
                if(u):
                    return JsonResponse({"msg":"The username has been used"},status=500)
            except:
                pass
            signer = Signer()
            username_sh = signer.sign(json_data['username'])
            password_sh = signer.sign(json_data['password'])
            context ={
                "username_sh":username_sh,
                "password_sh":password_sh,
            }  
            return JsonResponse({"data":context})
    context = {}
    return render(request, 'main/signup.html', context)

def auth_verification(request, PostPassword, PostUsername):
    if request.method =="POST":
        json_data = json.loads(request.body)
       
        signer = Signer()
        username = signer.unsign(json_data["username"])
        password = signer.unsign(json_data["password"])
     
        u = UserSite()
        lastID = UserSite.objects.values('id').last()
        u.id = lastID['id'] +1
        u.username = username
        u.password =password
        u.email = json_data['email']
        u.save() 
        return JsonResponse({"msg":"Data has been successfuly sent"})    
    context = {
        "PostPassword": PostPassword,
        "PostUsername":PostUsername,
    }
    return render(request, 'main/verification-site/verification.html', context)

def auth_success_verify(request):
    context = {}
    return render(request, "main/verification-site/verify-success.html", context)

# ========================== SITE PAGES ==================

def site_home(request, id):
    u = UserSite.objects.get(id=id)
    r = Role.objects.get(user_ref = u)
    if(r.admin_role):
        url=f"/homeSite/admin/{id}/"
        return redirect(url)
        """
         context = {
                  "id": u.id
         }
         return render(request, "main/site/admin/admin-home-page.html", context)
        """
    elif(r.user_role):
         context = { 
             "username":u.username,
             "id": u.id
         }
         return render(request, "main/site/user/user-home-page.html", context)
    else:
        url="/signUp/verification/success"
        return redirect(url)

#============================= ADMIN PAGE ==========================
def admin_page(request, id ):
    b = BookUpdate.objects.all().order_by("date_action_created")
    t = TodoUpdate.objects.all().order_by("date_action_created")
    user_count = UserSite.objects.all().count()
    
    context = {
            "id": id,
            "BookUpdate_Collection": b,
            "TodoList_Collection":t,
            "user_count":user_count, 
    }
    return render(request, "main/site/admin/admin-home-page.html", context)

# ========================= ROLES =========================
def role_page(request, id):
    u_username = UserSite.objects.get(id=id)
    r_users = Role.objects.filter(user_role = True).order_by("user_ref__username")
    r_admin = Role.objects.filter(admin_role = True).order_by("user_ref__username")

    context = {
        "id":id,
         "username":u_username,
         "user_roles": r_users,
         "admin_roles": r_admin,
    }  
    return render(request,"main/site/admin/roles/home-roles.html", context)

def role_page_ADD(request, id):
    u = UserSite.objects.all().order_by("username")

    if request.method == "POST":
        json_data = json.loads(request.body)
        u_ref = UserSite.objects.get(username = json_data['username'])
        r = Role.objects.get(user_ref = u_ref)
        r.user_role = json_data['role_user']
        r.admin_role = json_data["role_admin"]
        r.save()
        return JsonResponse({"msg":"Data has been successfuly sent"})   
      


       
    context ={
        "id":id,
        "users_choose":u,

    }
    return render(request, "main/site/admin/roles/add-roles.html", context )

def role_page_EDIT(request,id):
    u = UserSite.objects.get(id=id)
    r = Role.objects.get(user_ref =u)
  
    context = {
        "id":id,
        "user":u,
        "roles":r,
    }
    if (request.method =="POST"):
        json_data = json.loads(request.body)
        print(json_data)
        user = UserSite.objects.get(username = json_data['username'])
        role = Role.objects.get(user_ref = user)
        role.user_role = json_data['role_user']
        role.admin_role = json_data['role_admin']
        role.save()
        return JsonResponse({"msg":"Data has been successfuly sent"})   
        #print("this is for post edit")
        
    return render(request,"main/site/admin/roles/edit-roles.html", context)
# =============================== USER PAGES =======================
#========================== BOOKS ================================
def user_books(request,id):
    
    u = UserSite.objects.get(id=id)

    context = {
         "username":u.username,
         "id": u.id
    }
    return render(request, "main/site/user/books/book-choice.html", context)

# ======================= NONFICTION  ==========================================
def nonfic_books_ADD(request,id):
    if request.method =="POST":
        u = UserSite.objects.get(id=id)
       
      
        n = NonFictionBook()
        LastID = NonFictionBook.objects.values("id").last()
        n.id = LastID['id'] + 1
        n.user_ref = u
        n.bookImage = request.FILES.get("inp_file_image")
        n.bookFile = request.FILES.get("inp_file_book")
        n.author = request.POST.get("inp_file_author")
        n.book_name = request.POST.get("inp_file_BookName")
        n.save()
        n =  NonFictionBook.objects.get(id = LastID['id'] + 1 )
        updates = BookUpdate()
        updatesLastID = BookUpdate.objects.values("id").last()
        updates.id = updatesLastID['id'] + 1
        updates.user = n.user_ref.username
        updates.book_title = n.book_name
        updates.actions = "Added"
        updates.save()
    
    return JsonResponse({"msg":"operation complete"},status=200)
def nonfic_books_EDIT(request,id):
    if(request.method  == "GET"):
     
        n = NonFictionBook.objects.get(id=id)
        serializer =  NonficSerializer(n)
        return JsonResponse({"data":(serializer.data)},status=200, content_type="application/json")
    elif(request.method =="POST"):

        n = NonFictionBook.objects.get(id=id)
        updates = BookUpdate()
        updatesLastID = BookUpdate.objects.values("id").last()
        updates.id = updatesLastID['id'] + 1
        updates.user = n.user_ref.username
        updates.book_title = n.book_name
        updates.actions = "Edited"
        updates.save()
        book_image = request.FILES.get('inp_file_image') or None
        book_file = request.FILES.get("inp_file_BookName") or None
        n.author = request.POST.get("inp_file_author")
        n.book_name = request.POST.get("inp_file_BookName")
        if(book_image != None):
            n.bookImage = book_image
        if(book_file != None):
            n.bookFile = book_file
        n.save()
        # if(request.FILES('get')):
        #     print("have file")

        return JsonResponse({"msg": "has been accomplish"}, status =200 )
   

def nonfic_books_GET(request,id):
    u = UserSite.objects.get(id =id)
    if request.method == "GET":
        nonfic_collection = NonFictionBook.objects.filter(user_ref = u.id).order_by("book_name")
        serializer = NonficSerializer(nonfic_collection, many=True)
        return JsonResponse({"data":(serializer.data)},status=200, content_type="application/json")
    
def nonfic_books_DELETE(request,id):
    if request.method =="POST":
        json_data = json.loads(request.body)
       
        n = NonFictionBook.objects.get(id = json_data['id'])
        updates = BookUpdate()
        updatesLastID = BookUpdate.objects.values("id").last()
        updates.id = updatesLastID['id'] + 1
        updates.user = n.user_ref.username
        updates.book_title = n.book_name
        updates.actions = "Deleted"
        updates.save()
        n.delete()
    
    return JsonResponse({"msg":"operation completed"}, status =200)

def nonfic_books(request, id):
    u = UserSite.objects.get(id =id)
    nonfic_collection = NonFictionBook.objects.filter(user_ref = u.id).order_by("book_name")
    count = 0
    for data in nonfic_collection:
        count +=1
    loopcount = count /3

    if loopcount <=0:
        loopcount = 1
    else:
        loopcount = math.ceil(loopcount)
    context ={
         "username":u.username, 
          "id":id,
          "loopcount":loopcount, 
    }
    return render(request, 'main/site/user/books/non-fiction/nonfiction-home.html', context)

#================================ FICTION ==========================================
def fiction_books(request, id):
    context = {
        "id":id
    }
    return render(request, "main/site/user/books/fiction/fiction-home.html", context)

# ============================== ART ======================
def user_art(request, id ):
    u = UserSite.objects.get(id=id)
    context = {
          "username":u.username,
            'id':id,
    }
    return render(request,"main/site/user/art/base-art.html",context)
#=========================== TODO ===============================
def user_todo(request, id):
   
    u = UserSite.objects.get(id=id)
    todolist_loop = TodoList.objects.filter(user_ref = u.id).count()
 
    context ={
        "username":u.username,
        "id":id,
        "todolist_loop":todolist_loop,
    }
    return render(request, 'main/site/user/todoApp/base-todoApp.html', context)

def user_todo_GET(request, id ):
    u = UserSite.objects.get(id=id)
    todolist_collection = TodoList.objects.filter(user_ref = u.id).order_by("due_date")
    serializer = TodoListSerializer(todolist_collection, many=True)
    return JsonResponse({"data":(serializer.data)},status=200, content_type="application/json")

def user_todo_ADD(request,id):

    if request.method =="POST":
        json_data = json.loads(request.body)
        print(json_data)
        u = UserSite.objects.get(id =id)
        t = TodoList()
        lastID = TodoList.objects.values('id').last()
        t.user_ref = u
        t.id = lastID['id']+1
        t.task_description = json_data['task_desc']
        t.due_date = json_data['duedate']
        t.save()
        return JsonResponse({"msg":"operation complete"}, status =200)

def user_todo_EDIT(request, id):
    if request.method =="POST":
        json_data = json.loads(request.body)
        t = TodoList.objects.get(id = json_data['id'])
        t.task_description = json_data['task_desc']
        t.due_date = json_data['due_date']
        t.completed = json_data["completed"]
        t.save()
        print(json_data)
        return JsonResponse({'msg':"operation completed"}, status = 200)

def user_todo_DELETE(request, id):

    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        t = TodoList.objects.get(id=json_data['id'])
        t.delete()
        print("this is for delete POST")
        return JsonResponse({'msg':"operation completed"}, status = 200)


    