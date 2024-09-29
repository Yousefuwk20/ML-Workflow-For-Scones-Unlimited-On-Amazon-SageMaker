import json
import sagemaker
import base64
import os
from sagemaker.serializers import IdentitySerializer

ENDPOINT = os.environ['ENDPOINT']

def lambda_handler(event, context):

    image = base64.b64decode(event['body']['image_data'])

    predictor = sagemaker.predictor.Predictor(ENDPOINT) 

    predictor.serializer = IdentitySerializer("image/png")

    inferences = predictor.predict(image)

    event["body"]["inferences"] = json.loads(inferences)
    return {
        'statusCode': 200,
        'body': event['body']
    }