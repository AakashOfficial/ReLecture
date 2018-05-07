from django.utils import timezone
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import PostForm

from .models import Document
from .forms import DocumentForm
from .function.pdf2txt import pdf2txt


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
            return HttpResponse('<div>Recording_File Uploaded</div><h1><a href="/">Relecture post</a></h1>')



    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request,'relecture/pdf_upload.html', {'documents': documents, 'form': form})

def pdf_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(doc_file= request.FILES['doc_file'])
            new_doc.save()
            pdf2txt(new_doc.doc_file.path, '1.json', '2.csv')
            return HttpResponse('<div>PDF_File Uploaded</div><h1><a href="/">Relecture post</a></h1>')


    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request,'relecture/pdf_upload.html', {'documents': documents, 'form': form})

def pdf_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(doc_file= request.FILES['doc_file'])
            new_doc.save()
            return render(request, 'relecture/pdf_view.html', {'document': new_doc})

    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request,'relecture/pdf_upload.html', {'documents': documents, 'form': form})
