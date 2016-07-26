Introduction

StelligentMiniProject.py is a python script that will perform the following actions:

1. Create a VPC via AWS Cloud Formation that contains an elastic load balancer, a public subnet, and a private subnet. 
2. Create an AWS Opsworks stack creates with a load balanced (one node deployed only) app layer into the previous created VPC
3. Executes a very simple Chef recipe to configure Apache, and deploys a single static html page. 

Taken out of the release because of bugs
4. Kicks off automated infrastructure tests using ServerSpec

Setup Instructions
1.Boto - AWS SDK for Python
To install boto, use the following command:
pip install -U boto
Or, if you download the tarball package, you can call the setup.py script directly: 
tar xzf http://boto.googlecode.com/files/boto-1.9b.tar.gz
cd boto-1.9b
python setup.py install
These are the only two configuration parameters you need to be concerned with. The file should look like this: 
[Credentials]
aws_access_key_id = {ACCESS KEY ID}
aws_secret_access_key = {SECRET ACCESS KEY}
You will find these values after logging in to your AWS account and clicking Account. Click the Security Credentials 

2.Configure AWS Credentials using credentials file or AWS Configure. A default region should be specified

3. All files needed for the deployment are available on https://github.com/willecollins/Stelligent

Usage:
python StelligentMiniProject.py CFNStackName CFNTemplatePath OPSWorksTemplatePath AWSRegion

Example
python StelligentMiniProject.py LateStackTest StelligentCloudFormation.json StelligentOpsWorks.json us-west-2


Known Issues

Trying to create a stack with the same name in a region will cause an error. A future revision would check for the existing of the template and perform and update instead of a create. 

The region that is passed in must be the same as your default region for your account in this version. 