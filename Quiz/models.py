from django.db.models.deletion import CASCADE
from django.db import models



# Create your models here.
class Category(models.Model):
    category=models.CharField(max_length=35)

    def __str__(self):
        return self.category

        

class Quiz(models.Model):
    title= models.CharField(max_length=50, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    categoryName= models.ForeignKey(Category, on_delete=models.PROTECT,  related_name='quiz')

    def __str__(self):
        return self.title


class  Question(models.Model):
    DIFFICULTY= (
        ("H", "Hard"),
        ("M", "Middle"),
        ("E", "Easy"),

    )
    question= models.CharField(max_length=250)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY, default="M")
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    quizTitle =models.ForeignKey(Quiz, on_delete=models.PROTECT, related_name="questions", null=True)

    def __str__(self):
        return self.question
 




class Answer(models.Model):
    updateDate = models.DateTimeField(auto_now=True)
    answer=models.CharField(max_length=200)
    is_right=models.BooleanField(default=False)
    questionTitle = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")

    def __str__(self):
        return f" {self.questionTitle.quizTitle} =>{self.questionTitle} =>{self.answer} => {self.is_right}"
