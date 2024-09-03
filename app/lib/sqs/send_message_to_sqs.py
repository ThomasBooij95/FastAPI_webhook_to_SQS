import boto3
from botocore.exceptions import ClientError


def send_message_to_sqs(queue_name, message_body):
    """
    Sends a message to the specified SQS queue.

    :param queue_name: Name of the SQS queue.
    :param message_body: The message content to be sent.
    :return: The response from the SQS service../
    """
    # Create a new session using default credentials and region.

    session = boto3.Session()

    # Get the SQS client
    sqs = session.client("sqs")

    try:
        # Get the URL for the SQS queue
        queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]

        # Send the message
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

        return response

    except ClientError as e:
        print(f"An error occurred: {e}")
        return e


# Example usage:
if __name__ == "__main__":
    queue_name = "sd_webinargeek_subscriptions"
    message_body = "AWS Programming is easy"

    response = send_message_to_sqs(queue_name, message_body)
    if response:
        print(f"Message sent! Message ID: {response}")
