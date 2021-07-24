import boto3
import uuid
import json

id = uuid.uuid4()
SOME_ID = str(id).split('-')[0]

AWS_ACCESS_KEY_ID = 'AKIA2YPC3EGE6KRKKBLL'
AWS_SECRET_ACCESS_KEY = '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'

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
events_client = boto3.client(
    'events',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

lambda_name = "schedule_ec2_instances"

fn_arn = "arn:aws:lambda:ap-south-1:739746980233:function:schedule_ec2_instances"
cron = "0/7 * ? * SAT *"
rule_name = "start_schedule_v1"

# rule_res = events_client.put_rule(
#     Name=rule_name,
#     ScheduleExpression='cron({})'.format(cron),
#     State='ENABLED',
#     Tags=[
#         {
#             'Key': 'tag_in_put_rule',
#             'Value': 'value_in_put_rule'
#         },
#     ]
# )
# print("rule created")
# lambda_client.add_permission(
#     FunctionName=lambda_name,
#     StatementId="{0}-Event".format(rule_name),
#     Action='lambda:InvokeFunction',
#     Principal='events.amazonaws.com',
#     SourceArn=rule_res['RuleArn'],
# )
# print("permission added")
# input_json = {
#     "status": "start",
#     "instance": {
#         "id" : "123456"
#     }
# }
# events_client.put_targets(
#     Rule=rule_name,
#     Targets=[
#         {
#             'Id': "target_start",
#             'Arn': fn_arn,
#             'Input': json.dumps(input_json),
#         },
#     ]
# )
# print("target added")
# response = lambda_client.remove_permission(
#     FunctionName=lambda_name,
#     StatementId="{0}-Event".format(rule_name),
# )
# response = events_client.remove_targets(
#     Rule=rule_name,
#     Ids=[
#         'target_start',
#     ],
#     Force=False
# )

# response = events_client.delete_rule(
#     Name=rule_name,
#     Force=True
# )
# print("rule deleted")

response = events_client.list_rules()
print(response)

