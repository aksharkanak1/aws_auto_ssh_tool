# aws_auto_ssh_tool
Objective : To execute scripts or list of commands with in all the AWS EC2 instances belonging to specific account .

Features 
1) Get the list of  AWS resources associated with specific  account. 
2) Login to each of the AWS EC2 instances . Execute a list of commands or list of scripts with the EC2 instance.

Limitations :
1)Currently only  public key authnetication is supported for ssh login to EC2 Instance  . The user can provide only one key.
2)Since the appilcation is launched outside AWS all the EC2 intance should have public ip address .
3)As of now there is no filter while selecting the EC2 instance.
   
   
