import boto3
import logging

from yeti.config import AwsConfig

logger = logging.getLogger("notify")

config = AwsConfig()

topic = config.get(AwsConfig.MOTION_EVENT_TOPIC)
message = config.get(AwsConfig.MOTION_EVENT_MESSAGE)

client = boto3.client('sns')


def send():
    logger.info("Attempting to send motion detected event")

    try:
        client.publish(TopicArn=topic,
                       Message=message,
                       Subject="New Motion Event")
    except Exception as e:
        logger.exception(e)
        logger.info("Exception occurred when attempting to notify motion event. Ignoring")


if __name__ == "__main__":
    send()
