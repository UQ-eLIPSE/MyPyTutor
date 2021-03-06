class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.subscripts_with_value = False

    def visit_Subscript(self, node):
        super().visit_Subscript(node)

        if len(self.functions['get_value'].args) == 2:
            d, k = self.functions['get_value'].args

            if k in TutorialNodeVisitor.involved_identifiers(node.slice) \
                    and d == TutorialNodeVisitor.identifier(node.value):
                self.subscripts_with_value = True


class DictAnalyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['get_value'].is_defined:
            self.add_error('You need to define a get_value function')
        elif len(self.visitor.functions['get_value'].args) != 2:
            self.add_error('get_value must accept exactly two args')

        if not self.visitor.subscripts_with_value:
            self.add_error('You need to subscript the dictionary, eg d[k]')


ANALYSER = DictAnalyser(CodeVisitor)