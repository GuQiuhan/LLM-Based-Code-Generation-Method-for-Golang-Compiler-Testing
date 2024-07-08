import re

from go_tree_sitter.go_language import GoLanguage


class GoTreeSitterTool:
    @staticmethod
    def get_function_declaration(node):
        query = """
        (function_declaration)@x
        (method_declaration)@x
        """

        captures = GoLanguage.use_query(query, node)
        return [elem[0] for elem in captures]

    @staticmethod
    def get_binary_expression(node):
        query = """
        (binary_expression)@x
        """

        captures = GoLanguage.use_query(query, node)
        return [elem[0] for elem in captures]

    @staticmethod
    def get_import_spec(node):
        query = """
        (import_spec)@x
        """

        captures = GoLanguage.use_query(query, node)
        return [elem[0] for elem in captures]

    def get_comment(node):
        query = """
        (comment)@x
        """

        captures = GoLanguage.use_query(query, node)
        return [elem[0] for elem in captures]

    @staticmethod
    def has_error(node):
        query = """
        (ERROR)@x
        """

        captures = GoLanguage.use_query(query, node)

        return len(captures) != 0

    @staticmethod
    def has_selector_expression(node):
        query = """
        (selector_expression)@x
        """
        captures = GoLanguage.use_query(query, node)

        return len(captures) != 0
