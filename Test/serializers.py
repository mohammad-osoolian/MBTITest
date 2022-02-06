from rest_framework import serializers
from .models import Respondent, Submit, Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'ans', 'question_num', 'submit']


class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'respondent', 'submit_date', 'ptype', 'answers']


class RespondentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respondent
        fields = ['id', 'age', 'gender', 'twitter_id', 'submits']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'option1', 'option2', 'num']
