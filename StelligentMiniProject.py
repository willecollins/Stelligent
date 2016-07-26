import sys
import boto3
import botocore

# Initialize variables from command line

MyStackName = str(sys.argv[1])
TemplatePath = str(sys.argv[2])
OpsWorksTemplatePath = str(sys.argv[3])
RegionName = str(sys.argv[4])




#Hard-coded variables - to be changed in next version

NatInstanceType = "t1.small"
Parameters = "[{'ParameterKey': 'NATInstanceType', 'ParameterValue: 't1.micro']"
tagdict = ""

#Upload Template to S3

#Hard coded Random Bucknet Name
BucketName = "dkr4543kd3---mini-project"
s3=boto3.resource('s3')

#Create the bucket if it doesn't already exist

try:
    s3.meta.client.head_bucket(Bucket='mybucket')
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False
    s3.create_bucket(Bucket=BucketName)
#Cloud Formation Template
s3.Bucket(BucketName).upload_file(TemplatePath, 'MyTemplate')
#OpsWorks Template
s3.Bucket(BucketName).upload_file(OpsWorksTemplatePath, 'OpsWorksTemplate')

#Create TemplateURL for Cloudformation stack
MyTemplateURL = "https://s3" + ".amazonaws.com/" + BucketName + "/MyTemplate"

#CreateTemplateURL for OpsWorks stack
OpsWorksTemplateURL = "https://s3"  + ".amazonaws.com/" + BucketName + "/OpsWorksTemplate"


#Create a Cloud Formation Connection
Client = boto3.client(service_name='cloudformation', region_name=RegionName)


#Check to see if Stack Already Exists


#try:
stackID = Client.create_stack(
 		   StackName=MyStackName,
 		   # template_body=json,
 		   TemplateURL=MyTemplateURL,
 		   #Parameters=Parameters,
 		   DisableRollback=False,
 		   TimeoutInMinutes=30,
 		   #Capabilities=None,
 		   #Tags=tagdict
 		)

#Wait Until Stack is complete
waiter = Client.get_waiter('stack_create_complete')
waiter.wait(StackName=MyStackName)

#Get Information about the newly created stack
cloudformation = boto3.resource('cloudformation')
stack = cloudformation.Stack(MyStackName)
outputs = stack.outputs

#Set Values to pass to Next stack
for dict in outputs:

     if dict['OutputKey'] == 'PrivateSubnets':
             PrivateSubnet = dict['OutputValue']
     elif dict['OutputKey'] == 'PublicSubnets':
             PublicSubnet = dict['OutputValue']
     elif (dict['OutputKey']) == 'VPC':
             VPCId = dict['OutputValue']
     elif (dict['OutputKey']) == 'LoadBalancer':
            LoadBalancer = dict['OutputValue']

 #Iterate Through List and get the


print ('first part complete')
#except Exception as e:




#Create Opsworks Stack
#try:
myParam = [{"ParameterKey": "VPCId", "ParameterValue":  VPCId}, {"ParameterKey": "PublicSubnets","ParameterValue": PublicSubnet},
           { "ParameterKey": "DefSubnet", "ParameterValue": PublicSubnet}]

stackID2 = Client.create_stack(
 		   StackName='OpsWorksTestStack',
 		   # template_body=json,
 		   TemplateURL=OpsWorksTemplateURL,
 		   Parameters=myParam,
 		   DisableRollback=False,
 		   TimeoutInMinutes=30,
		   Capabilities=['CAPABILITY_IAM']
           #Tags=tagdict

 		)
#     #events = Client.describe_stack_events( stackID, None )