import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


async def send_otp_email(to_email: str, otp: str, full_name: str) -> bool:
    """
    Send OTP email to user
    
    Args:
        to_email: Recipient email address
        otp: One-time password
        full_name: User's full name
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Mã xác thực OTP - Speed Up"
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        
        # Plain text version
        text_content = f"""
        Xin chào {full_name},
        
        Cảm ơn bạn đã đăng ký tài khoản Speed Up!
        
        Mã xác thực OTP của bạn là: {otp}
        
        Mã này sẽ hết hạn sau 5 phút.
        
        Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email này.
        
        Trân trọng,
        Đội ngũ Speed Up
        """
        
        # HTML version
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #333;
                    margin: 0;
                }}
                .content {{
                    color: #555;
                    line-height: 1.6;
                }}
                .otp-box {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-size: 32px;
                    font-weight: bold;
                    letter-spacing: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #888;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Speed Up</h1>
                </div>
                <div class="content">
                    <p>Xin chào <strong>{full_name}</strong>,</p>
                    <p>Cảm ơn bạn đã đăng ký tài khoản Speed Up!</p>
                    <p>Mã xác thực OTP của bạn là:</p>
                    <div class="otp-box">{otp}</div>
                    <p><strong>Lưu ý:</strong> Mã này sẽ hết hạn sau 5 phút.</p>
                    <p>Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email này.</p>
                </div>
                <div class="footer">
                    <p>Trân trọng,<br>Đội ngũ Speed Up</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach both versions
        message.attach(MIMEText(text_content, "plain"))
        message.attach(MIMEText(html_content, "html"))
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True
        )
        
        logger.info(f"OTP email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {to_email}: {str(e)}")
        return False


async def send_welcome_email(to_email: str, full_name: str) -> bool:
    """
    Send welcome email after OTP verification
    
    Args:
        to_email: Recipient email address
        full_name: User's full name
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Chào mừng đến với Speed Up!"
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .content {{
                    color: #555;
                    line-height: 1.6;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #888;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Chào mừng {full_name}!</h1>
                </div>
                <div class="content">
                    <p>Tài khoản của bạn đã được xác thực thành công.</p>
                    <p>Giờ bạn có thể đăng nhập và bắt đầu học tập với Speed Up.</p>
                </div>
                <div class="footer">
                    <p>Trân trọng,<br>Đội ngũ Speed Up</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html_content, "html"))
        
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True
        )
        
        logger.info(f"Welcome email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
        return False
