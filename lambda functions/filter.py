import json


THRESHOLD = .88


def lambda_handler(event, context):

    inferences = event['body']['inferences']

    meets_threshold = any([x > THRESHOLD for x in inferences]) 

    if meets_threshold:
        pass
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }