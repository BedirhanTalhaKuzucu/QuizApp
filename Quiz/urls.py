from django.urls import path
from .views import CategoryList, QuizListView, QuestionListView, AddNewQuizView, QuizRUDView

urlpatterns = [
    path('category', CategoryList.as_view(), name="category"),
    path('category/<str:category>/', QuizListView.as_view(), name="category"),
    path('category/<str:category>/<str:title>', QuestionListView.as_view(), name="quiz"),
    path('add', AddNewQuizView.as_view()),
    path('update/<int:pk>/', QuizRUDView.as_view()),

]