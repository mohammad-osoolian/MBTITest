import coreapi
from rest_framework import viewsets, status
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from  rest_framework.views import APIView
from .models import Respondent, Answer, Submit, Question
from .serializers import RespondentSerializer, SubmitSerializer, AnswerSerializer, QuestionSerializer


class RespondentViewSet(viewsets.ModelViewSet):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer


class SubmitViewSet(viewsets.ModelViewSet):
    queryset = Submit.objects.all()
    serializer_class = SubmitSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class MBTITestView(APIView):
    def post(self, request):
        respondent_dict = request.data['respondent']
        respondent_dict["submits"]= []
        answers_list = request.data['answers']
        rs = RespondentSerializer(data=respondent_dict)
        if (not rs.is_valid()) or len(answers_list) != 60:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for ans in answers_list:
            if ans not in [option[0] for option in Answer.ANSWER_OPTIONS]:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if Respondent.objects.filter(twitter_id=respondent_dict['twitter_id']):
            respondent = Respondent.objects.get(twitter_id=respondent_dict['twitter_id'])
        else:
            respondent = rs.save()

        submit = Submit.objects.create(respondent=respondent)
        for i, ans in enumerate(answers_list):
            Answer.objects.create(ans=ans, question_num=i+1, submit=submit)

        submit.update_ptype()
        context = {"ptype": submit.ptype}
        return Response(data=context, status=status.HTTP_201_CREATED)
