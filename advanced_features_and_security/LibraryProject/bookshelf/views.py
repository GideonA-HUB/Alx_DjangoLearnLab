from django.shortcuts import render
from .models import Book
from .forms import ExampleForm 

# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Post


@permission_required('blog.can_create', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('post_detail', post_id=post.id)
    return render(request, 'create_post.html')

@permission_required('blog.can_edit', raise_exception=True)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', post_id=post.id)
    return render(request, 'edit_post.html', {'post': post})

@permission_required('blog.can_delete', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def book_list(request):
    # Fetch all books from the database
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def book_detail(request, book_id):
    # Fetch a single book by its ID, or return a 404 error if not found
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Example action: you can save the data, send an email, etc.
            return render(request, 'bookshelf/form_example.html', {'form': form, 'message': 'Form submitted successfully!'})
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})


