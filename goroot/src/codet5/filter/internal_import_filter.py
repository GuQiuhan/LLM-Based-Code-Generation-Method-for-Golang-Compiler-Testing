from go_tree_sitter.go_tree_sitter_tool import GoTreeSitterTool


class InternalImportFilter:

    @staticmethod
    def do_filter(node):
        flag = False
        import_specs = GoTreeSitterTool.get_import_spec(node)

        for import_spec in import_specs:
            path = import_spec.text.decode("utf8")
            flag |= ("internal" in path)

            if flag:
                break

        return flag
