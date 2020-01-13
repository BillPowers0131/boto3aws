
class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2"""

    def create_key_par(self,key_name):
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


