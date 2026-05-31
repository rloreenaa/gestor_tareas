import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import TaskList, Task


@csrf_exempt
def task_lists(request):
    if request.method == 'GET':
        lists = TaskList.objects.all().values('id', 'name', 'created_at')
        return JsonResponse(list(lists), safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        task_list = TaskList.objects.create(name=data['name'])
        return JsonResponse({'id': task_list.id, 'name': task_list.name}, status=201)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def task_list_detail(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id)

    if request.method == 'DELETE':
        task_list.delete()
        return JsonResponse({'message': 'Lista eliminada'}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def tasks(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id)

    if request.method == 'GET':
        tasks = task_list.tasks.all().values('id', 'title', 'completed', 'created_at')
        return JsonResponse(list(tasks), safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(title=data['title'], task_list=task_list)
        return JsonResponse({'id': task.id, 'title': task.title, 'completed': task.completed}, status=201)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def task_detail(request, list_id, task_id):
    task_list = get_object_or_404(TaskList, id=list_id)
    task = get_object_or_404(Task, id=task_id, task_list=task_list)

    if request.method == 'PATCH':
        data = json.loads(request.body)
        task.completed = data.get('completed', task.completed)
        task.save()
        return JsonResponse({'id': task.id, 'title': task.title, 'completed': task.completed})

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Tarea eliminada'}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)