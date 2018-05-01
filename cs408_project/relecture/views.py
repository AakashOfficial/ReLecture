from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import PostForm

from django.template import RequestContext
from .models import Document
from .forms import DocumentForm
from django.core.urlresolvers import reverse


def test(request):
    return render(request, 'relecture/test.html')


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'relecture/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'relecture/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'relecture/post_detail.html', {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'relecture/post_edit.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(doc_file= request.FILES['doc_file'])
            new_doc.save()
            return HttpResponse('File Uploaded')



    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request,'relecture/file_upload.html', {'documents': documents, 'form': form})
