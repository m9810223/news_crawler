from .writer import MarkdownWriter


class PTTWriter(MarkdownWriter):
    def __init__(self, output_path):
        super().__init__(
            output_path,
            '`{push}` [{title}]({link})' + self.SEP_ENTRY
        )
