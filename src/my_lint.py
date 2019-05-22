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

class WhileVisitor(ast.NodeVisitor):

    
    def __init__(self):
        self._is_suspicious = False

        
    def visit_While(self, node):
        print("=> WHILE")
        # look for the variable in the comparison
        if isinstance(node.test, ast.Compare):
            op = node.test.ops[0]
            var_name = None
            print("\toperator : {}".format(op))
            if isinstance(op, _ast.Lt) or isinstance(op, _ast.LtE):
                # var {< | <=} var'
                var_name = node.test.left.id
            else:
                # var {> | >=} var'
                var_name = node.test.comparators[0].id
        else:
            return
        print("\tvar_name : {}".format(var_name))
        body_visitor = WhileBodyVisitor(var_name)
        body_visitor.visit(node)
        self._is_suspicious = 0 < body_visitor.get_cpt() <= 3 \
          and body_visitor.get_in_slice
        print("{")
        print("\tname : {}".format(body_visitor.get_var_name()))
        print("\tcpt : {}".format(body_visitor.get_cpt()))
        print("\tin_slice : {}".format(body_visitor.get_in_slice()))
        print("}")
        print("<= WHILE")

    def is_suspicious(self):
        return self._is_suspicious
        
class WhileBodyVisitor(ast.NodeVisitor):

    def __init__(self, var_name):
        ast.NodeVisitor.__init__(self)
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


    def _is_var_name(self, name):
        res = self._var_name == name
        print("| _is_var_name({}) -> {}".format(name, res))
        return res


    def visit_AugAssign(self, node):
        print("| visit_AugAssign, l. {}".format(node.lineno))
        self.generic_visit(node)


    def visit_Assign(self, node):
        print("| visit_Assign, l. {}".format(node.lineno))
        self.generic_visit(node)


    def visit_Index(self, node):
        print("| visit_Index")
        if isinstance(node.value, ast.Name):
            if self._is_var_name(node.value.id):
                self._in_slice = True
        else:
            self.generic_visit(node)
        

    def visit_Name(self, node):
        """
        ast.Name(id, ctx)
        """
        print("| visit_Name, l. {}".format(node.lineno))
        if self._is_var_name(node.id):
            self._incr_cpt()
        

    def visit_Attribute(self, node):
        print("| visit_Attribute, l. {}".format(node.lineno))
        if self._is_var_name(node.attr):
            self._incr_cpt()
        

    def visit_Num(self, node):
        print("| visit_Num, l. {}".format(node.lineno))
        if self._is_var_name(node.n):
            self._incr_cpt()
    

class map_modification(ast.NodeVisitor):

    self._data_structures = {"set", "list", "dict"}

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            # J'ai choisi d'itérer sur node.args pour le
            # moment mais il faudra trouver un moyen d'acceder
            # directement à un élément
            if node.func.id == "list":
                for elt in node.args:
                    if isinstance(elt, ast.Call):
                        if elt.func.id == "map":
                            print("Use comprehension instead !")
            return
                        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to check",
                        type=str)

    args = parser.parse_args()
    tree = None
    with open(args.filename, "r") as stream:
        tree = ast.parse(stream.read())
    # tree = ast.parse(fct)
    if tree is None:
        return
    check = WhileVisitor()
    check.visit(tree)
    if check.is_suspicious():
        print("SUSPICIOUS ITERATION")
    check = map_modification()
    check.visit(tree)
    
        
if __name__ == '__main__':
    main()
