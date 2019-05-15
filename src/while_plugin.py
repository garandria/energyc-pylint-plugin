import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class WhileIterationChecker(BaseChecker):
    __implements__ = IAstroidChecker

    
    name = 'while-iteration'
    priority = -10
    msgs = {
        'R77777': (
            'Use a while to iterate over a Subscriptable.',   # displayed-message
            'while-iteration',                                # message-symbol
            'Avoid using a while to iterate over a Subscriptable for energy \
            sake'                         # message-help
        )        
    }
    # options = (
    #            'option-symbol': {'argparse-like-kwarg': 'value'},
    #            )

    def __init__(self, linter=None):
        super(WhileIterationChecker, self).__init___(linter)
        self._stack = []


    def visit_while(self, node):
        if isinstance(node.test, astroid.Compare):
            self._cpt = 0
            self._in_slice = False
            self._var_name = None

    def visit_compare(self, node):
        op = node.ops[0][0]
        # node.ops is a list(Tuple(str | NodeNG))
        # TODO : while i < j < k :
        if isinstance(op, astroid.*Lt) or isinstance(op, astroid.LtE):
            self._var_name = node.test.left.id
        else:
            self._var_name = node.test.comparators[0].id

    def visit_augassign(self, node):
        self.generic_visit(node)

    def visit_assign(self, node):
        self.generic_visit(node)

    def visit_subscript(self, node):
        self.generic_visit(node)

    def visit_name(self, node):
        if self._is_var_name(node.name):
            self._incr_cpt()

    def visit_index(self, node):
        self.generic_visit(node)

    def _is_var_name(self, name):
        return self._var_name == name

    def _incr_cpt(self):
        self._cpt += 1
            
