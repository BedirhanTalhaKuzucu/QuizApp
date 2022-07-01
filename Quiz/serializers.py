from asyncore import write
from os import read
from unicodedata import category
from .models import Category, Quiz, Question, Answer
from rest_framework import serializers
from rest_framework import generics
from django.shortcuts import get_object_or_404


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer', 'is_right')


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

    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('question', 'difficulty', "answer")


class AdminCreateSerializer(serializers.ModelSerializer):
    categoryName = serializers.StringRelatedField() #default read_only
    questions = QuestionSerializer(many=True)
    category = serializers.CharField(write_only= True, required=True )
    # user = serializers.StringRelatedField()  # default read_only=True
    
    class Meta:
        model = Quiz
        fields =(
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
        print(instance.categoryName)
        category = Category.objects.create(category=category)
        instance.categoryName = category
        instance.save()
        # instance.passenger.all()

        # #update yapılırken yolcu silmek için
        # mevcutIdlist=[Id.id for Id in mevcut ]
        # updatedIdlist= [item["id"] for item in passenger_data if "id" in item.keys()]
        # for Id in mevcutIdlist:
        #     if Id in updatedIdlist:
        #         pass
        #     else:
        #         print("yok", Id)
        #         mevcut = mevcut.exclude(id=Id)
        # instance.passenger.set(mevcut)
        # # print(instance.passenger.all())
      
        # #update yaperken var olan yolcuları güncellemek, olmayanları creat etmek için
        # for  passenger in passenger_data:
        #     #gelen bilgilerde yolcu id si var mı? var ise bu id mevcut rezervasyonda mı yoksa var olan diğer yolcular arasında mı
        #     if "id" in passenger.keys():
        #         pas = mevcut.filter(id=passenger["id"])
        #         if pas:
        #             pas = pas.update(**passenger)
        #         else:
        #             pas = Passenger.objects.get(id=passenger["id"])
        #             instance.passenger.add(pas)
        #     else: 
        #             pas = Passenger.objects.create(**passenger)
        #             print(pas)
        #             instance.passenger.add(pas)

    
        # instance.flight_id = validated_data["flight_id"]
        # instance.save()

        return instance


   
