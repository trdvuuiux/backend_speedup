# POST /api/auth/otp/resend

## Summary
- Resend OTP to user email (without authentication).
- User must exist and not be verified yet.

## Auth & Permissions
- PUBLIC

## Request
### Body
```json
{
  "email": "user@example.com"
}
```

## Required
| field | location | required |
|-------|----------|----------|
| email | body     | x        |

## Response
### Success (200)
```json
{
  "success": true,
  "errorCode": null,
  "errorMessage": null,
  "data": null
}
```

### Errors
- **(400 Bad Request)** - errorCode: `243` - Email is required
- **(404 Not Found)** - errorCode: `238` - Email does not exist
- **(400 Bad Request)** - errorCode: `255` - Email already verified

```json
{
  "success": false,
  "errorCode": "238",
  "errorMessage": "Email does not exist",
  "data": null
}
```

## Notes
- OTP will be sent to user's email
- New OTP will expire in 5 minutes
- Can only resend OTP if user is not verified yet
