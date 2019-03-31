
from __future__ import unicode_literals
import sys
import os
from six.moves import cStringIO
import ast
import six
import re

def dump(tree):
    v = cStringIO()
    Printer(file=v).visit(tree)
    return v.getvalue()

Terminal = ["For","If","FunctionDef","Call","Assign","Import","While","ImportFrom","Return","AnnAssign","AugAssign","ExceptHandler","IfExp"]
nonTerminal = ["BinOp","Compare","UnaryOp","Expr","Subscript","Attribute","BoolOp","GeneratorExp"]

class Printer(ast.NodeVisitor):
    def __init__(self, file=sys.stdout, indent=" "):
        self.indentation = 0
        self.indent_with = indent
        self.f = file
    def visit(self, node):
        super(Printer, self).visit(node)
    def write(self, text):
        self.f.write(six.text_type(text))
    def generic_visit(self, node):
        if isinstance(node, list):
            nodestart = ""
            nodeend = ""
            children = [("", child) for child in node]
        else:
            if type(node).__name__ in Terminal:
                # nodestart = type(node).__name__+"_stmt" + "\n"+self.indent_with*(self.indentation+1) +"T "+type(node).__name__ + " " + str(getattr(node,'lineno'))
                nodestart = type(node).__name__+"_stmt" + "\n"+str(self.indentation+1) +" T "+type(node).__name__ + " " + str(getattr(node,'lineno'))
            elif hasattr(node,'lineno') and type(node).__name__ not in nonTerminal:
                nodestart = "T "+type(node).__name__ + " " + str(getattr(node,'lineno'))
            else:
                nodestart = type(node).__name__ + ""
            nodeend = ""
            children = [(name+" ", value) for name, value in ast.iter_fields(node)]

        if len(children) >= 1:
            self.indentation += 1

        self.write(nodestart)
        for i, pair in enumerate(children):
            attr, child = pair
            if isinstance(child, (ast.AST, list)) and child and len(children)>=1 and attr!="ctx ":
                self.write("\n" + str(self.indentation)+" ")
                # self.write("\n" + self.indentation * self.indent_with)
                self.write(attr)
                self.visit(child)
            else:
                if child and attr!="ctx ":
                    self.write(" "+repr(child))
                elif attr == "n " or attr=="value ":
                    self.write(" "+repr(child))

        self.write(nodeend)
        if len(children) >= 1:
            self.indentation -= 1

def pyAst(path):
    print("""
----------------------------------------------------------------------------------------------------
generating python abstract tree:
    """)
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1]=='.py'  and filename != 'temp.py':
            print("""
Dumping ast file: """+filename+"""
            """)
            file = open(path+'/'+filename, "r")
            source = file.read()
            root = ast.parse(source)
            output = open(path+'/'+os.path.splitext(filename)[0] + ".txt", "w")
            output.write("0 " + dump(root))
    print("""
Python abstract tree generated success.
    """)