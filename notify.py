import json
import os
import urllib3

# Get the Slack Webhook URL from Lambda environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
http = urllib3.PoolManager()

def lambda_handler(event, context):
    # 1. Parse the message from the SNS event
    sns_message = event['Records'][0]['Sns']['Message']
    data = json.loads(sns_message)

    # 2. Extract details from the Jenkins message
    status = data.get('status', 'UNKNOWN')
    project = data.get('project', 'N/A')
    build_num = data.get('build_number', 'N/A')
    build_url = data.get('url', '#')
    commit = data.get('commit', 'N/A')

    # 3. Format the Slack message
    if "SUCCESS" in status:
        color = "#36a64f" # Green
        emoji = "✅"
    else:
        color = "#d50000" # Red
        emoji = "🚨"

    slack_payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{emoji} Jenkins Pipeline {status}*"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Project:*\n{project}"},
                            {"type": "mrkdwn", "text": f"*Build Number:*\n<{build_url}|#{build_num}>"},
                            {"type": "mrkdwn", "text": f"*Commit:*\n`{commit}`"}
                        ]
                    }
                ]
            }
        ]
    }

    # 4. Post the message to Slack
    try:
        encoded_data = json.dumps(slack_payload).encode('utf-8')
        response = http.request(
            'POST',
            SLACK_WEBHOOK_URL,
            body=encoded_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Message posted to Slack. Status: {response.status}")
    except Exception as e:
        print(f"Error posting to Slack: {e}")
        raise e

    return {
        'statusCode': 200
    }