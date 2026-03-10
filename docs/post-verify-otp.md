# POST /api/auth/otp/verify

## Summary
- Verify OTP and activate user account.

## Auth & Permissions
- PUBLIC

## Request
### Body
```json
{
  "email": "string",
  "otp": "string"
}
```

## Required
| field  | location | required |
|--------|----------|----------|
| email  | body     | x        |
| otp    | body     | x        |

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
- **(400 Bad Request)** - errorCode: `243` - Email and OTP are required
- **(400 Bad Request)** - errorCode: `202` - Request body has invalid data type or JSON
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid or expired OTP
- **(404 Not Found)** - errorCode: `227` - User not found

```json
{
  "success": false,
  "errorCode": "string",
  "errorMessage": "string",
  "data": null
}
```

## Logic (Internal)
1. Validate request payload
2. Look up user by email
3. Verify OTP matches and is not expired (5 minutes)
4. Clear OTP from user record
5. Generate new tokens
6. Update tokens in database

## Notes
- OTP expires after 5 minutes
- User must provide correct OTP to verify email
