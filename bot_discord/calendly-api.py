import requests
import json
import config

def get_token_from_file(filename):
    with open(filename, 'r') as file:
        token = file.read().strip()
    return token

def get_user_info(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get('https://api.calendly.com/users/me', headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to get user info: {response.content}')

def subscribe_to_webhook(url, token, events, scope, signing_key: str = None):
    response = get_user_info(token)
    organization = response.get('resource').get('current_organization')
    user = response.get('resource').get('uri')

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        'url': url,
        'events': events,
        'organization': organization,
        'user': user,
        'scope': scope,
    }
    response = requests.post('https://api.calendly.com/webhook_subscriptions', headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print('Successfully subscribed to webhook')
    else:
        print(f'Failed to subscribe to webhook: {response.content}')

# Example usage:
webhook_url = input("Enter the webhook URL: ")
subscribe_to_webhook(
    f'{webhook_url}/webhook', 
    config.CALENDY_API_KEY, 
    ['invitee.created', 'invitee.canceled', 'invitee_no_show.created'],
    'user',
)