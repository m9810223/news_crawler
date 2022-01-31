from .writer import MarkdownWriter


class YouratorWriter(MarkdownWriter):
    def __init__(self, output_path):
        super().__init__(
            output_path,
            '\n'.join((
                '''[{title}]({link}) - [{company}]({company_link})''',
                '',
                '```',
                '''{work_place} {salary}''',
                '',
                '''{description}''',
                '''其他條件\n{other_condition}''',
                '```',
            )) + self.SEP_ENTRY
        )
