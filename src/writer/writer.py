from pathlib import Path


class Writer:
    SEP_ENTRY = '\n' * 2

    def __init__(self, output_path: Path, formatter):
        self.output_path = output_path
        self.formatter = formatter

    def sort_key(self, entry: dict):
        return 0

    def write(self, entries: list):
        string = ''
        for entry in sorted(entries, key=self.sort_key):
            string += self.formatter.format(**entry)
        Path.mkdir((self.output_path).parent, parents=True, exist_ok=True)
        with open(self.output_path, 'w') as f:
            f.write(string)


class MarkdownWriter(Writer):
    def __init__(self, output_path: Path, formatter):
        if not str(output_path).endswith('.md'):
            output_path = Path(f'{output_path}.md')
        super().__init__(output_path, formatter)
