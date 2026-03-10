# POST /api/auth/login

## Summary
- Authenticate with email and password and return access and refresh tokens.

## Auth & Permissions
- PUBLIC

## Request
### Body
```json
{
  "email": "string",
  "password": "string"
}
```

## Required
| field    | location | required |
|----------|----------|----------|
| email    | body     | x        |
| password | body     | x        |

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
- **(400 Bad Request)** - errorCode: `243` - Required fields are missing (email, password)
- **(400 Bad Request)** - errorCode: `BAD_REQUEST` - Email format is invalid
- **(400 Bad Request)** - errorCode: `202` - Request body has invalid data type or JSON
- **(401 Unauthorized)** - errorCode: `238` - Email does not exist
- **(401 Unauthorized)** - errorCode: `239` - Password is incorrect
- **(403 Forbidden)** - errorCode: `FORBIDDEN` - User is blocked

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
3. Verify password using bcrypt
4. Generate access and refresh tokens
5. Update tokens in database
6. Return token pair

## Notes
- Token expiry values are in seconds
- Access token expires in 30 minutes (1800 seconds)
- Refresh token expires in 7 days (604800 seconds)
