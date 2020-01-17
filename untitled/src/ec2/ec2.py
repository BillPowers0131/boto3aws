

import datetime


class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2"""

    def create_key_pair(self,key_name):
        print('Creating key name')
        return self._client.create_key_pair(KeyName=key_name)

    def create_security_group(self,groupname,description,vpc_id):
        print('Creating a security group')
        return self._client.create_security_group(
            GroupName=groupname,
            Description=description,
            VpcId=vpc_id
        )

    def add_inbound_method_to_sg(self,security_group_id):
        print('Allowing inbound public access for public security group: ' + security_group_id)
        return self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]

        )

    def launch_ec2_instance(self,image_id,key_name,min_count,max_count,security_group_id,subnet_id,user_data):
        print('Launching ' + str(min_count) + ' EC2 instance(s).')
        return self._client.run_instances(
            ImageId=image_id,
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType='t2.micro',
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            UserData=user_data
        )

    def describe_ec2_instances(self):
        print('Describing EC2 instances.......')
        return self._client.describe_instances()

    def modify_ec2_instances(self,instance_id):
        print('Modifying instance ID: ' + instance_id)
        return self._client.modify_instance_attribute(
            InstanceId=instance_id,
            DisableApiTermination={"Value": False}
        )

    def stop_instance(self,instance_id):
         print('Stopping instance: ' + instance_id)
         return self._client.stop_instances(
             InstanceIds=[instance_id]
         )

    def start_instance(self,instance_id):
        print('Starting instance:' + instance_id)
        return self._client.start_instances(
            InstanceIds=[instance_id]
        )

    def terminate_instance(self,instance_id):
        print('Terminating instance: ' + instance_id)
        return self._client.terminate_instances(
            InstanceIds=[instance_id]
        )

    def create_image(self,instance_id):
        print('Taking a snapshot of ' + instance_id)
        snapshot_time = datetime.date.today()
        print(snapshot_time)
        return self._client.create_image(
           InstanceId=instance_id,
            Name=f'AMI Timestamp {snapshot_time}'
            )


