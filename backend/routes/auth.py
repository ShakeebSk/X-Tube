from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie
import boto3

# from backend.db.middleware.auth_middleware import get_current_user
from db.middleware.auth_middleware import get_current_user
from db.models.users import User

# from backend.db.db import get_db
from db.db import get_db
from secrets_keys import SecretKeys
from helper.auth_helper import get_secret_hash
from sqlalchemy.orm import Session

# from backend.pydantic_models.auth_models import SignupRequest


from pydantic_models.auth_models import (
    SignupRequest,
    LoginRequest,
    ConfirmSignupRequest,
    ResendOTP,
)


router = APIRouter()
secret_keys = SecretKeys()

# COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
# COGNITO_CLIENT_SECRET = secret_keys.COGNITO_CLIENT_SECRET

# cognito_client = boto3.client("cognito-idp", region_name=secret_keys.REGION_NAME)


# @router.post("/signup")
# def signup_user(data: SignupRequest, db: Session = Depends(get_db)):

#     try:
#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.sign_up(
#             ClientId=COGNITO_CLIENT_ID,
#             Username=data.email,
#             Password=data.password,
#             SecretHash=secret_hash,
#             UserAttributes=[
#                 {"Name": "email", "Value": data.email},
#                 {"Name": "name", "Value": data.name},
#             ],
#         )

#         cognito_sub = cognito_response.get("UserSub")

#         if not cognito_sub:
#             raise HTTPException(400, "Cognito did not return a valid user sub")

#         new_user = User(name=data.name, email=data.email, cognito_sub=cognito_sub)

#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)

#         return {
#             "message": "Signup Successfull. Please verify your email if required..."
#         }

#     except Exception as e:
#         raise HTTPException(400, f"Cognito signup exception {e}")


# # @router.post("/signup")
# # def signup_user(data: SignupRequest, db: Session = Depends(get_db)):
# #     try:
# #         # Check if user already exists in DB first
# #         existing_user = db.query(User).filter(User.email == data.email).first()
# #         if existing_user:
# #             raise HTTPException(status_code=400, detail="User already exists in database.")

# #         secret_hash = get_secret_hash(data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

# #         cognito_response = cognito_client.sign_up(
# #             ClientId=COGNITO_CLIENT_ID,
# #             Username=data.email,
# #             Password=data.password,
# #             SecretHash=secret_hash,
# #             UserAttributes=[
# #                 {"Name": "email", "Value": data.email},
# #                 {"Name": "name", "Value": data.name},
# #             ],
# #         )

# #         cognito_sub = cognito_response.get("UserSub")
# #         if not cognito_sub:
# #             raise HTTPException(400, "Cognito did not return a valid user sub")

# #         new_user = User(name=data.name, email=data.email, cognito_sub=cognito_sub)
# #         db.add(new_user)
# #         db.commit()
# #         db.refresh(new_user)

# #         return {"message": "Signup successful. Please verify your email if required."}

# #     except cognito_client.exceptions.UsernameExistsException:
# #         raise HTTPException(status_code=400, detail="User already exists in Cognito.")

# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=f"Cognito signup exception: {e}")


# @router.post("/login")
# def login_user(
#     data: LoginRequest, response: Response
# ):  # db: Session = Depends(get_db)):

#     try:
#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.initiate_auth(
#             ClientId=COGNITO_CLIENT_ID,
#             AuthFlow="USER_PASSWORD_AUTH",
#             # Username=data.email,
#             # Password=data.password,
#             # SecretHash=secret_hash,
#             AuthParameters={
#                 "USERNAME": data.email,
#                 "PASSWORD": data.password,
#                 "SECRET_HASH": secret_hash,
#             },
#         )

#         auth_result = cognito_response.get("AuthenticationResult")

#         if not auth_result:
#             raise HTTPException(400, "Incorrect cognito response")

#         access_token = auth_result.get("AccessToken")
#         refresh_token = auth_result.get("RefreshToken")

#         response.set_cookie(
#             key="access_token", value=access_token, httponly=True, secure=True
#         )

#         response.set_cookie(
#             key="refresh_token", value=refresh_token, httponly=True, secure=True
#         )

#         return {"message": "User Logged-in Successfully..."}
#     except Exception as e:
#         raise HTTPException(400, f"Cognito Login exception {e}")


# # @router.post("/confirm-signup")
# # def confirm_signup(data: ConfirmSignupRequest):  # db: Session = Depends(get_db)):

# #     try:
# #         secret_hash = get_secret_hash(
# #             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
# #         )

# #         cognito_response = cognito_client.confirm_sign_up(
# #             ClientId=COGNITO_CLIENT_ID,
# #             Username=data.email,
# #             ConfirmationCode=data.otp,
# #             SecretHash=secret_hash,
# #             # AuthFlow="USER_PASSWORD_AUTH" ,
# #             # Username=data.email,
# #             # Password=data.password,
# #             # SecretHash=secret_hash,
# #             # AuthParameters={
# #             #     'USERNAME':data.email,
# #             #     'PASSWORD':data.password,
# #             #     'SECRET_HASH':secret_hash,
# #             #     ''
# #             # }
# #         )
# #         return {"message: user confirmed successfully!"}
# #     except Exception as e:
# #         raise HTTPException(400, f"Cognito Login exception {e}")


# @router.post("/confirm-signup")
# def confirm_signup(data: ConfirmSignupRequest):
#     try:
#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_client.confirm_sign_up(
#             ClientId=COGNITO_CLIENT_ID,
#             Username=data.email,
#             ConfirmationCode=data.otp,
#             SecretHash=secret_hash,
#         )

#         return {"message": "User confirmed successfully!"}

#     except cognito_client.exceptions.NotAuthorizedException as e:
#         # This happens when user is already confirmed
#         if "Current status is CONFIRMED" in str(e):
#             return {"message": "User is already confirmed. Please proceed to login."}
#         raise HTTPException(status_code=400, detail=str(e))

#     except Exception as e:
#         raise HTTPException(
#             status_code=400, detail=f"Cognito confirm-signup exception: {e}"
#         )


# # @router.post("/refresh")
# # def refresh_token(
# #     refresh_token: str = Cookie(None),
# #     user_cognito_sub: str = Cookie(None),
# #     response: Response = None,
# # ):  # db: Session = Depends(get_db)):

# #     try:
# #         secret_hash = get_secret_hash(
# #             user_cognito_sub, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
# #         )

# #         cognito_response = cognito_client.initiate_auth(
# #             ClientId=COGNITO_CLIENT_ID,
# #             AuthFlow="REFRESH_TOKEN_AUTH",
# #             AuthParameters={"REFRESH_TOKEN": refresh_token, "SECRET_HASH": secret_hash},
# #         )

# #         auth_result = cognito_response.get("AuthenticationResult")

# #         if not auth_result:
# #             raise HTTPException(400, "Incorrect cognito response")

# #         access_token = auth_result.get("AccessToken")
# #         # refresh_token = auth_result.get("RefreshToken")

# #         response.set_cookie(
# #             key="access_token", value=access_token, httponly=True, secure=True
# #         )

# #         # response.set_cookie(
# #         #     key="refresh_token", value=refresh_token, httponly=True, secure=True
# #         # )

# #         # return cognito_response
# #         return {"message: Access token  refreshed!"}

# #     except Exception as e:
# #         raise HTTPException(400, f"Cognito Login exception {e}")

# # from fastapi import APIRouter, HTTPException, Response, Cookie
# # import boto3
# # from botocore.exceptions import ClientError

# router = APIRouter()


# @router.post("/refresh")
# def refresh_token(
#     refresh_token: str = Cookie(None),
#     user_cognito_sub: str = Cookie(None),
#     response: Response = None,
# ):
#     if not refresh_token or not user_cognito_sub:
#         raise HTTPException(
#             status_code=401, detail="Missing refresh token or user info"
#         )

#     try:
#         secret_hash = get_secret_hash(
#             user_cognito_sub, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.initiate_auth(
#             ClientId=COGNITO_CLIENT_ID,
#             AuthFlow="REFRESH_TOKEN_AUTH",
#             AuthParameters={"REFRESH_TOKEN": refresh_token, "SECRET_HASH": secret_hash},
#         )

#         auth_result = cognito_response.get("AuthenticationResult")
#         if not auth_result:
#             raise HTTPException(status_code=400, detail="Invalid Cognito response")

#         access_token = auth_result.get("AccessToken")

#         # ✅ Set a new access token cookie
#         response.set_cookie(
#             key="access_token",
#             value=access_token,
#             httponly=True,
#             secure=True,
#             samesite="None",  # ensure cross-origin cookie works if Flutter uses localhost
#         )

#         return {"message": "Access token refreshed!"}

#     except cognito_client.exceptions.NotAuthorizedException as e:
#         # Cognito-specific error for expired/invalid refresh token
#         detail = str(e)
#         if "expired" in detail.lower():
#             raise HTTPException(
#                 status_code=401, detail="Refresh token expired, please log in again"
#             )
#         raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

#     except ClientError as e:
#         # Any other AWS-related client error
#         raise HTTPException(
#             status_code=500,
#             detail=f"AWS Client error: {e.response['Error']['Message']}",
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


router = APIRouter()
secret_keys = SecretKeys()

COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
COGNITO_CLIENT_SECRET = secret_keys.COGNITO_CLIENT_SECRET

cognito_client = boto3.client(
    "cognito-idp",
    region_name=secret_keys.REGION_NAME,
)


@router.post("/signup")
def signup_user(
    data: SignupRequest,
    db: Session = Depends(get_db),
):
    try:
        secret_hash = get_secret_hash(
            data.email,
            COGNITO_CLIENT_ID,
            COGNITO_CLIENT_SECRET,
        )

        cognito_response = cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email,
            Password=data.password,
            SecretHash=secret_hash,
            UserAttributes=[
                {"Name": "email", "Value": data.email},
                {"Name": "name", "Value": data.name},
            ],
        )

        cognito_sub = cognito_response.get("UserSub")

        if not cognito_sub:
            raise HTTPException(400, "Cognito did not return a valid user sub")

        new_user = User(
            name=data.name,
            email=data.email,
            cognito_sub=cognito_sub,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Signup successful. Please verify your email if required."}
    except Exception as e:
        raise HTTPException(400, f"Cognito sugnup exception: {e}")


@router.post("/login")
def login_user(data: LoginRequest, response: Response):
    try:
        secret_hash = get_secret_hash(
            data.email,
            COGNITO_CLIENT_ID,
            COGNITO_CLIENT_SECRET,
        )

        cognito_response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": data.email,
                "PASSWORD": data.password,
                "SECRET_HASH": secret_hash,
            },
        )

        auth_result = cognito_response.get("AuthenticationResult")

        if not auth_result:
            raise HTTPException(400, "Incorrect cognito response")

        access_token = auth_result.get("AccessToken")
        refresh_token = auth_result.get("RefreshToken")

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
        )

        return {"message": "User logged in successfully!"}
    except Exception as e:
        raise HTTPException(400, f"Cognito sugnup exception: {e}")


@router.post("/confirm-signup")
def confirm_signup(data: ConfirmSignupRequest):
    try:
        secret_hash = get_secret_hash(
            data.email,
            COGNITO_CLIENT_ID,
            COGNITO_CLIENT_SECRET,
        )

        cognito_response = cognito_client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.otp,
            SecretHash=secret_hash,
        )

        return {"message": "User confirmed successfully!"}
    except Exception as e:
        raise HTTPException(400, f"Cognito sugnup exception: {e}")


@router.post("/refresh")
def refresh_token(
    refresh_token: str = Cookie(None),
    user_cognito_sub: str = Cookie(None),
    response: Response = None,
):
    try:
        if not refresh_token or not user_cognito_sub:
            raise HTTPException(400, "cookies cannot be null!")
        secret_hash = get_secret_hash(
            user_cognito_sub,
            COGNITO_CLIENT_ID,
            COGNITO_CLIENT_SECRET,
        )

        cognito_response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
                "SECRET_HASH": secret_hash,
            },
        )
        auth_result = cognito_response.get("AuthenticationResult")

        if not auth_result:
            raise HTTPException(400, "Incorrect cognito response")

        access_token = auth_result.get("AccessToken")

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
        )

        return {"message": "Access token refreshed!"}
    except Exception as e:
        raise HTTPException(400, f"Cognito sugnup exception: {e}")


@router.get("/me")
def protected_route(user=Depends(get_current_user)):
    return {"message": "You are authenticated!", "user": user}


@router.post("/resend-otp")
def resend_otp(data: ResendOTP):
    """
    Resends the Cognito confirmation code to the user's registered email.
    """
    try:
        secret_hash = get_secret_hash(
            data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
        )

        cognito_response = cognito_client.resend_confirmation_code(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email,
            SecretHash=secret_hash,
        )

        delivery_details = cognito_response.get("CodeDeliveryDetails", {})
        destination = delivery_details.get("Destination", "your registered email")

        return {
            "message": f"OTP has been resent successfully to {destination}. Please check your inbox."
        }

    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(
            status_code=404, detail="User not found. Please sign up first."
        )
    except cognito_client.exceptions.InvalidParameterException as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Cognito resend OTP exception: {e}"
        )


# @router.get("/me")
# def potected_route(user=Depends(get_current_user)):
#     return {"message": "You are authenticated! ", "user": user}


# """

# """

# from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
# import boto3
# from botocore.exceptions import ClientError
# from sqlalchemy.orm import Session

# from db.middleware.auth_middleware import get_current_user
# from db.models.users import User
# from db.db import get_db
# from secrets_keys import SecretKeys
# from helper.auth_helper import get_secret_hash
# from pydantic_models.auth_models import (
#     SignupRequest,
#     LoginRequest,
#     ConfirmSignupRequest,
#     ResendOTP,
# )

# router = APIRouter()
# secret_keys = SecretKeys()

# COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
# COGNITO_CLIENT_SECRET = secret_keys.COGNITO_CLIENT_SECRET
# REGION_NAME = secret_keys.REGION_NAME

# cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)


# # -------------------------------------------------------------------
# # 🟢 SIGNUP
# # -------------------------------------------------------------------
# @router.post("/signup")
# def signup_user(data: SignupRequest, db: Session = Depends(get_db)):
#     try:
#         # Check if user already exists in the DB
#         existing_user = db.query(User).filter(User.email == data.email).first()
#         if existing_user:
#             raise HTTPException(
#                 status_code=400, detail="User already exists in database."
#             )

#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.sign_up(
#             ClientId=COGNITO_CLIENT_ID,
#             Username=data.email,
#             Password=data.password,
#             SecretHash=secret_hash,
#             UserAttributes=[
#                 {"Name": "email", "Value": data.email},
#                 {"Name": "name", "Value": data.name},
#             ],
#         )

#         cognito_sub = cognito_response.get("UserSub")
#         if not cognito_sub:
#             raise HTTPException(
#                 status_code=400, detail="Cognito did not return a valid user sub"
#             )

#         new_user = User(name=data.name, email=data.email, cognito_sub=cognito_sub)
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)

#         return {"message": "Signup successful. Please verify your email."}

#     except cognito_client.exceptions.UsernameExistsException:
#         raise HTTPException(status_code=400, detail="User already exists in Cognito.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Cognito signup exception: {e}")


# # -------------------------------------------------------------------
# # 🟢 CONFIRM SIGNUP
# # -------------------------------------------------------------------
# @router.post("/confirm-signup")
# def confirm_signup(data: ConfirmSignupRequest):
#     try:
#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_client.confirm_sign_up(
#             ClientId=COGNITO_CLIENT_ID,
#             Username=data.email,
#             ConfirmationCode=data.otp,
#             SecretHash=secret_hash,
#         )

#         return {"message": "User confirmed successfully!"}

#     except cognito_client.exceptions.NotAuthorizedException as e:
#         if "Current status is CONFIRMED" in str(e):
#             return {"message": "User is already confirmed. Please proceed to login."}
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(
#             status_code=400, detail=f"Cognito confirm-signup exception: {e}"
#         )


# # -------------------------------------------------------------------
# # 🟢 LOGIN
# # -------------------------------------------------------------------
# @router.post("/login")
# def login_user(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
#     try:
#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.initiate_auth(
#             ClientId=COGNITO_CLIENT_ID,
#             AuthFlow="USER_PASSWORD_AUTH",
#             AuthParameters={
#                 "USERNAME": data.email,
#                 "PASSWORD": data.password,
#                 "SECRET_HASH": secret_hash,
#             },
#         )

#         auth_result = cognito_response.get("AuthenticationResult")
#         if not auth_result:
#             raise HTTPException(status_code=400, detail="Invalid Cognito response")

#         access_token = auth_result.get("AccessToken")
#         refresh_token = auth_result.get("RefreshToken")

#         # ✅ Get Cognito user info
#         user_info = cognito_client.get_user(AccessToken=access_token)
#         cognito_sub, email, name = None, None, None
#         for attr in user_info["UserAttributes"]:
#             if attr["Name"] == "sub":
#                 cognito_sub = attr["Value"]
#             elif attr["Name"] == "email":
#                 email = attr["Value"]
#             elif attr["Name"] == "name":
#                 name = attr["Value"]

#         # ✅ Ensure user is in database
#         user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
#         if not user:
#             user = User(name=name, email=email, cognito_sub=cognito_sub)
#             db.add(user)
#             db.commit()
#             db.refresh(user)

#         # ✅ Set cookies for frontend
#         response.set_cookie(
#             key="access_token",
#             value=access_token,
#             httponly=True,
#             secure=True,
#             samesite="None",
#         )
#         response.set_cookie(
#             key="refresh_token",
#             value=refresh_token,
#             httponly=True,
#             secure=True,
#             samesite="None",
#         )
#         response.set_cookie(
#             key="user_cognito_sub",
#             value=cognito_sub,
#             httponly=True,
#             secure=True,
#             samesite="None",
#         )

#         return {
#             "message": "User logged in successfully!",
#             "user": {"name": user.name, "email": user.email},
#         }

#     except cognito_client.exceptions.NotAuthorizedException:
#         raise HTTPException(status_code=401, detail="Incorrect username or password.")
#     except cognito_client.exceptions.UserNotConfirmedException:
#         raise HTTPException(
#             status_code=403, detail="User not confirmed. Please verify your email."
#         )
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Cognito login exception: {e}")


# # -------------------------------------------------------------------
# # 🟢 REFRESH TOKEN
# # -------------------------------------------------------------------
# @router.post("/refresh")
# def refresh_token(
#     refresh_token: str = Cookie(None),
#     user_cognito_sub: str = Cookie(None),
#     response: Response = None,
# ):
#     if not refresh_token or not user_cognito_sub:
#         raise HTTPException(
#             status_code=401, detail="Missing refresh token or user info"
#         )

#     try:
#         secret_hash = get_secret_hash(
#             user_cognito_sub, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.initiate_auth(
#             ClientId=COGNITO_CLIENT_ID,
#             AuthFlow="REFRESH_TOKEN_AUTH",
#             AuthParameters={"REFRESH_TOKEN": refresh_token, "SECRET_HASH": secret_hash},
#         )

#         auth_result = cognito_response.get("AuthenticationResult")
#         if not auth_result:
#             raise HTTPException(status_code=400, detail="Invalid Cognito response")

#         access_token = auth_result.get("AccessToken")

#         response.set_cookie(
#             key="access_token",
#             value=access_token,
#             httponly=True,
#             secure=True,
#             samesite="None",
#         )

#         return {"message": "Access token refreshed successfully!"}

#     except cognito_client.exceptions.NotAuthorizedException as e:
#         if "expired" in str(e).lower():
#             raise HTTPException(
#                 status_code=401, detail="Refresh token expired. Please log in again."
#             )
#         raise HTTPException(status_code=401, detail="Invalid or revoked refresh token.")
#     except ClientError as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"AWS client error: {e.response['Error']['Message']}",
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# # -------------------------------------------------------------------
# # 🟢 RESEND OTP
# # -------------------------------------------------------------------
# @router.post("/resend-otp")
# def resend_otp(data: ResendOTP):
#     try:
#         secret_hash = get_secret_hash(
#             data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
#         )

#         cognito_response = cognito_client.resend_confirmation_code(
#             ClientId=COGNITO_CLIENT_ID,
#             Username=data.email,
#             SecretHash=secret_hash,
#         )

#         destination = cognito_response.get("CodeDeliveryDetails", {}).get(
#             "Destination", "your registered email"
#         )

#         return {"message": f"OTP resent successfully to {destination}."}

#     except cognito_client.exceptions.UserNotFoundException:
#         raise HTTPException(
#             status_code=404, detail="User not found. Please sign up first."
#         )
#     except cognito_client.exceptions.InvalidParameterException as e:
#         raise HTTPException(status_code=400, detail=f"Invalid request: {e}")
#     except Exception as e:
#         raise HTTPException(
#             status_code=400, detail=f"Cognito resend OTP exception: {e}"
#         )


# # -------------------------------------------------------------------
# # 🟢 GET CURRENT USER
# # -------------------------------------------------------------------
# @router.get("/me")
# def protected_route(user=Depends(get_current_user)):
#     return {"message": "You are authenticated!", "user": user}
