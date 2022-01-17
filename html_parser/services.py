class Page():

    def __init__(self, url: str, line_width: int):
        self.url = url
        self.line_width = line_width
        self.document_format = '.txt'

    def parse(self):
        ...

    def _validate(self):
        ...

    def _apply_settings(self):
        ...

    def _create_document(self):
        ...
