#!/usr/bin/env python3

from aws_cdk import core

from CDK_Stacks.cdk_windows_autoscaling import WindowsAutoScaling
from CDK_Stacks.cdk_vpc_stack import CdkVpcStack
from params import MySecretParams ## Just a simple class to hide clear-text vars

env_EU = core.Environment(account=MySecretParams.accountID, region='eu-west-1')
stack_name = "ASG-POC"
KeyPairName = MySecretParams.KeyPairName # You will need to create it manually via the AWS Console
ec2_type = "t3.large"


app = core.App()
# First stack, VPC, 1 public and 1 private subnets in 2 AZs = 4 subnets.
vpc_stack = CdkVpcStack(app, stack_name+"-Infra", env=env_EU)

windows_servers = WindowsAutoScaling(app, "ASG-Test",
                                        vpc=vpc_stack.vpc, 
                                        KeyPairName=KeyPairName, 
                                        ec2_type=ec2_type,
                                        env=env_EU)

windows_servers.add_dependency(vpc_stack)

app.synth()
