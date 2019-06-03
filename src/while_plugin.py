import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker



class while_iteration_checker(BaseChecker):
    __implements__ = IAstroidChecker
    
    name = 'while-iteration'
    priority = -3
    msgs = {
        'R7777': (
            'Use a while to iterate over a Subscriptable.',   # displayed-message
            'while-iteration',                                # message-symbol
            'Avoid using a while to iterate over a Subscriptable, use for loop \
            instead'                         # message-help
        )        
    }
    # options = (
    #            'option-symbol': {'argparse-like-kwarg': 'value'},
    #            )
    options = (
        (
            'ignore-ints',
            {
                'default': False, 'type': 'yn', 'metavar' : '<y_or_n>',
                'help': 'Allow returning non-unique integers',
                }
                ),
                )

    def __init__(self, linter=None):
        super(while_iteration_checker, self).__init__(linter)
        self._in_while = False
        self._var_name = None
        self._cpt = 0
        self._in_slice = False
        

    def visit_while(self, node):
        self._in_while = True
        if self._var_name is None:
            if isinstance(node.test, astroid.Compare):
                op = node.test.ops[0][0]
                if op in {'<', '<='}:
                    self._var_name = node.test.left.name
                elif op in {'>', '>='}:
                    self._var_name = node.test.ops[0][1].Name                    

                    
    def leave_while(self, node):
        if self._is_suspicious():
            self.add_message(
                'while-iteration',
                node = node,
                )
        self._in_while = False
        self._var_name = None
        self._cpt = 0
        self._in_slice = False
            

    def _is_suspicious(self):
        return 0 <  self._cpt <= 3 and self._var_in_slice

    
    def _incr_cpt(self):
        self._cpt += 1
        

    def _is_var_name(self, name):
        return self._var_name == name
        

    def visit_augassign(self, node):
        if self._in_while:
            if node.op == '+=':
                if isinstance(node.target, astroid.AssignAttr):
                    if self._is_var_name(node.target.attrname):
                        self._incr_cpt()
                elif isinstance(node.target, astroid.AssignName):
                    if self._is_var_name(node.target.name):
                        self._incr_cpt()

                        
    def visit_subscript(self, node):
        if self._in_while:
            if isinstance(node.slice.value, astroid.Attribute):
                if self._is_var_name(node.slice.value.attrname):
                    self._var_in_slice = True
            elif isinstance(node.slice.value, astroid.Name):
                if self._is_var_name(node.slice.value.name):
                    self._var_in_slice = True

    
def register(linter):
    linter.register_checker(while_iteration_checker(linter))
        
