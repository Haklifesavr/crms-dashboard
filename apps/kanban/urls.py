from django.urls import path
from .views import KanbanView, KanbanDataView, CreateBoardView, CreateItemView, UpdateItemBoardView, DeleteItemView, DeleteBoardView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/kanban/",
        login_required(KanbanView.as_view(template_name="app_kanban.html")),
        name="app-kanban",
    ),
    path("api/kanban-data/", KanbanDataView.as_view(), name="kanban-data"),
    path("api/create-board/", CreateBoardView.as_view(), name="create-board"),
    path("api/create-item/", CreateItemView.as_view(), name="create-item"),
    path("api/update-item/<int:pk>/", CreateItemView.as_view(), name="update-item"),
    path("api/delete-item/<int:pk>/", DeleteItemView.as_view(), name="delete-item"),
    path("api/delete-board/<int:pk>/", DeleteBoardView.as_view(), name="delete-board"),
    path('api/update-item-board/<int:task_id>/', UpdateItemBoardView.as_view(), name='update_item_board'),
]
