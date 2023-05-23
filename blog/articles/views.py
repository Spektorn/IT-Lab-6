from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Article

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def sign_up(request):
    if not request.user.is_authenticated:
        # Допуск к странице, если пользователь не авторизован
        if request.method == "POST":
            # Обработать данные формы, если метод POST:
            # В словаре form будет храниться информация, введенная пользователем
            form = {
                'username': request.POST["username"],
                'email': request.POST["email"],
                'password': request.POST["password"],
            }

            if form["username"] and form["email"] and form["password"]:
                # Если поля заполнены:
                if not User.objects.filter(username=form["username"]):
                    # Если имя пользователя является уникальным:
                    # зарегистрировать пользователя
                    User.objects.create_user(form["username"], form["email"], form["password"])
                    return redirect('archive')
                else:
                    # Если имя пользователя не является уникальным:
                    form['errors'] = u"Пользователь с таким именем уже существует"
                    return render(request, 'sign_up.html', {'form': form})
            else:
                # Если введенные данные неполны:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'sign_up.html', {'form': form})
            
        else:
            # иначе просто вернуть страницу с формой, если метод GET
            return render(request, 'sign_up.html', {})
    else:
        return redirect('archive')
    
def sign_in(request):
    if not request.user.is_authenticated:
        # Допуск к странице, если пользователь не авторизован
        if request.method == "POST":
            # Обработать данные формы, если метод POST:
            # В словаре form будет храниться информация, введенная пользователем
            form = {
                'username': request.POST["username"],
                'password': request.POST["password"],
            }

            if form["username"] and form["password"]:
                # Если поля заполнены:
                user = authenticate(username=form["username"], password=form["password"])
                if user:
                    # Если пользователь прошел аутентификацию:
                    # авторизовать пользователя
                    login(request, user)
                    return redirect('archive')
                else:
                    # Если пользователь не прошел аутентификацию:
                    form['errors'] = u"Неверное имя пользователя или пароль"
                    return render(request, 'sign_in.html', {'form': form})
            else:
                # Если введенные данные неполны:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'sign_in.html', {'form': form})
            
        else:
            # иначе просто вернуть страницу с формой, если метод GET
            return render(request, 'sign_in.html', {})
    else:
        return redirect('archive')

def custom_logout(request):
    logout(request)
    return redirect('archive')

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    
    except Article.DoesNotExist:
        raise Http404
    
def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # Обработать данные формы, если метод POST:
            # В словаре form будет храниться информация, введенная пользователем
            form = {
                'title': request.POST["title"],
                'text': request.POST["text"],
            }
            
            if form["title"] and form["text"]:
                # Если поля заполнены:
                if not Article.objects.filter(title=form["title"]):
                    # Если поле заголовка статьи является уникальным:
                    # создать пост и перейти на его страницу
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=Article.objects.get(text=form["text"], title=form["title"], author=request.user ).id)
                else:
                    # Если поле заголовка статьи не является уникальным:
                    form['errors'] = u"Название статьи не является уникальным"
                    return render(request, 'create_post.html', {'form': form})
            else:
                # Если введенные данные неполны:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # иначе просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404
