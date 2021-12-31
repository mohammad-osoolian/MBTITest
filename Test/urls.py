from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


urlpatterns = [
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
