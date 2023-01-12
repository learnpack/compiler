import docker
import string
import random
import os
import subprocess
import textwrap


class CompilerException(Exception):
    pass


class CompilationResult():
    stdout = None
    exit_code = None

    def __init__(self, stdout=None, exit_code=None):
        self.stdout = stdout
        self.exit_code = exit_code

    def to_dict(self):
        return {
            "stdout": self.stdout.decode('utf-8') if not None else None,
            "exit_code": self.exit_code,
        }


class Compiler():
    cwd = None
    image_name = None
    local_codebase_path = None
    container_codebase_path = None
    script = None
    script_name = "script.py"
    stdin = None
    lang = None

    def __init__(self, lang=None):
        self.cwd = os.getcwd()
        self.lang = lang
        self.local_codebase_path = os.path.join(self.cwd, "codebase")
        self.container_codebase_path = "/codebase"

        if self.lang is None:
            raise CompilerException("Please provide compilation language")

        self.image_name = self.lang+"-"+self._random_word(10).lower()

    def _get_command(self):
        cmd = f"python {self.container_codebase_path}/{self.script_name}"
        # print("DEBUG: command ", cmd)
        return cmd

    def _random_word(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))

    def _get_volumes(self):
        _vol = {
            self.local_codebase_path: {
                'bind': self.container_codebase_path,
                'mode': 'rw'
            }
        }
        # print("Volumes: ", _vol)
        return _vol

    def _prepend_mock_inputs(self):
        with open(os.path.join(self.cwd, f"environments/{self.lang}/prepend.txt"), "r") as template:
            prepend_text = template.read().replace(
                "{% stdin %}", str(self.stdin))
            with open(os.path.join(self.local_codebase_path, self.script_name), "r") as original:
                original_data = original.read()
            with open(os.path.join(self.local_codebase_path, self.script_name), "w") as modified:
                modified.write(prepend_text + original_data)

    def append(self, script=None):
        if script is not None:
            self.script = script
            self._render_script()

    def _render_script(self):
        with open(os.path.join(self.local_codebase_path, self.script_name), 'w') as f:
            f.write(self.script)

        if self.stdin and len(self.stdin) > 0:
            self._prepend_mock_inputs()

    def set_stdin(self, inputs=[]):

        if self.script is None:
            raise CompilerException(
                "Please specify the script content before adding stdin")

        if not isinstance(inputs, list):
            raise CompilerException(
                "Stdin must be a list of values to be inputed into the script")

        if len(inputs) > 0:
            self.stdin = inputs
            self._render_script()

    def run(self):

        kwargs = {"detach": True}
        client = docker.from_env()

        # create image
        dockerfile_path = os.path.join(self.cwd, 'environments/'+self.lang)
        image = client.images.build(path=dockerfile_path, tag=self.image_name)

        # print("Running container with the following config", kwargs)
        container = client.containers.run(
            self.image_name,  # The image to use
            self._get_command(),  # The command to run the script
            volumes=self._get_volumes(),
            **kwargs,
        )

        # Wait for the container to finish running
        exit_code = container.wait()
        # print(f"Finished running with exit_code: {str(exit_code)}")

        # Print the container logs
        return CompilationResult(
            exit_code=exit_code,
            stdout=container.logs()
        )
