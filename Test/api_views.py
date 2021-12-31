from rest_framework import viewsets
from .models import Respondent, Answer, Submit
from .serializers import RespondentSerializer, SubmitSerializer, AnswerSerializer


class RespondentViewSet(viewsets.ModelViewSet):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer


class SubmitViewSet(viewsets.ModelViewSet):
    queryset = Submit.objects.all()
    serializer_class = SubmitSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class =  AnswerSerializer
