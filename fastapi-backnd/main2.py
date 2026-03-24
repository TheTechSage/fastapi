# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr
# import smtplib

# app = FastAPI()

# # Configuration (Keep these secure!)
# EMAIL = "mk9405194@gmail.com"
# PASSCODE = "trov jxlr fnko axuh"

# # Data model for the request body
# class EmailRequest(BaseModel):
#     recipient: EmailStr
#     subject: str
#     body: str

# @app.post("/send-email")
# async def send_email_api(request: EmailRequest):
#     # Construct the message
#     message = f"Subject: {request.subject}\n\n{request.body}"
    
#     try:
#         # Using 'with' automatically closes the connection
#         with smtplib.SMTP("smtp.gmail.com", 587) as connection:
#             connection.starttls()
#             connection.login(user=EMAIL, password=PASSCODE)
#             connection.sendmail(
#                 from_addr=EMAIL,
#                 to_addrs=request.recipient,
#                 msg=message
#             )
#         return {"status": "success", "message": f"Email sent to {request.recipient}"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# import random
# import smtplib
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr

# app = FastAPI()

# # Configuration
# EMAIL = "mk9405194@gmail.com"
# PASSCODE = "trov jxlr fnko axuh"

# # Temporary storage for OTPs (In-memory)
# # Format: {"email@example.com": "123456"}
# otp_storage = {}

# class OTPRequest(BaseModel):
#     email: EmailStr

# class VerifyRequest(BaseModel):
#     email: EmailStr
#     otp: str

# def send_otp_email(target_email, otp):
#     subject = "Your Verification Code"
#     body = f"Your OTP code is: {otp}. It will expire soon."
#     message = f"Subject: {subject}\n\n{body}"
    
#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(EMAIL, PASSCODE)
#         server.sendmail(EMAIL, target_email, message)

# @app.post("/send-otp")
# async def send_otp(request: OTPRequest):
#     # 1. Generate a 6-digit OTP
#     otp = str(random.randint(100000, 999999))
    
#     # 2. Store it in our dictionary
#     otp_storage[request.email] = otp
    
#     try:
#         # 3. Send the email
#         send_otp_email(request.email, otp)
#         return {"message": "OTP sent successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/verify-otp")
# async def verify_otp(request: VerifyRequest):
#     # Check if the email exists in our storage
#     if request.email in otp_storage:
#         # Compare the stored OTP with the user's input
#         if otp_storage[request.email] == request.otp:
#             # Delete OTP after successful verification so it can't be reused
#             del otp_storage[request.email]
#             return {"status": "verified", "message": "Email authenticated successfully!"}
#         else:
#             raise HTTPException(status_code=400, detail="Invalid OTP code")
    
#     raise HTTPException(status_code=404, detail="No OTP found for this email")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client

app = FastAPI()

# --- CONFIGURATION ---
# Replace with your actual Twilio credentials
TWILIO_ACCOUNT_SID = "your_sid_here"
TWILIO_AUTH_TOKEN = "your_token_here"
TWILIO_NUMBER = "+1234567890"  # Your Twilio virtual number

# Using the same dictionary logic from the email example
otp_storage = {}

class SMSRequest(BaseModel):
    phone_number: str  # Format: +919876543210

class VerifyRequest(BaseModel):
    phone_number: str
    otp: str

# --- ENDPOINTS ---

@app.post("/send-sms-otp")
async def send_sms_otp(request: SMSRequest):
    # 1. Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    otp_storage[request.phone_number] = otp
    
    try:
        # 2. Initialize Twilio Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # 3. Send the SMS
        message = client.messages.create(
            body=f"Your Verification Code is: {otp}",
            from_=TWILIO_NUMBER,
            to=request.phone_number
        )
        
        return {"status": "success", "message_sid": message.sid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMS failed: {str(e)}")

@app.post("/verify-sms-otp")
async def verify_sms_otp(request: VerifyRequest):
    if request.phone_number in otp_storage:
        if otp_storage[request.phone_number] == request.otp:
            del otp_storage[request.phone_number] # Clear after use
            return {"status": "verified", "message": "Mobile number verified!"}
        else:
            raise HTTPException(status_code=400, detail="Incorrect OTP")
            
    raise HTTPException(status_code=404, detail="No OTP requested for this number")