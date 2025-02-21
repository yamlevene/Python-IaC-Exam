from user_input import *
from tf_creation import build_tf_file


if __name__ == '__main__':
    print("Hello there! I need some information from you. lets begin:")
    ami = request_ami()
    instance_type = request_instance_type()
    region, av_zone = request_availability_zone()
    alb_name = request_alb_name()
    tf_file = build_tf_file(ami, region, av_zone, instance_type, alb_name)
