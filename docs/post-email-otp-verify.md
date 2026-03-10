# POST /api/auth/email/otp/verify

## Summary
- Verify OTP and issue new access and refresh tokens.

## Auth & Permissions
- USER (Bearer token required)

## Request
### Headers
- Authorization: Bearer {accessToken}

### Body
```json
{
  "otp": "string"
}
```

## Required
| field         | location   | required |
|---------------|------------|----------|
| otp           | body       | x        |
| Authorization | header    | x        |

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
- **(400 Bad Request)** - errorCode: `243` - OTP is missing
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid token
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid token type
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid token payload
- **(401 Unauthorized)** - errorCode: `238` - User not found
- **(401 Unauthorized)** - errorCode: `602` - OTP attempts exceeded
- **(401 Unauthorized)** - errorCode: `242` - OTP is expired
- **(401 Unauthorized)** - errorCode: `602` - Invalid OTP

```json
{
  "success": false,
  "errorCode": "string",
  "errorMessage": "string",
  "data": null
}
```

## Logic (Internal)
1. Resolve user from access token
2. Validate OTP (check expiry, attempts)
3. Mark email as verified
4. Generate new tokens

## Notes
- Max attempts is 5
- OTP TTL is 10 minutes
