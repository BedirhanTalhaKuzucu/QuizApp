from django.shortcuts import render
from rest_framework import generics
from .serializers import AdminCreateSerializer, CategorySerializer, QuizSerializer, QuestionSerializer
from .models import Category, Quiz, Question
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.

class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class QuizListView(generics.ListAPIView):

   queryset = Quiz.objects.all()
   serializer_class = QuizSerializer

   def get(self, request, *args, **kwargs):
        
        category = self.kwargs['category']

        categoryNameId = get_object_or_404(Category, category__iexact=category)
        categoryNameId = categoryNameId.id
        quizList = Quiz.objects.filter(categoryName = categoryNameId)
        
        data = QuizSerializer(quizList ,many=True).data
        return Response(data, status=status.HTTP_200_OK)


class QuestionListView(generics.ListAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

   

    def get(self, request, *args, **kwargs):
        category = self.kwargs['category']
        categoryName = get_object_or_404(Category, category__iexact=category)

        if categoryName:
            quizTitle = self.kwargs['title']
            quizTitleid = get_object_or_404(Quiz, title__iexact = quizTitle)
            

            if categoryName.id == quizTitleid.categoryName.id:
                titleId = quizTitleid.id
                questionList = Question.objects.filter(quizTitle = titleId)
                data = QuestionSerializer(questionList ,many=True).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({        'status_code': 404,        'error': 'The resource was not found'    })
        else:
            return Response({        'status_code': 404,        'error': 'The resource was not found'    })

        # quizTitle = self.kwargs['title']
        # titleId = get_object_or_404(Quiz, title__iexact = quizTitle)
        

class AddNewQuizView(generics.ListCreateAPIView):

    queryset = Quiz.objects.all()
    serializer_class = AdminCreateSerializer


class QuizRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = AdminCreateSerializer










  