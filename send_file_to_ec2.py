import os
import requests
import json
import paramiko
    
json_file_path = input("Enter the path to save the JSON file: ")
ec2_instance_ip = input("Enter the EC2 instance IP address: ")
ec2_username = input("Enter the username for connecting to the EC2 instance: ")
private_key_path = input("Enter the path to your private key (PEM): ")
object_file_path = input("Enter the path to object file: ")

currency_exchange_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        print("Data loaded from file")
else:
    response = requests.get(currency_exchange_url)
    if response.status_code == 200:
        data = response.json()
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print("Data successfully received and saved to a file")
    else:
        print("Error while receiving data")

def send_json_to_instance(ec2_instance_ip, ec2_username, private_key_path, file, object=None):
    ssh = paramiko.SSHClient()
    private_key = paramiko.RSAKey(filename=private_key_path)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ec2_instance_ip, username=ec2_username, pkey=private_key)

    if object is None:
        object = os.path.basename(file)

    sftp = ssh.open_sftp()
    sftp.put(file, object)

    sftp.close()
    ssh.close()

    print(f"File {file} successfully sent to EC2 instance at {object}.")

send_json_to_instance(ec2_instance_ip, ec2_username, private_key_path, json_file_path, object_file_path)