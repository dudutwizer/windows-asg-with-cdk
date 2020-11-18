from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_autoscaling as asg
import aws_cdk.aws_elasticloadbalancingv2 as lb

clean_windows_ami = ec2.MachineImage.latest_windows(version=ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE)  # Clean image
custom_ami = ec2.MachineImage.lookup(name= "dudu-asg-test") #Change it to your AMI

with open("./user_data/user_data_script.ps1") as f:
    user_data = f.read()

class WindowsAutoScaling(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, KeyPairName,ec2_type, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.role = iam.Role(self, id+'ec2-role',assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'))
        
        #Grant permission to access the SSM (To allow Session Manager)
        self.role.add_managed_policy(policy=iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))
        # Define Auto Scaling Group
        self.app_servers_asg = asg.AutoScalingGroup(self, id + " ASG", 
                                        instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                        machine_image=custom_ami,
                                        vpc=vpc,
                                        role=self.role,
                                        min_capacity=2,
                                        max_capacity=10,
                                        desired_capacity=10,
                                        vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                        user_data=ec2.UserData.custom(user_data)
                                        )
        self.app_servers_asg.scale_on_cpu_utilization('ScaleToCPU', target_utilization_percent= 70)


        # Define Load Balancer
        self.alb = lb.ApplicationLoadBalancer(self, id+ ' ALB', internet_facing=True, vpc=vpc)
        self.listener = self.alb.add_listener(id+' Listener', port= 80, open= True)
        self.listener.add_targets(id+' ApplicationFleet', port=80, targets=[self.app_servers_asg])
        
        core.CfnOutput(self, "Loadbalancer DNS Name",
                       value=self.alb.load_balancer_dns_name)
