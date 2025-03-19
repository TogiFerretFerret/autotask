import ast
def is_valid_python(code):
   try:
       ast.parse(code)
   except SyntaxError:
       return False
   return True

import platform

def is_macos():
    return platform.system() == "Darwin"
