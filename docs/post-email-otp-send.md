# POST /api/auth/otp/send

## Summary
- Send a verification OTP to the authenticated user email.

## Auth & Permissions
- USER (Bearer token required)

## Request
### Headers
- Authorization: Bearer {accessToken}

## Required
| field         | location   | required |
|---------------|------------|----------|
| Authorization | header    | x        |

## Response
### Success
```json
{
  "success": true,
  "errorCode": null,
  "errorMessage": null,
  "data": null
}
```

### Errors
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid token
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid token type
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid token payload
- **(401 Unauthorized)** - errorCode: `238` - User not found

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
2. Generate new OTP
3. Save OTP to database
4. Send OTP via email

## Notes
- OTP TTL is 10 minutes
- Max attempts is 5 for verification
