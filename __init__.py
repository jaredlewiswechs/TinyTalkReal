"""
realTinyTalk — The Friendly Programming Language
"""

from .kernel import ExecutionBounds
from .lexer import Lexer
from .parser import Parser
from .runtime import Runtime


def run(code: str, bounds: ExecutionBounds = None) -> 'Value':
    """Convenience function: lex → parse → execute TinyTalk code."""
    if bounds is None:
        bounds = ExecutionBounds()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    rt = Runtime(bounds)
    return rt.execute(ast)


__all__ = ['run', 'ExecutionBounds', 'Lexer', 'Parser', 'Runtime']
