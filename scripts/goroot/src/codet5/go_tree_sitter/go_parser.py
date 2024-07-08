from tree_sitter import Parser

from go_tree_sitter.go_language import GoLanguage


class GoParser:
    def __init__(self):
        self.parser = Parser()
        self.parser.set_language(GoLanguage.language)

    def parse(self, code):
        tree = self.parser.parse(bytes(code, 'utf8'))
        return tree.root_node
