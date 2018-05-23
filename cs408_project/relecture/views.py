from django.utils import timezone
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import PostForm

from .models import Document
from .forms import DocumentForm
from .function.pdf2txt import pdf2txt
from .function.speech_to_text import speech_to_text


def index(request):
    return render(request, 'relecture/index.html')


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


def file_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(doc_file=request.FILES['doc_file'])
            new_doc.save()
            print(new_doc.doc_file.path)
            # speech_to_text(new_doc.doc_file.path)
            print(new_doc.pk)
            return redirect('pdf_upload', pk=new_doc.pk)

    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, 'relecture/file_upload.html', {'documents': documents, 'form': form})


def pdf_upload(request, pk):
    rec_doc = get_object_or_404(Document, pk=pk)
    print(rec_doc, rec_doc.pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_doc = Document(doc_file=request.FILES['doc_file'])
            pdf_doc.save()
            # pdf2txt(new_doc.doc_file.path, '1.json', '2.csv')
            return redirect('loading', rec_pk=rec_doc.pk, pdf_pk=pdf_doc.pk)


    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, 'relecture/pdf_upload.html', {'documents': documents, 'form': form})


def loading(request, rec_pk, pdf_pk):
    rec_doc = get_object_or_404(Document, pk=rec_pk)
    pdf_doc = get_object_or_404(Document, pk=pdf_pk)
    if request.method == 'POST':
        from time import sleep
        sleep(5)
        # speech_to_text(rec_doc.doc_file.path)
        # pdf2txt(pdf_doc.doc_file.path, '1.json', '2.csv')
        return redirect('pdf_view')
    else:
        return render(request, 'relecture/loading.html', {'rec_doc': rec_doc, 'pdf_doc': pdf_doc, 'first': 1})


def pdf_view(request):
    return render(request, 'relecture/pdf_view.html', {})
