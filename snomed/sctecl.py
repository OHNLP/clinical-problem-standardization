# -*- coding: utf-8 -*-
'''
Utility for parsing SNOMED CT Expressions
'''

from antlr4 import *
from .ecl.ECLLexer import ECLLexer
from .ecl.ECLParser import ECLParser
from .ecl.ECLListener import ECLListener

def validate(expr):
    lexer = ECLLexer(InputStream(expr))

    constraints = [None, None]

    class PrintListener(ECLListener):
        def enterConceptid(self, ctx):
            constraints[0] = ctx.getText()
        def enterConstraintoperator(self, ctx):
            constraints[1] = ctx.getText()

    stream = CommonTokenStream(lexer)
    parser = ECLParser(stream)
    tree = parser.subexpressionconstraint()
    printer = PrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    if parser.getNumberOfSyntaxErrors() > 0:
        raise Exception

    return constraints

def do_parse(expr):
    constraints = []
    parts = expr.split(" OR ")
    for part in parts:
        constraints.append(validate(part))

    return constraints