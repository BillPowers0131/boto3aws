from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import EC2Client


def main():
    # Create VPC
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()

    print('VPC created' + str(vpc_response))

    # Add name tag to VPC
    vpc_name = 'Boto3-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)

    print('Added ' + vpc_name + ' to ' + vpc_id)

    print('Creating an IGW')

    igw_response = vpc.create_internet_gateway()

    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # Create subnet in VPC

    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')

    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    print('Public subnet created for ' + vpc_id + ':' + str(public_subnet_response))

    # Create name tag for public subnet

    vpc.add_name_tag(public_subnet_id, 'Public-Subnet')

    # Create a public route table

    public_route_table_response = vpc.create_public_route_table(vpc_id)

    rtb_id = public_route_table_response['RouteTable']['RouteTableId']

    # Adding internet gateway to Public Route Table

    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)

    # Associate Public subnet with route table

    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

    # Allow auto-assign public ip address for subnet

    vpc.allow_auto_assign_public_ips_for_addresses(public_subnet_id)

    # Create a private Subnet

    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    print('Created private subnet ' + private_subnet_id + ' for VPC ' + vpc_id)

    # Add name tag to the private subnet

    vpc.add_name_tag(private_subnet_id, 'Private-Subnet')

    # Adding key pair

    ec2 = EC2(ec2_client)

    key_pair_name = 'Boto3-keypair'
    key_pair_response = ec2.create_key_par(key_pair_name)

    print('Created key pair with ' + key_pair_name + 'as well as ' + str(key_pair_response))

    # create a security group
    public_security_group_name = 'Boto-Public-SG'
    public_security_group_description = 'Security for Public Subnet'
    public_security_group_response = ec2.create_security_group(public_security_group_name,
                                                               public_security_group_description, vpc_id)
    public_security_group_response['GroupId']

    public_security_group_id = public_security_group_response['GroupId']
    # add public access to security group

    ec2.add_inbound_method_to_sg(public_security_group_id)

    print('Added public access rule to security group')

    ami_id = 'ami-00068cd7555f543d5'

    user_data = """#!/bin/bash
                    yum update -y
                    yum install httpd -y
                    service httpd start
                    chkconfig httpd on
                    echo "<html><body><h1>Hello from <b>Boto3</b> using Python!</h1></body></html>" > /var/www/html/index.html"""

    # launch a public EC2 instance

    ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, public_security_group_id, public_subnet_id, user_data)

    print('Launching public EC2 instance.')

    # Adding another security group for a private EC2 instance

    private_security_group_name = 'Boto3-Private-SG'
    private_security_group_description = 'Private security group for Private Subnet'
    private_security_group_response = ec2.create_security_group(private_security_group_name,
    private_security_group_description, vpc_id)
    private_security_group_response['GroupId']

    private_security_group_id = private_security_group_response['GroupId']

    # launch a private EC2 instance

    ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, private_security_group_id, private_subnet_id, """""")


if __name__ == '__main__':
    main()
