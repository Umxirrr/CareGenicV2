import boto3

def send_sms(phone_number, message):
    try:
        sns = boto3.client(
            "sns",
            region_name="ap-south-1",
            aws_access_key_id="AKIAUUHAPO3WDAWOLU6H",
            aws_secret_access_key="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"
        )
        response = sns.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        return True, response['MessageId']
    except Exception as e:
        return False, str(e)
