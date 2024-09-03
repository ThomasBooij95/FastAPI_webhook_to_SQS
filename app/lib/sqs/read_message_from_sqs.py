import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv("./app/.env")


def read_messages_from_queue(queue_name):
    """
    Reads all messages from the specified SQS queue and returns them.

    :param queue_name: Name of the SQS queue.
    :return: Messages string if the process was successful, False otherwise.
    """
    # Create a new session using default credentials and region.
    session = boto3.Session()

    # Get the SQS and S3 clients
    sqs = session.client("sqs")

    messages = []

    try:
        # Get the URL for the SQS queue
        queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
        messages_attrs = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=[
                "ApproximateNumberOfMessages",
                "ApproximateNumberOfMessagesNotVisible",
            ],
        )["Attributes"]

        messages_in_queue = int(messages_attrs["ApproximateNumberOfMessages"])
        print(f"Approximate messages in queue {messages_in_queue}")
        # Continuously poll the queue until no more messages are available
        while True:
            # Receive a batch of messages (up to 10 at a time)
            response = sqs.receive_message(
                QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=1
            )
            # Check if there are any messages in the response
            if "Messages" in response:
                for message in response["Messages"]:
                    messages.append(message["Body"])
            else:
                break  # No more messages in the queue

        if messages:
            # Convert messages list to a single string (or any format you prefer)
            message_data = "\n".join(messages)
            return message_data

        else:
            print("No messages found in the queue.")
            return False

    except ClientError as e:
        print(f"An error occurred: {e}")
        return False


# Example usage:
if __name__ == "__main__":
    queue_name = "sd_webinargeek_subscriptions"

    messages = read_messages_from_queue(queue_name)

    if messages:
        print(messages)
    else:
        print("Operation failed.")
