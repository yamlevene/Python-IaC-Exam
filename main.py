import json
from user_input import *
from tf_creation import build_tf_file, run_terraform, mock_details, TF_FAILED
from validate_resources import validate_ec2_instance, validate_alb, VALIDATION_FAIL


if __name__ == '__main__':

    print("Hello there! I need some information from you. lets begin:")

    # get user inputs
    ami = request_ami()
    instance_type = request_instance_type()
    region, av_zone = request_availability_zone()
    alb_name = request_alb_name()
    tf_content = build_tf_file(ami, region, av_zone, instance_type, alb_name)

    # create tf file
    with open("main.tf", "w") as tf_file:
        tf_file.write(tf_content)

    print("Created Terraform configuration file - main.tf")
    print("Starting to run main.tf...")

    # build the resources
    build_output = run_terraform()
    if build_output == TF_FAILED:
        print("couldn't create resources, mocking values were given")
        instance_id, lb_dns_name = mock_details()
    else:
        print("resources were created successfuly")
        instance_id, lb_dns_name = build_output
    

    # Validate EC2 instance
    ec2_validation_output = validate_ec2_instance(instance_id)
    if ec2_validation_output == VALIDATION_FAIL:
        # mock values
        print("mocking EC2 instance details")
        instance_state, public_ip = "mocking state", "mocking_ip"
    else:
        instance_state, public_ip = validation_output
    
    # Validate ALB
    lb_validation_output = validate_alb(lb_dns_name)
    if lb_validation_output == VALIDATION_FAIL:
        # mock values
        print("mocking ALB details")
        lb_dns = "mocking DNS name"
    else:
        lb_dns = validation_output
    
    # Store the captured data in a JSON file
    validation_data = {
        "instance_id": instance_id,
        "instance_state": instance_state,
        "public_ip": public_ip,
        "load_balancer_dns": lb_dns
    }
    
    with open('aws_validation.json', 'w') as json_file:
        json.dump(validation_data, json_file, indent=4)

    print("Data saved to aws_validation.json")
