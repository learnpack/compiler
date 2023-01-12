from src.compiler import Compiler

compiler = Compiler(lang="python:latest")
compiler.append(script="""
age = input('What is your age?')
print("Your age is", age)
""")
compiler.set_stdin(inputs=[34])
compilation_result = compiler.run()
print(compilation_result.stdout)
