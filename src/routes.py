from flask import Flask, request, jsonify, url_for, Blueprint
from .utils import APIException
from .compiler import Compiler
import base64

api = Blueprint('v1', __name__)


@api.route("/compile", methods=['POST'])
def run_code():

    payload = request.json

    body = None
    if "body" not in payload:
        raise APIException("Missing body attribute on the request payload")

    body = base64.b64decode(request.json['body']).decode("utf-8")

    _stdin = []
    if "stdin" in payload:
        if not isinstance(payload['stdin'], list):
            raise APIException("Stdin Attribute must be a list of inputs")
        else:
            _stdin = payload['stdin']

    compiler = Compiler(lang="python:latest")
    compiler.append(script=body)
    compiler.set_stdin(inputs=_stdin)
    result = compiler.run().to_dict()

    if result["stdout"] is not None:
        result["stdout"] = str(base64.b64encode(
            result["stdout"].encode('utf-8')).decode('utf-8'))

    return result
