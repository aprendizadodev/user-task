from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from apptask.models import User
from apptask.models import Task
from apptask.serializers import UserSerializer
from apptask.serializers import TaskSerializer
from rest_framework.decorators import api_view

# OBTER lista de user, POSTAR um novo user, EXCLUIR todos os users
@api_view(['GET', 'POST', 'DELETE'])
def user_list(request):
    # Recuperar todos os users / localizar por nome
    if request.method == 'GET':
        users = User.objects.all()
        
        name = request.GET.get('name', None)
        if name is not None:
            users = users.filter(name__icontains=name)
        
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
        # 'safe=False' para serialização de objetos

    # Criar e salvar um novo user
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Excluir todos os users do banco de dados
    elif request.method == 'DELETE':
        count = User.objects.all().delete()
        return JsonResponse({'message': '{} Usuários deletados com sucesso!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    

# GET / PUT / DELETE user
# Encontrar um único user pelo id:
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    
    # localizar user por pk (id)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message': 'O usuário não existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)

    # Atualizar um usuário pelo id na solicitação
    elif request.method == 'PUT': 
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data) 
        if user_serializer.is_valid(): 
            user_serializer.save() 
            return JsonResponse(user_serializer.data) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Excluir um usuário com id especifico
    elif request.method == 'DELETE': 
        user.delete()
        return JsonResponse({'message': 'Usuário deletado com sucesso!'}, status=status.HTTP_204_NO_CONTENT)


# OBTER lista de task, POSTAR uma nova task, EXCLUIR todos as tasks
@api_view(['GET', 'POST', 'DELETE'])
def task_list(request):
    # Recuperar todas as tasks / localizar por 
    if request.method == 'GET':
        tasks = Task.objects.all()
        
        state = request.GET.get('state', None)
        if state is not None:
            tasks = tasks.filter(name__icontains=state)
        
        tasks_serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(tasks_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    # Criar e salvar uma nova task
    elif request.method == 'POST':
        task_data = JSONParser().parse(request)
        task_serializer = TaskSerializer(data=task_data)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse(task_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Excluir todas as task do banco de dados
    elif request.method == 'DELETE':
        count = Task.objects.all().delete()
        return JsonResponse({'message': '{} Tarefas deletadas com sucesso!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    

# GET / PUT / DELETE task
# Encontrar uma única task pelo id:
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    
    # localizar task por pk (id)
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({'message': 'Não existe tarefa com este código!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        task_serializer = TaskSerializer(task)
        return JsonResponse(task_serializer.data)

    # Atualizar uma task pelo id na solicitação
    elif request.method == 'PUT': 
        task_data = JSONParser().parse(request)
        task_serializer = TaskSerializer(task, data=task_data)
        if task_serializer.is_valid(): 
            task_serializer.save() 
            return JsonResponse(task_serializer.data) 
        return JsonResponse(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Excluir uma task com id especifico
    elif request.method == 'DELETE': 
        task.delete()
        return JsonResponse({'message': 'Tarefa deletada com sucesso!'}, status=status.HTTP_204_NO_CONTENT)


# OBTER todas as tasks pendentes
@api_view(['GET'])
def task_list_state(request):
    tasks = Task.objects.filter(state=False)
        
    if request.method == 'GET': 
        tasks_serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(tasks_serializer.data, safe=False)

# OBTER tasks relacionadas a um usuário
@api_view(['GET'])
def task_list_user(request, pk):
    task = Task.objects.filter(user_id=pk)
    if task.exists() == False:
        return JsonResponse({'message': 'Não existe tarefa vinculada a este usuário!'}, status=status.HTTP_404_NOT_FOUND)

    elif task.exists() == True:
        task = Task.objects.filter(user_id=pk)
        if request.method == 'GET':
            task_serializer = TaskSerializer(task, many=True)
            return JsonResponse(task_serializer.data, safe=False)