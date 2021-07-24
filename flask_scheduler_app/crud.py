from settings import *
import boto3
import json
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
)
events_client = boto3.client(
    'events',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
)
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
)

lambda_name = "schedule_ec2_instances"

fn_arn = "arn:aws:lambda:ap-south-1:739746980233:function:schedule_ec2_instances"

def configure_rule(rule_name, cron, status, instance):
    rule_res = events_client.put_rule(
        Name=rule_name,
        ScheduleExpression='cron({})'.format(cron),
        State='ENABLED',
    )
    lambda_client.add_permission(
        FunctionName=lambda_name,
        StatementId="{0}-Event".format(rule_name),
        Action='lambda:InvokeFunction',
        Principal='events.amazonaws.com',
        SourceArn=rule_res['RuleArn'],
    )
    input_json = {
        "status": status,
        "instance": instance
    }
    events_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': "target_"+rule_name+"_1234",
                'Arn': fn_arn,
                'Input': json.dumps(input_json),
            },
        ]
    )

def create_rule(schedule_name, instance, days, status):
    total_days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    incoming_days = days
    in_cron_days = ",".join(incoming_days)
    remaining_days = list(set(total_days) - set(incoming_days))
    rem_cron_days = ",".join(remaining_days)

    rule_name_start = schedule_name + "_start"
    rule_name_stop = schedule_name + "_stop"

    existing_rules = events_client.list_rules()
    for rule in existing_rules['Rules']:
        if rule['Name'] == rule_name_start or rule['Name'] == rule_name_stop:
            return "Schedule name already used. Use different name"

    if status == 'start':
        cron = "0/5 * ? * {} *".format(in_cron_days)
        configure_rule(rule_name_start, cron, status, instance)
        if len(remaining_days) > 0:
            cron = "* * ? * {} *".format(rem_cron_days)
            status = 'stop'
            configure_rule(rule_name_stop, cron, status, instance)
        if 'id' in instance:
            response = ec2_client.create_tags(
                DryRun=False,
                Resources=[instance['id']],
                Tags=[
                    {
                        'Key': 'Scheduled',
                        'Value': 'True'
                    },
                ]
            )
        if 'key_tag' in instance and 'value_tag' in instance:
            reservations =   ec2_client.describe_instances(
                Filters=[{'Name': instance['key_tag'], 'Values': [instance['value_tag']]}])["Reservations"]
            for reservation in reservations :
                for each_instance in reservation["Instances"]:
                    ec2_client.create_tags(
                        Resources = [each_instance["InstanceId"] ],
                        Tags=[
                            {
                                'Key': 'Scheduled',
                                'Value': 'True'
                            },
                        ]
                    )
        return "schedule is created"
    elif status == 'stop':
        cron = "* * ? * {} *".format(in_cron_days)
        configure_rule(rule_name_stop, cron, status, instance)
        if len(remaining_days) > 0:
            cron = "* * ? * {} *".format(rem_cron_days)
            status = 'start'
            configure_rule(rule_name_start, cron, status, instance)
        if 'id' in instance:
            response = ec2_client.create_tags(
                DryRun=False,
                Resources=[instance['id']],
                Tags=[
                    {
                        'Key': 'Scheduled',
                        'Value': 'True'
                    },
                ]
            )
        if 'key_tag' in instance and 'value_tag' in instance:
            reservations =   ec2_client.describe_instances(
                Filters=[{'Name': instance['key_tag'], 'Values': [instance['value_tag']]}])["Reservations"]
            for reservation in reservations :
                for each_instance in reservation["Instances"]:
                    ec2_client.create_tags(
                        Resources = [each_instance["InstanceId"]],
                        Tags=[
                            {
                                'Key': 'Scheduled',
                                'Value': 'True'
                            },
                        ]
                    )
        return "schedule is created"
    else:
        return "status can only be either start or stop."


def update_rule(schedule_name, instance, days, status):
    total_days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    incoming_days = days
    in_cron_days = ",".join(incoming_days)
    remaining_days = list(set(total_days) - set(incoming_days))
    rem_cron_days = ",".join(remaining_days)

    existing_rules = events_client.list_rules()
    
    rule_name_start = schedule_name + "_start"
    rule_name_stop = schedule_name + "_stop"
    if status == 'start':
        cron = "* * ? * {} *".format(in_cron_days)
        for rule in existing_rules['Rules']:
            if rule['Name'] == rule_name_start:
                rule_res = events_client.put_rule(
                    Name=rule_name_start,
                    ScheduleExpression='cron({})'.format(cron),
                    State='ENABLED',
                )
                if len(remaining_days) > 0:
                    cron = "* * ? * {} *".format(rem_cron_days)
                    status = 'stop'
                    try:
                        rule_res = events_client.put_rule(
                            Name=rule_name_stop,
                            ScheduleExpression='cron({})'.format(cron),
                            State='ENABLED',
                        )
                    except Exception:
                        pass
        return "schedule is updated"
    elif status == 'stop':
        cron = "* * ? * {} *".format(in_cron_days)
        for rule in existing_rules['Rules']:
            if rule['Name'] == rule_name_stop:
                rule_res = events_client.put_rule(
                    Name=rule_name_stop,
                    ScheduleExpression='cron({})'.format(cron),
                    State='ENABLED',
                )
                if len(remaining_days) > 0:
                    cron = "* * ? * {} *".format(rem_cron_days)
                    status = 'start'
                    try:
                        rule_res = events_client.put_rule(
                            Name=rule_name_start,
                            ScheduleExpression='cron({})'.format(cron),
                            State='ENABLED',
                        )
                    except Exception:
                        pass
        return "schedule is updated"
    else:
        return "status can only be either start or stop."


def delete_rule(schedule_name, instance):
    exists = 0
    existing_rules = events_client.list_rules()
    for name in existing_rules['Rules']:
        response = events_client.remove_targets(
            Rule=name['Name'],
            Ids=[
                "target_"+name['Name']+"_1234",
            ],
            Force=False
        )
        response = lambda_client.remove_permission(
            FunctionName=lambda_name,
            StatementId="{0}-Event".format(name['Name']),
        )
        response = events_client.delete_rule(
            Name=name['Name'],
            Force=True
        )
    print("rule deleted")
    if 'id' in instance:
        response = ec2_client.delete_tags(
            DryRun=False,
            Resources=[instance['id']],
            Tags=[
                {
                    'Key': 'Scheduled',
                    'Value': 'True'
                },
            ]
        )
    if 'key_tag' in instance and 'value_tag' in instance:
        reservations =   ec2_client.describe_instances(
            Filters=[{'Name': instance['key_tag'], 'Values': [instance['value_tag']]}])["Reservations"]
        for reservation in reservations :
            for each_instance in reservation["Instances"]:
                ec2_client.delete_tags(
                    Resources = [each_instance["InstanceId"]],
                    Tags=[
                        {
                            'Key': 'Scheduled',
                            'Value': 'True'
                        },
                    ]
                )
    return "Schedule deleted"


def fetch_schedules():
    res = events_client.list_rules()
    if 'Rules' in res:
        return res['Rules']
    else:
        return "No schedules"
