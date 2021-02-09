#EC2 Instance Class

class EC2Instance:
    def __init__(self, ec2, launch_template):

        self.ec2 = ec2
        self.launch_template = launch_template

        self.instance = None
        self.instance_id = None
        self.public_dns = None

    def start_instance(self):
        self.instance = self.ec2.create_instances(LaunchTemplate=self.launch_template, MinCount=1, MaxCount=1)
        self.instance = self.instance[0]

    def terminate_instance(self):
        self.instance.terminate()

    def update_info(self):
        self.instance.wait_until_running()
        self.instance.reload()
        self.instance_id = self.instance.instance_id
        self.public_dns = self.instance.public_dns_name

