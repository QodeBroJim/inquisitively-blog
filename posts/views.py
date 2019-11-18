from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from taggit.models import Tag

from .forms import CommentForm, PostForm
from .models import Post, Author, PostView, Category
from marketing.forms import EmailSignupForm, AccessTutorialSignupForm
from marketing.models import Signup, AccessTutorialSignup

def get_year():
    now = str(timezone.now().year)
    return now

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def get_pk(request):
    return request.pk

def search(request):
    queryset = Post.objects.filter(status='published').all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .filter(status='published') \
        .annotate(Count('categories__title'))
    return queryset

def get_tag_count():
    queryset = Post \
        .objects \
        .values('tags__name') \
        .filter(status='published') \
        .annotate(Count('tags__name'))
    return queryset

def get_categories(request):
    title = Post.objects.values('categories__title').filter(status='published')

    return render(request=request,
                  template_name='post_categories.html',
                  context={
                      'queryset': Category.objects.filter(title__in=title).order_by('title')
                  })

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.filter(
        status='published').order_by('-timestamp')[0:3]
    year = get_year()
    form = EmailSignupForm()
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'form': form,
        'year': year,
    }
    return render(request, 'index.html', context)

def access_tutorial_landing_page(request):
    year = get_year()
    form = AccessTutorialSignupForm()
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        hobby = request.POST['hobby']
        new_signup = AccessTutorialSignup()
        new_signup.email = email
        new_signup.first_name = first_name
        new_signup.last_name = last_name
        new_signup.hobby = hobby
        new_signup.save()
        return redirect('/database-download')

    context = {
        'form': form,
        'year': year,
    }
    return render(request, 'access_db_signup.html', context)
    
def db_download(request):
    year = get_year()
    context = {
        'year': year,
    }
    return render(request, 'access_db_download.html', context)

def about(request):
    year = get_year()
    context = {
        'year': year,
    }
    return render(request, 'about.html', context)

def blog(request):
    category_count = get_category_count()
    tag_count = get_tag_count()
    year = get_year()
    most_recent = Post.objects.filter(
        status='published').order_by('-timestamp')[:3]
    post_list = Post.objects.filter(status='published').order_by('-timestamp')
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'tag_count': tag_count,
        'year': year,
    }
    return render(request, 'blog.html', context)

def blog_by_category(request, category_slug):
    category_count = get_category_count()
    tag_count = get_tag_count()
    year = get_year()
    most_recent = Post.objects.filter(
        status='published').order_by('-timestamp')[:3]
    post_list = Post.objects.filter(categories__title=category_slug).order_by('-timestamp')[:3]
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'tag_count': tag_count,
        'year': year,
    }
    return render(request, 'blog_by_category.html', context)

def blog_by_tag(request, tag_slug):
    category_count = get_category_count()
    tag_count = get_tag_count()
    year = get_year()
    most_recent = Post.objects.filter(
        status='published').order_by('-timestamp')[:3]
    post_list = Post.objects.filter(tags__slug=tag_slug).order_by('-timestamp')
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'tag_count': tag_count,
        'year': year,
    }
    return render(request, 'blog_by_tag.html', context)

def post(request, pk):
    category_count = get_category_count()
    tag_count = get_tag_count()
    most_recent = Post.objects.filter(status='published').order_by('-timestamp')[:3]
    post = get_object_or_404(Post, slug=pk)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'pk': pk
            }))
    context = {
        'form': form,
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'tag_count': tag_count,
    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'pk': form.instance.slug
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)

def post_update(request, pk):
    title = 'Update'
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'pk': form.instance.slug
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect(reverse('post-list'))