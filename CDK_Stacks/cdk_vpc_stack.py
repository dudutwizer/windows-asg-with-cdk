from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class CdkVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(self, id, max_azs=2, cidr="10.10.0.0/16",
                            # This configuration will create 2 groups in 2 AZs = 4 subnets.
                            subnet_configuration=[
                                ec2.SubnetConfiguration(
                                    subnet_type=ec2.SubnetType.PUBLIC,
                                    name="Public",
                                    cidr_mask=24
                                    ), 
                                ec2.SubnetConfiguration(
                                    subnet_type=ec2.SubnetType.PRIVATE,
                                    name="Private",
                                    cidr_mask=24
                                    )
                                ],
                            nat_gateways=2,
                            )