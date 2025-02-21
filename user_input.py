from data import UBUNTU_AMI, AMAZON_LINUX_AMI, AV_ZONES, DEFAULT_AV_ZONE
import sys

EXIT_CODE = "0"
UBUNTU, AMAZON_LINUX = "1", "2"
T3_SMALL, T3_MEDIUM = "1", "2"


def suggest_exit():
    """
    allows user to exit
    """
    exit_input = input("do you want to exit? if so - press 0 and click enter, otherwise press any key ")
    if exit_input == EXIT_CODE:
        sys.exit(0)


def request_ami():
    """
    asks user to provide an ami
    """
    ami = None
    while ami is None:
        user_choice = input("Would you like Ubuntu (choose 1) or Amazon linux (choose 2)? 1/2: ")
        if user_choice == UBUNTU:
            ami = UBUNTU_AMI
        elif user_choice == AMAZON_LINUX:
            ami = AMAZON_LINUX_AMI
        else:
            print("you must choose 1 or 2 my dear friend")
            suggest_exit()
    return ami


def request_instance_type():
    """
    asks user to provide an instance type
    """
    instance_type = None
    while instance_type is None:
        user_choice = input("Would you like t3.small machine (choose 1) or t3.medium machine (choose 2)? 1/2: ")
        if user_choice == T3_SMALL:
            instance_type = "t3.small"
        elif user_choice == AMAZON_LINUX:
            instance_type = "t3.medium"
        else:
            print("you must choose 1 or 2 my dear friend")
            suggest_exit()
    return instance_type


def request_availability_zone():
    """
    asks user to provide an availability zone
    """
    user_choice = input("which availability zone would you prefer: ")
    try:
        region = AV_ZONES[user_choice]
        av_zone = user_choice
        return region, av_zone
    except KeyError as k_err:
        print(f"Sorry! we only support this availability zones at the moment:\n{list(AV_ZONES.keys())}")
        print(f"We'll forward you by default to {DEFAULT_AV_ZONE}")
        region = AV_ZONES[DEFAULT_AV_ZONE]
        av_zone = DEFAULT_AV_ZONE
        return region, av_zone


def request_alb_name():
    """
    asks user to provide a name for a load balancer
    """
    user_alb_name = None
    valid = False
    while not valid:
        user_choice = input("Name your ALB please: ")
        if user_choice == "":
            print("I can't work with an empty name!")
            suggest_exit()
        else:
            user_alb_name = user_choice
            valid = True
    return user_alb_name
