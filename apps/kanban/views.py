from django.views.generic import TemplateView
from web_project import TemplateLayout
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Board, Item
from .serializers import BoardSerializer, ItemSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


class KanbanView(TemplateView):
    template_name = "app_kanban.html"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            TemplateLayout.init(self, context)
            return context

class KanbanDataView(APIView):
    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    

class CreateBoardView(APIView):
    def post(self, request, format=None):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateItemView(APIView):
    # POST method to create a new item
    def post(self, request):
        data = request.data.copy()
        board_id = data.get("board_id")
        if not board_id:
            return Response({"error": "board_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        board = get_object_or_404(Board, pk=board_id)
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            item = serializer.save(board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #  PUT method to update an existing itme 
    def put(self, request, pk):
        obj = Item.objects.get(id=pk)
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   
class UpdateItemBoardView(APIView):
    def put(self, request, task_id):
        try:
            # Get the task object from the database
            task = Item.objects.get(pk=task_id)
            
            # Extract the new board ID from the request data
            new_board_id = int(request.data.get('boardId'))
            
            # Update the board ID of the task
            task.board_id = new_board_id
            task.save()
            
            return Response(status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DeleteItemView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response({"message": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class DeleteBoardView(APIView):
    def delete(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        board.delete()
        return Response({"message": "Board and its items deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
