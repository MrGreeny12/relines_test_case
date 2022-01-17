from django.urls import path

from html_parser.versions.v_1_0.views import HTMLDocumentParserAPIView

urlpatterns = [
    path('html-parser/', HTMLDocumentParserAPIView.as_view(), name='upload_urls_list'),
]
