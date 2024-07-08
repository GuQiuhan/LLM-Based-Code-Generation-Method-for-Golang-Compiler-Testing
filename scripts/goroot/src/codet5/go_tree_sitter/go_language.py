from tree_sitter import Language


class GoLanguage:
    PATH = "/bigdata/qiuhan/codet5/usage/goroot/src/codet5/resources/build/my-languages.so"

    language = Language(PATH, "go")

    @staticmethod
    def use_query(query, node):
        return GoLanguage.language.query(query).captures(node)
