from jinja2 import Template
from python_terraform import Terraform
import time

TF_FAILED = -1


def build_tf_file(ami: str, region: str, availability_zone: str, instance_type: str, load_balancer_name: str):
    """
    create a rendered template for main.tf file for terraform build process
    """
    
    # create a template for main.tf file
    terraform_template = """
    provider "aws" {
      region = "{{ region }}"
    }

    resource "aws_instance" "web_server" {
      ami = "{{ ami }}"
      instance_type = "{{ instance_type }}"
      availability_zone = "{{ availability_zone }}"
      subnet_id         = aws_subnet.public[0].id

      tags = {
        Name = "WebServer"
      }
    }

    resource "aws_lb" "application_lb" {
      name               = "{{ load_balancer_name }}"
      internal           = false
      load_balancer_type = "application"
      security_groups    = [aws_security_group.lb_sg.id]
      subnets            = aws_subnet.public[*].id
    }

    resource "aws_security_group" "lb_sg" {
      name        = "lb_security_group_unique"
      description = "Allow HTTP inbound traffic"

      ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      }
    }

    resource "aws_lb_listener" "http_listener" {
      load_balancer_arn = aws_lb.application_lb.arn
      port              = 80
      protocol          = "HTTP"

      default_action {
        type             = "forward"
        target_group_arn = aws_lb_target_group.web_target_group.arn
      }
    }

    resource "aws_lb_target_group" "web_target_group" {
      name     = "web-target-group-unique"
      port     = 80
      protocol = "HTTP"
      vpc_id   = aws_vpc.main.id
    }

    resource "aws_lb_target_group_attachment" "web_instance_attachment" {
      target_group_arn = aws_lb_target_group.web_target_group.arn
      target_id        = aws_instance.web_server.id
    }

    resource "aws_subnet" "public" {
      count            = 2
      vpc_id          = aws_vpc.main.id
      cidr_block      = "10.0.${count.index}.0/24"
      availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
    }

    resource "aws_vpc" "main" {
      cidr_block = "10.0.0.0/16"
    }

    output "instance_id" {
      value = aws_instance.web_server.id
    }

    output "load_balancer_dns" {
      value = aws_lb.application_lb.dns_name
    }
    """

    # render the template
    template = Template(terraform_template)
    rendered_template = template.render(
        ami=ami,
        region=region,
        availability_zone=availability_zone,
        instance_type=instance_type,
        load_balancer_name=load_balancer_name
    )

    return rendered_template


def run_terraform():
    terraform = Terraform(working_dir=".")

    # initialize
    print("\nInitializing Terraform...")
    return_code, stdout, stderr = terraform.init()
    print(stdout)
    if return_code == 1:
        print(stderr)
        terraform.destroy(skip_plan=True)
        return TF_FAILED

    # plan execution
    print("\nPlanning Terraform deployment...")
    return_code, stdout, stderr = terraform.plan()
    print(stdout)
    if return_code == 1:
        print(stderr)
        terraform.destroy(skip_plan=True)
        return TF_FAILED

    # apply deployment
    print("\nApplying Terraform...")
    return_code, stdout, stderr = terraform.apply(skip_plan=True)
    print(stdout)
    if return_code == 1:
        print(stderr)
        terraform.destroy(skip_plan=True)
        return TF_FAILED

    # capture instance id and alb dns name from outputs values
    print("\nFetching Terraform outputs...")
    return_code, output, stderr = terraform.output()
    if return_code == 0:
        print("Terraform Outputs:", output)
        instance_id = output.get("instance_id", {}).get("value", "N/A")
        load_balancer_dns = output.get("load_balancer_dns", {}).get("value", "N/A")
        return instance_id, load_balancer_dns
    else:
        print(stderr)
        terraform.destroy(skip_plan=True)
        return TF_FAILED


def mock_details():
  """
  mock instance id and alb dns name
  """
  return "instance_ip", "lb-dns-name"
