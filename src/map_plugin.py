import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class map_modification(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'map-modification'
    priority = -3
    msgs = {
        'R6666': (
            'Modify the data structure with a map.',
            'map-modification',
            'Use comprehension instead.'
        ),
    }
    options = (
        (
            'ignore-ints',
            {
                'default': False, 'type': 'yn', 'metavar' : '<y_or_n>',
                'help': 'Allow using map instead of comprehension',
            }
        ),
    )
    
    def __init__(self, linter=None):
        super(map_modification, self).__init__(linter)
        self._ds_conversion = {'list', 'set'}
        

    def visit_call(self, node):
        if isinstance(node.func, astroid.Name) \
          and node.func.name in self._ds_conversion:
            if node.args and node.args[0].func.name == 'map':
                self.add_message(
                    'map-modification',
                    node=node,
                    )
    
def register(linter):
    linter.register_checker(map_modification(linter))
