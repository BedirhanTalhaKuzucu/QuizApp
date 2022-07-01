from django.contrib import admin
from .models import Category, Answer, Question, Quiz
import nested_admin



class AnswerInline(nested_admin.NestedTabularInline): 
    model = Answer
    # fk_name = Answer

    # extra = 1
    # # # classes = ('collapse',)
    min_num = 4
    max_num = 4



    


class QuestionInline(nested_admin.NestedTabularInline):
    '''Tabular Inline View for '''
    model = Question
    extra = 1
    fields= ("question", "difficulty")
    inlines = (AnswerInline,)

    # readonly_fields = ('changeform_link', )
    # classes = ('collapse',)
    # min_num = 4
    # max_num = 4

class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ("title", "createdDate", "categoryName")
    inlines = (QuestionInline,)



admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category)

