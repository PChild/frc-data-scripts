import gen
import base64
import requests

user = 'CHILDREPT0401'
token = gen.getFirstAPI()
base = user + ':' + token
authToken = base64.b64encode(base.encode())

serverBase = 'https://frc-api.firstinspires.org'