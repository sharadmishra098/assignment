import json
import boto3
ec2 = boto3.resource('ec2')
def lambda_handler(event, context):
    print("looging event")
    print(event)
    if event['status'] == "start":
        if "key_tag" in event['instance'] and "value_tag" in event['instance']:
            filters = [
                    {
                        'Name': 'tag:'+str(event['instance']['key_tag']),
                        'Values':[event['instance']['value_tag']]
                    }
                ]
            instances = ec2.instances.filter(Filters=filters)
            for instance in instances:
                instance.start()
        if 'id' in event['instance']:
            ec2.instances.filter(InstanceIds=[event['instance']['id']]).start()
    if event['status'] == "stop":
        if "key_tag" in event['instance'] and "value_tag" in event['instance']:
            filters = [
                    {
                        'Name': 'tag:'+str(event['instance']['key_tag']),
                        'Values':[event['instance']['value_tag']]
                    }
                ]
            instances = ec2.instances.filter(Filters=filters)
            for instance in instances:
                instance.stop()
        if 'id' in event['instance']:
            ec2.instances.filter(InstanceIds=[event['instance']['id']]).stop()
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
