from fastapi_mail import FastMail, ConnectionConfig, MessageType, MessageSchema
from src.config import Config

config = ConnectionConfig(
    MAIL_USERNAME="sunarsushil100@gmail.com",
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Social Mate",
    MAIL_FROM="sunarsuhil100@gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
mail = FastMail(config)


def otpHtmlMessage(optCode: str):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>OTP Verification</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          margin: 0;
          padding: 0;
        }}
        .container {{
          width: 100%;
          max-width: 400px;
          margin: 50px auto;
          background: #fff;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          border-radius: 8px;
          overflow: hidden;
        }}
        .header {{
          text-align: center;
          background-color: #4CAF50;
          color: #fff;
          padding: 20px;
        }}
        .header img {{
          width: 60px;
          height: auto;
          margin-bottom: 10px;
        }}
        .content {{
          padding: 20px;
          text-align: center;
        }}
        .content p {{
          margin: 15px 0;
          font-size: 16px;
          color: #333;
        }}
        .otp {{
          display: inline-block;
          padding: 10px 20px;
          font-size: 20px;
          color: #fff;
          background-color: #007BFF;
          border-radius: 5px;
          margin: 10px 0;
          font-weight: bold;
        }}
        .footer {{
          text-align: center;
          padding: 10px;
          font-size: 12px;
          color: #888;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <img src="https://cdn.dribbble.com/users/120295/screenshots/814551/drib.jpg" alt="Logo">
          <h2>OTP Verification</h2>
        </div>
        <div class="content">
          <p>Don't share the following code with anyone:</p>
          <span class="otp">{optCode}</span>
          <p>If you did not request this code, please ignore this message.</p>
        </div>
        <div class="footer">
          &copy; 2024 Social Mate. All rights reserved.
        </div>
      </div>
    </body>
    </html>
    """


def createMessage(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    return message
