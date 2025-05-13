import boto3

def send_sms(phone_number, message):
    try:
        sns = boto3.client("sns", region_name="ap-south-1")  # Use Mumbai region
        response = sns.publish(
            PhoneNumber=phone_number,  # Must be in +91XXXXXXXXXX format
            Message=message
        )
        return True, response['MessageId']
    except Exception as e:
        return False, str(e)
