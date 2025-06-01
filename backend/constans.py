import os
from dotenv import load_dotenv


load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

SIMILARITY_THRESHOLD = 0.4

FAQ_DATA = [
    "To get a refund, submit a request within 14 days.",
    "We work from 9 AM to 6 PM on weekdays.",
    "You can change your password via 'Forgot Password?'.",
    "Delivery takes 3 to 5 business days.",
    "Support is available by phone and chat.",
    "Registration takes no more than 2 minutes.",
    "To recover your account, use your email or phone number.",
]
