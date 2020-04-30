import os
import http.client
import json

# Slack limit for messages' length: https://api.slack.com/reference/block-kit/blocks#section
SLACK_LIMIT = 3000


def get_config():
    r = {}
    r['FILE'] = os.getenv('PLUGIN_FILE', default=None)
    r['WEBHOOK'] = os.getenv('PLUGIN_WEBHOOK', default=None)
    r['DRONE_SERVER'] = os.getenv('PLUGIN_DRONE_SERVER', default=None)
    r['DRONE_REPO'] = os.getenv('DRONE_REPO', default=None)
    r['DRONE_BUILD_NUMBER'] = os.getenv('DRONE_BUILD_NUMBER', default=None)
    return r


def generate_payload(data, code=False):
    if code:
        msg = '```' + data + '```'
    else:
        msg = data

    r = {
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': msg
                }
            }
        ]
    }

    return r


def send(message, webhook, code=None):
    conn = http.client.HTTPSConnection(host='hooks.slack.com')

    payload = json.dumps(generate_payload(message, code))
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache'
    }

    conn.request(
        method='POST',
        url=webhook,
        body=payload,
        headers=headers
    )


def main():
    '''
    Mandatory configuration variables:
        PLUGIN_FILE
        PLUGIN_WEBHOOK

    Optional configuration variables:
        PLUGIN_DRONE_SERVER

    Also, this plugin uses some DRONE environment variables:
        DRONE_REPO
        DRONE_BUILD_NUMBER
    '''

    config = get_config()
    drone_url = None

    if config['DRONE_SERVER']:
        drone_url = config['DRONE_SERVER'] + '/' + \
            config['DRONE_REPO'] + '/' + config['DRONE_BUILD_NUMBER']

    with open(config['FILE'], 'r') as file:
        message = file.read()

    # The '+ 6' is because we add 6 ticks '` to the message to create a code block on Slack
    if len(message) + 6 <= SLACK_LIMIT:
        send(message, config['WEBHOOK'], code=True)
    else:
        # Show latest 3000 characters of file
        total_chars = 6 - SLACK_LIMIT
        truncated_msg = message[total_chars:]
        send(truncated_msg, config['WEBHOOK'], code=True)
        if drone_url:
            send('File is truncated due to Slack limits. Follow ' +
                 drone_url + ' to get full file.', config['WEBHOOK'])
        else:
            send('Go to Drone to get full file.', config['WEBHOOK'])


if __name__ == "__main__":
    main()
