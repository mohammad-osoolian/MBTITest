from django.urls import path, include
from rest_framework import routers
from .api_views import RespondentViewSet, SubmitViewSet, AnswerViewSet
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


router = routers.DefaultRouter()
router.register('respondents', RespondentViewSet, basename='respondent')
router.register('submits', SubmitViewSet, basename='submit')
router.register('answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('api/', include(router.urls)),
    path('openapi', get_schema_view(
                title="MBTI Test",
                description="API for all things …",
                version="1.0.0"
            ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger-ui'),
]
