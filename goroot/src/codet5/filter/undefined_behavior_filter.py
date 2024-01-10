from go_tree_sitter.go_tree_sitter_tool import GoTreeSitterTool


class UndefinedBehaviorFilter:

    @staticmethod
    def do_filter(node):
        return UndefinedBehaviorFilter.package_initialization(node) or \
            UndefinedBehaviorFilter.division_by_zero(node)

    @staticmethod
    def package_initialization(node):
        flag = False
        for child in node.children:
            if child.type == "var_declaration" or child.type == "short_var_declaration":
                flag |= GoTreeSitterTool.has_selector_expression(child)
            if flag:
                break

        return flag

    @staticmethod
    def division_by_zero(node):
        flag = False
        binary_expressions = GoTreeSitterTool.get_binary_expression(node)
        for binary_expression in binary_expressions:
            if "/" in [child.type for child in binary_expression.children]:
                right = binary_expression.child_by_field_name("right")
                if right.type == "int_literal":
                    s = right.text.decode("utf8")
                    if s.startswith("0x") or s.startswith("-0x"):
                        flag |= (int(s, 16) == 0)
                    else:
                        flag |= (int(s, 10) == 0)
                if right.type == "float_literal":
                    s = right.text.decode("utf8")
                    flag |= (float(s) == 0.0)
            if flag:
                break

        return flag
