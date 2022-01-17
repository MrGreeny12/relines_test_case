from rest_framework import views, status
from rest_framework.response import Response

from html_parser.services import Page


class HTMLDocumentParserAPIView(views.APIView):
    '''
    Представление (v 1.0) для получения списка urls и создания документа
    '''

    def get(self, request):
        try:
            urls: list = request.GET.getlist('url')
            line_width: int = int(request.GET.get('line_width'))
            if len(urls) == 0:
                return Response('Нечего обрабатывать =(',
                                status=status.HTTP_418_IM_A_TEAPOT)
            for url in urls:
                Page(url=url, line_width=line_width).parse()
            return Response(status=status.HTTP_200_OK)
        except TypeError:
            return Response('Формат адреса или длинны строки указан неверно',
                            status=status.HTTP_400_BAD_REQUEST)
