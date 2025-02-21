import boto3
from botocore.exceptions import ClientError

VALIDATION_FAIL = -1

def validate_ec2_instance(instance_id):
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    
    try:
        # fetch EC2 instance details
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        
        # check if instance exists and is running
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']
        public_ip = instance.get('PublicIpAddress', 'N/A')

        if instance_state != 'running':
            print(f"Instance is not running. Current state: {instance_state}")
        
        return instance_state, public_ip
    
    except ClientError as c_err:
        print(f"Error validating EC2 instance: {c_err}")
        return VALIDATION_FAIL

def validate_alb(load_balancer_name):
    elbv2_client = boto3.client('elbv2', region_name='us-east-1')
    
    try:
        # fetch ALB details
        response = elbv2_client.describe_load_balancers(Names=[load_balancer_name])
        
        # check if ALB exists
        alb = response['LoadBalancers'][0]
        dns_name = alb['DNSName']
        
        return dns_name
    
    except ClientError as c_err:
        print(f"Error validating ALB: {c_err}")
        return VALIDATION_FAIL