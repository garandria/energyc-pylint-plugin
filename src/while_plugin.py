import astroid
import ast
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker



class while_iteration_checker(BaseChecker):
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


    def visit_while(self, node):
        var_name = None
        if isinstance(node.test, astroid.Compare):
            op = node.test.ops[0]
            if op == '<' or op == '<=':
                var_name = node.test.left.name
            else:
                var_name = node.test.ops[0][1].name
        else:
            return
        # body_visitor = while_body_visitor(var_name)
        # body_visitor.visit(node)
        # if self._is_suspicious(body_visitor):
        #     self.add_message(
        #         'suspicious iteration', node=node,
        #         )
        self.add_message(
            'suspicious iteration', node=node,
            )

    def _is_suspicious(self, visitor):
        return 0 <  visitor.get_cpt() <= 3 and visitor._var_in_slice()

class while_body_visitor(BaseChecker):

    def __init__(self, var_name):
        self._var_name = var_name
        self._cpt = 0
        self._in_slice = False


    def get_var_name(self):
        return self._var_name


    def get_cpt(self):
        return self._cpt


    def get_in_slice(self):
        return self._in_slice

    
    def _incr_cpt(self):
        self._cpt += 1
        print("| cpt ++")

    def visit_Index(self, node):
        if isinstance(node.value, ast.Name):
            if self._is_var_name(node.value.id):
                self._in_slice = True
        return
    
# class while_body_visitor(ast.NodeVisitor):

#     def __init__(self, var_name):
#         ast.NodeVisitor.__init__(self)
#         self._var_name = var_name
#         self._cpt = 0
#         self._in_slice = False
        
        
#     def get_var_name(self):
#         return self._var_name


#     def get_cpt(self):
#         return self._cpt


#     def get_in_slice(self):
#         return self._in_slice

        
#     def _incr_cpt(self):
#         self._cpt += 1
#         print("| cpt ++")


#     def _is_var_name(self, name):
#         res = self._var_name == name
#         print("| _is_var_name({}) -> {}".format(name, res))
#         return res


#     def visit_AugAssign(self, node):
#         print("| visit_AugAssign, l. {}".format(node.lineno))
#         self.generic_visit(node)


#     def visit_Assign(self, node):
#         print("| visit_Assign, l. {}".format(node.lineno))
#         self.generic_visit(node)


#     def visit_Index(self, node):
#         print("| visit_Index")
#         if isinstance(node.value, ast.Name):
#             if self._is_var_name(node.value.id):
#                 self._in_slice = True
#         else:
#             self.generic_visit(node)
        

#     def visit_Name(self, node):
#         """
#         ast.Name(id, ctx)
#         """
#         print("| visit_Name, l. {}".format(node.lineno))
#         if self._is_var_name(node.id):
#             self._incr_cpt()
        

#     def visit_Attribute(self, node):
#         print("| visit_Attribute, l. {}".format(node.lineno))
#         if self._is_var_name(node.attr):
#             self._incr_cpt()
        

#     def visit_Num(self, node):
#         print("| visit_Num, l. {}".format(node.lineno))
#         if self._is_var_name(node.n):
#             self._incr_cpt()


def register(linter):
    linter.register_checker(WhileIterationChecker(linter))
        
