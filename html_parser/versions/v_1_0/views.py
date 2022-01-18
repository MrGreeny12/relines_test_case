import logging

from rest_framework import views, status
from rest_framework.response import Response

from html_parser.services import Page


logger = logging.getLogger(__name__)


class HTMLDocumentParserAPIView(views.APIView):
    '''
    Представление (v 1.0) для получения списка urls и создания документа
    '''
    def get(self, request):
        try:
            urls: list = request.GET.getlist('url')
            line_width: int = int(request.GET.get('line_width'))
            img: bool = request.GET.get('img')
            if len(urls) == 0:
                return Response('Нечего обрабатывать =(',
                                status=status.HTTP_418_IM_A_TEAPOT)
            for url in urls:
                Page(url=url, line_width=line_width, img=img).get_useful_content()
            return Response('Документы хранятся в папке files',
                            status=status.HTTP_200_OK)
        except TypeError as e:
            logger.info(e)
            return Response('Формат адреса или длинны строки указан неверно',
                            status=status.HTTP_400_BAD_REQUEST)
