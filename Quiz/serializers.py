from asyncore import write
from os import read
from unicodedata import category

from requests import Response
from .models import Category, Quiz, Question, Answer
from rest_framework import serializers
from rest_framework import generics
from django.shortcuts import get_object_or_404


class AnswerSerializer(serializers.ModelSerializer):

    answer_id = serializers.IntegerField(source="id", required=False)

    class Meta:
        model = Answer
        fields = ('answer_id', 'answer', 'is_right')


class CategorySerializer(serializers.ModelSerializer):

    quiz_count=  serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'category', 'quiz_count')

    
    def get_quiz_count(self, obj):
        return Quiz.objects.filter(categoryName = obj.id).count()


class QuizSerializer(serializers.ModelSerializer):

    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ('title', 'question_count')

    def get_question_count(self, obj):
        return Question.objects.filter(quizTitle = obj.id).count()


class QuestionSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source="id", required=False)
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ("question_id",'question', 'difficulty', "answer")


class AdminCreateSerializer(serializers.ModelSerializer):
    categoryName = serializers.StringRelatedField() #default read_only
    questions = QuestionSerializer(many=True)
    category = serializers.CharField(write_only= True, required=True )
    quiz_id = serializers.IntegerField(source="id", required=False)


    # user = serializers.StringRelatedField()  # default read_only=True
    
    class Meta:
        model = Quiz
        fields =(
            'quiz_id',
            "categoryName",
            'category',
            "title",
            "questions",
        )
        
    def create(self, validated_data):
        category = validated_data.pop('category')
        questions=validated_data.pop("questions")
        
        #category modeli sorgulama veya create        
        if Category.objects.filter(category__iexact=category).exists():
            category = Category.objects.get(category__iexact=category)
        else:
            category = Category.objects.create(category=category)

        #quiz modeli sorgulama veya create        
        title=validated_data['title']
        if Quiz.objects.filter(title__iexact=title).exists():
            print("asdasdasd")
            quiz = get_object_or_404(Quiz, title__iexact=title)        
        else:
            validated_data['categoryName'] = category
            quiz= Quiz.objects.create(**validated_data)
        
        for item in questions:
            answer=item.pop("answer")
            item['quizTitle'] = quiz
            question = Question.objects.create(**item)

            for item in answer:
                item['questionTitle'] = question
                answerCreated = Answer.objects.create(**item)
        return quiz

    def update(self, instance, validated_data):

        category = validated_data.pop('category')
        questions=validated_data.pop("questions")

        #category UPDATE
        if Category.objects.filter(category__iexact=category).exists():
            category = Category.objects.get(category__iexact=category)
        else:
            category = Category.objects.create(category=category)

        instance.categoryName = category


        #quizTitle UPDATE
        title=validated_data['title']
        instance.title=title

        #I got the ids of the existing questions and answers
        availableQuestions = instance.questions.all()
        availableQuestionsIdList = []
        availableAnswersIdLis= []
        for item in availableQuestions:
            answerIdlist = item.answer.all()
            for answerId in answerIdlist:
                availableAnswersIdLis.append(answerId.id)

            availableQuestionsIdList.append(item.id)


        #gönderilen question ve answer idleri alıyor
        updatedQuestionIdlist= []
        updatedAnswerIdlist=[]
        for item in questions:
            if "id" in item.keys():
                for answerId in item['answer']:
                    if "id" in answerId.keys():
                        updatedAnswerIdlist.append(answerId['id'])
                updatedQuestionIdlist.append(item["id"])
        # print(updatedAnswerIdlist)
        # print(updatedQuestionIdlist)



        #quesiton deleted
        for Id in availableQuestionsIdList:
            if Id in updatedQuestionIdlist:
                pass
            else:
                print("yok", Id)
                instance.questions.exclude(id=Id)
                a = Question.objects.get(id =Id)
                a.delete()
                availableQuestions = availableQuestions.exclude(id=Id)


        #answer deleted
        for Id in availableAnswersIdLis:
            if Id in updatedAnswerIdlist:
                pass
            else:
                print('yok', Id)
                a = Answer.objects.get(id =Id)
                a.delete()
       


        #update question 
        for  item in questions:
            answers =item.pop('answer')
                    
            if 'id' in item.keys():
                #gelen question mevcut quizin içinde mi değil mi
                if availableQuestions.filter(id=item['id']).exists():
                    question = availableQuestions.filter(id=item['id'])
                    question.update(**item)
                    question =  question[0]
                else:
                    question = get_object_or_404(Question, id=item['id'])
                    instance.questions.add(question)         
            else:
                item['quizTitle'] = instance
                question = Question.objects.create(**item)

            #answer updated
            for i in answers:
                if 'id' in i:
                    updateAnswer= Answer.objects.filter(id = i['id'])
                    updateAnswer.update(**i)
                else:
                    i['questionTitle'] = question
                    newAnswer=Answer.objects.create(**i)
            


        instance.save()

        return instance


   
