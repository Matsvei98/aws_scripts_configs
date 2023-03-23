import boto3
import os
import urllib.request
from tqdm import tqdm

# set AWS profile name
boto3.setup_default_session(profile_name='dev') # region_name='us-east-1'

# set list of lambda names
lambda_names = ["toothapps-schedule-save", "toothapps-schedule-find", "toothapps-schedule-event-find-by-criteria", "toothapps-schedule-event-find-times-by-criteria", "toothapps-schedule-event-save"]
version = "20230320"

# create main project folder
project_name = "project"
config_folder = "cloudformation"
# main folder
if not os.path.exists(project_name):
    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, config_folder))

for lambda_name in lambda_names:
    # create lambda folder and subfolders
    lambda_folder = os.path.join(project_name, "lambda", lambda_name)
    lambda_version_folder = os.path.join(lambda_folder, version)
    if not os.path.exists(lambda_version_folder):
        os.makedirs(lambda_version_folder)

    # download lambda zip file using Boto3
    lambda_client = boto3.client('lambda')
    response = lambda_client.get_function(
        FunctionName=lambda_name,
    )
    
    code_location = response["Code"]["Location"]
    filename=f"{project_name}/lambda/{lambda_name}/{version}/{lambda_name}.zip"

    with tqdm(unit="B", unit_scale=True, miniters=1, desc=filename) as t:
        urllib.request.urlretrieve(code_location, filename=filename, reporthook=lambda blocknum, bs, size: t.update(bs * blocknum - t.n))