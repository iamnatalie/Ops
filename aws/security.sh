#!/bin/bash
# adds rules to aws security group
cloudflare=(103.21.244.0/22 103.22.200.0/22 103.31.4.0/22 104.16.0.0/12 108.162.192.0/18 131.0.72.0/22 141.101.64.0/18 162.158.0.0/15 172.64.0.0/13 173.245.48.0/20 188.114.96.0/20 190.93.240.0/20 197.234.240.0/22 198.41.128.0/17 199.27.128.0/21)

for ip in ${cloudflare[*]}; do
	aws ec2 authorize-security-group-ingress --group-id sg-0db1106a --protocol tcp --port 80 --cidr $ip
	aws ec2 authorize-security-group-ingress --group-id sg-0db1106a --protocol tcp --port 443 --cidr $ip
done