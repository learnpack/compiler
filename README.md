# Small Compiler SDK using docker

This is a really small and fast library to compile any script.

1. You need to have docker server running in your environment. 
2. Only supports the `python` language in the `latest` version.
3. Its very easy to add support for new languages by adding a the dockerfile to the `./environments` folder.

## How to use it?

There is two ways, you can run the SDK and import it in your code, or you can deploy it as an API and sent the code as HTTP request.

Just import the class "Compiler" into your code, here is an example that you can run with `pipenv run compile`:

```py
from src.compiler import Compiler

# Create a new compiler and specify python version
compiler = Compiler(lang="python:latest")

compiler.append(script="""
age = input('What is your age?')
print("Your age is", age)
""")

compiler.set_stdin(inputs=[34])

compilation_result = compiler.run()

print(compilation_result.stdout)
```

## Compilation API

Start the compilation API with `pipenv run start`.

Send a POST HTTP request with the `stdin` and the script `body` to compile, keep in mind than the `body` has to be base64 encoded first.

```
curl --location --request POST 'https://your-api-host.com/v1/compile' \
--header 'Content-Type: application/json' \
--data-raw '{
    "stdin": [45],
    "body": "cHJpbnQoIkhlbGxvb28gbXkgZnJpZW5kIik="
}'
```
