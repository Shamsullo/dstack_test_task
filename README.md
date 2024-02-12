## Overview
This Python script facilitates running a Docker container and streaming its logs to AWS CloudWatch. It is a test task for the Backend Engineer position at [dstack.ai](https://dstack.ai) as part of my application.  It accepts parameters such as Docker image name, bash command to execute within the container, AWS CloudWatch group and stream names, as well as AWS credentials. The task technical requirements can be found [here](./Backend%20Engineer%20Test%20Task%20(Updated).pdf)

## Dependencies
The exact version used can be found in the requirements.txt file
1. Python 3.10 or higher
2. boto3
3. docker
   
## Usage
```bash
python script.py --docker-image IMAGE_NAME --bash-command "COMMAND" --aws-cloudwatch-group GROUP_NAME --aws-cloudwatch-stream STREAM_NAME --aws-access-key-id ACCESS_KEY --aws-secret-access-key SECRET_KEY --aws-region REGION
```
## Functions and flow
1.  **Argument Parsing:** Parse command-line arguments using argparse to get Docker image name, bash command, AWS CloudWatch group and stream names, and AWS credentials.
2. **AWS CloudWatch Client Creation:** Create a boto3 client for CloudWatch using the provided AWS credentials and region.
3. **Ensure CloudWatch Log Group and Stream Existence:** Check if the specified log group and stream exist in CloudWatch, create them if not.
4. **Run Docker Container:** Use Docker SDK to run a container with the specified image and command.
5. **Stream Logs to CloudWatch:** Continuously stream logs from the Docker container to the specified CloudWatch log group and stream.
6. **Cleanup:** Stop and remove the Docker container once logging is done.


## NOTES:
- The program expects permissions to interact with CloudWatch and Docker are properly set
- For now, for simplicity, the script prints log messages to the console. As well, stream them to CloudWatch
- Basic error handling is implemented
- Container removal is handled automatically after logging is finished
