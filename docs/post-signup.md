# POST /api/auth/signup

## Summary
- Register a new user and return access and refresh tokens.
- If user exists but not verified, will resend OTP.

## Auth & Permissions
- PUBLIC

## Request
### Body
```json
{
  "email": "string",
  "password": "string",
  "fullName": "string",
  "phoneNumber": "string | null",
  "avatarUrl": "string | null",
  "address": "string | null"
}
```

## Required
| field    | location | required |
|----------|----------|----------|
| email    | body     | x        |
| password | body     | x        |
| fullName | body     | x        |

## Response
### Success
```json
{
  "success": true,
  "errorCode": null,
  "errorMessage": null,
  "data": {
    "accessToken": "string",
    "refreshToken": "string",
    "accessExpireIn": 1800,
    "refreshExpireIn": 604800
  }
}
```

### Errors
- **(400 Bad Request)** - errorCode: `243` - Required fields are missing (email, password, fullName)
- **(400 Bad Request)** - errorCode: `BAD_REQUEST` - Email format or field length is invalid
- **(400 Bad Request)** - errorCode: `202` - Request body has invalid data type or JSON
- **(409 Conflict)** - errorCode: `255` - Email already verified
- **(400 Bad Request)** - errorCode: `221` - Default role not found

```json
{
  "success": false,
  "errorCode": "string",
  "errorMessage": "string",
  "data": null
}
```

## Logic (Internal)
1. Validate request payload (email format, password length, required fields)
2. Check if email already exists in database
   - If user exists AND verified → return error "Email already exists"
   - If user exists BUT not verified → resend OTP and return tokens
3. Generate OTP for email verification
4. Send OTP to user's email
5. Hash password and create user with role 'student'
6. Generate access and refresh tokens
7. Return tokens to client

## Notes
- OTP is sent separately via email for verification
- Default role is 'student'
- Password is hashed using bcrypt
- If user exists but not verified, signup will resend OTP (allows retry)