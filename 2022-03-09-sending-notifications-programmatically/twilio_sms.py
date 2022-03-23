from twilio.rest import Client

account_sid = "[REDACTED]"
auth_token = "[REDACTED]"
client = Client(account_sid, auth_token)

message = client.messages.create(body="Hello there!", from_='[REDACTED]', to='[REDACTED]')
