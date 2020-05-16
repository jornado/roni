from mailjet_rest import Client
import os
api_key = '16d68097f0234b7818a7756127738541'
api_secret = 'd6f50da9bbec197fde9ab20eadaf1998'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "slothingtonspam@gmail.com",
        "Name": "Jordan"
      },
      "To": [
        {
          "Email": "slothingtonspam@gmail.com",
          "Name": "Jordan"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print result.status_code
print result.json()
