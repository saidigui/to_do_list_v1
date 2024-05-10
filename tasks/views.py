from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html  import escape
from tasks.models import Collection, Task
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

def index(request): 
    context = {}

    collection_slug = request.GET.get("collection")
    if not collection_slug:
        collection = Collection.get_default_collection()
        return redirect(f"{reverse('home')}?collection=_defaut")
        
    collection =get_object_or_404(Collection, slug=collection_slug)

    context["collections"] = Collection.objects.order_by("slug")
    context["collection"] = collection
    context['tasks'] = collection.task_set.order_by("description")

    return render(request, 'tasks/index.html', context= context)


# Ajouter une collection 

def add_collection(request):


    collection_name = escape(request.POST.get("collection-name"))
    collection, created =  Collection.objects.get_or_create(name=collection_name, slug=slugify(collection_name))

    if not created:
        return HttpResponse("la collection existe déja ", status=409)
    
    return  render(request, 'tasks/collection.html',context={'collection':collection})

def delete_collection(request, collection_pk):
   collection = get_object_or_404(Collection, pk=collection_pk)
   collection.delete()
   return redirect('home')


# Ajouter une tache
@csrf_exempt
def add_task(request):

    collection = Collection.objects.get(slug=request.POST.get("collection"))
    description = escape(request.POST.get("task-description"))
    task = Task.objects.create(description=description, collection=collection)

    return  render(request, 'tasks/task.html',context={'task':task})

def  delete_task (request, task_pk):
    task=get_object_or_404(Task, pk=task_pk)
    task.delete()

    return HttpResponse("")

def get_tasks(request, collection_pk):
    collection =get_object_or_404(Collection, pk=collection_pk)
    tasks = collection.task_set.order_by('description')

    return render( request, 'tasks/tasks.html', context={"tasks":tasks, "collection":collection })