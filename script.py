import argparse
import boto3
import docker
from botocore.exceptions import ClientError
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run a Docker container and stream logs to AWS CloudWatch."
    )
    parser.add_argument(
        "--docker-image", required=True, help="Name of the Docker image"
    )
    parser.add_argument(
        "--bash-command",
        required=True,
        help="Bash command to run inside the Docker image",
    )
    parser.add_argument(
        "--aws-cloudwatch-group", required=True, help="Name of the AWS CloudWatch group"
    )
    parser.add_argument(
        "--aws-cloudwatch-stream",
        required=True,
        help="Name of the AWS CloudWatch stream",
    )
    parser.add_argument("--aws-access-key-id", required=True, help="AWS access key ID")
    parser.add_argument(
        "--aws-secret-access-key", required=True, help="AWS secret access key"
    )
    parser.add_argument("--aws-region", required=True, help="Name of the AWS region")
    return parser.parse_args()


def create_cloudwatch_client(aws_access_key_id, aws_secret_access_key, aws_region):
    return boto3.client(
        "logs",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def ensure_cloudwatch_log_group_and_stream(cloudwatch_client, group_name, stream_name):
    try:
        cloudwatch_client.create_log_group(logGroupName=group_name)
    except cloudwatch_client.exceptions.ResourceAlreadyExistsException:
        print(f"Log group {group_name} already exists.")

    try:
        cloudwatch_client.create_log_stream(
            logGroupName=group_name, logStreamName=stream_name
        )
    except cloudwatch_client.exceptions.ResourceAlreadyExistsException:
        print(f"Log stream {stream_name} under group {group_name} already exists.")


def run_docker_container(docker_image, bash_command):
    client = docker.from_env()
    container = client.containers.run(docker_image, command=bash_command, detach=True)

    return container


def stream_logs_to_cloudwatch(container, cloudwatch_client, group_name, stream_name):
    output = container.attach(stdout=True, stream=True, logs=True)
    for log in output:
        print(log)
        try:
            cloudwatch_client.put_log_events(
                logGroupName=group_name,
                logStreamName=stream_name,
                logEvents=[
                    {
                        "timestamp": int(datetime.now().timestamp() * 1000),
                        "message": log.decode("utf-8"),
                    }
                ],
            )
        except ClientError as e:
            print(f"Error sending logs to CloudWatch: {e}")


def main():
    args = parse_arguments()

    cloudwatch_client = create_cloudwatch_client(
        args.aws_access_key_id, args.aws_secret_access_key, args.aws_region
    )
    ensure_cloudwatch_log_group_and_stream(
        cloudwatch_client, args.aws_cloudwatch_group, args.aws_cloudwatch_stream
    )
    container = run_docker_container(args.docker_image, args.bash_command)
    print(f"Container {container.id} is running.")

    try:
        stream_logs_to_cloudwatch(
            container,
            cloudwatch_client,
            args.aws_cloudwatch_group,
            args.aws_cloudwatch_stream,
        )
    finally:
        container.stop()
        container.remove()
        print("Container stopped and removed.")


if __name__ == "__main__":
    main()
