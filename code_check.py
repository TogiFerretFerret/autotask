import ast
def is_valid_python(code):
   try:
       ast.parse(code)
   except SyntaxError:
       return False
   return True
