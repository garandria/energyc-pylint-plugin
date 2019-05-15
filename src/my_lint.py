import ast
import _ast
import argparse

fct = """
def iteration():
    l = list(range(100))
    k = len(l)
    i = 0
    e = list()
    while i < k:
        e.append(l[i])
        i += 1
"""

class WhileCheck (ast.NodeVisitor):

    def __init__(self):
        self._op = None
        self._var_name = None
        self._cpt = 0


    def visit_FunctionDef(self, node):
        print("| visit_FunctionDef, l.", node.lineno)
        print("| => FUNC :", node.name)
        self.generic_visit(node)
        print("| <= FUNC :", node.name)

        
    def visit_While(self, node):
        print("| visit_While, l.", node.lineno)
        self._show_fields(node)
        if isinstance(node.test, ast.Compare):
            self._op = node.test.ops[0]
            print("| op ->", self._op)
            if isinstance(self._op, _ast.Lt) or isinstance(self._op, _ast.LtE):
                # var {< | <=} var'
                self._var_name = node.test.left.id
            else:
                # var' {> | >=} var
                self._var_name = node.test.comparators[0].id
            print("| var ->", self._var_name)
            self.generic_visit(node)

            
    def visit_AugAssign(self, node):
        print("| visit_AugAssign, l.", node.lineno)
        self._show_fields(node)
        print("| cpt ->", self._cpt)
        if isinstance(node.target, ast.Name):
            print("| ast.Name")
            if self._is_var_name(node.target.id):
                self._incr_cpt()
                print("| incr(cpt)")
            print("| cpt ->", self._cpt)
        # if node.target is an attribute (oop)
        if isinstance(node.target, ast.Attribute):
            print("| ast.Attribute")
            if self._is_var_name(node.target.value.id):
                self._incr_cpt()
                print("| incr(cpt)")
            print("| cpt ->", self._cpt)
                
            
    def visit_Assign(self, node):
        print("| visit_Assign, l.", node.lineno)
        self._show_fields(node)
        # node.targes contains ast.Attribute (oop)
        if len(node.targets) > 1:
            # ex : a = b = 1
            for name in node.targets:
                if isinstance(name, ast.Attribute):
                    if self._is_var_name(name.value.id):
                        self._incr_cpt()
                elif isinstance(name, ast.Name):
                    if self._is_var_name(name.id):
                        self._incr_cpt()
        else:
            if isinstance(node, ast.Tuple):
                # ex : a, b, c = d
                for name in node.targets.elts:
                    if self._is_var_name(name.id):
                        self._incr_cpt()
           

    def visit_Subscript(self, node):
        """
        """
        print("| visit_Subscript [")
        self.generic_visit(node)
        print("| ]_Subscript")

        
    def visit_Index(self, node):
        print("| visit_Index")
        self.generic_visit(node)
                             

    def visit_Name(self, node):
        """
        ast.Name(id, ctx)
        """
        print("| visit_Name, l.", node.lineno)
        if self._is_var_name(node.id):
            self._incr_cpt()

            
    def visit_Attribute(self, node):
        """
        ast.Attribute(value, attr, ctx)
        """
        print("| visit_Attribute, l.", node.lineno)
        self.generic_visit(node)


    def visit_Num(self, node):
        print("| visit_Num")
        if self._is_var_name(node.n):
            self._incr_cpt()

        
    # def visit_Tuple(self, node):
    #     """
    #     for this case :
    #     a, b, c = d
    #     in Assign
    #     actually a, b += d is not possible
    #     """
        
    
        
    def _is_var_name(self, name):
        return name == self._var_name
    
                        
    def _incr_cpt(self):
        self._cpt += 1

        
    def _show_fields(self, node):
        for fields in ast.iter_fields(node):
            print("|\t", fields[0], ':', fields[1:], end='\n')


    def get_cpt(self):
        return self._cpt
            

    def leave_While(self, node):
        print("LEAVING WHILE", node)
        
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to check",
                        type=str)
    args = parser.parse_args()
    tree = None
    with open(args.filename, "r") as stream:
        tree = ast.parse(stream.read())
    # tree = ast.parse(fct)
    check = WhileCheck()
    check.visit(tree)
    if check.get_cpt() > 0:
        print("Compteur :", check.get_cpt())

        
if __name__ == '__main__':
    main()
