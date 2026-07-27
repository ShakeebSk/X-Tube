from pydantic import BaseModel


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ConfirmSignupRequest(BaseModel):
    email: str
    otp: str


class ResendOTP(BaseModel):
    email: str
