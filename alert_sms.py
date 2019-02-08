# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC05c0e2be35475ebdbf8066d508b7b87f'
auth_token = 'f0d8bb26b168a16e6c6dfa740c2880c4'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Company's twitter Account has reach threshold negative sentiment. Please check twitter ASAP!",
                     from_='+18572801622',
                     to='+17819990216'
                 )

print(message.sid)