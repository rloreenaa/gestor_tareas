from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TaskList, Task
from .serializers import TaskListSerializer, TaskSerializer


@api_view(['GET', 'POST'])
def task_lists(request):
    if request.method == 'GET':
        lists = TaskList.objects.all()
        serializer = TaskListSerializer(lists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def task_list_detail(request, list_id):
    task_list = get_object_or_404(TaskList, pk=list_id)
    task_list.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def tasks(request, list_id):
    task_list = get_object_or_404(TaskList, pk=list_id)

    if request.method == 'GET':
        tasks = Task.objects.filter(task_list=task_list)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['task_list'] = list_id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
def task_detail(request, list_id, task_id):
    task = get_object_or_404(Task, pk=task_id, task_list_id=list_id)

    if request.method == 'PATCH':
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)