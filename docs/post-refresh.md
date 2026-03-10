# POST /api/auth/refresh

## Summary
- Rotate refresh token and return a new token pair.

## Auth & Permissions
- PUBLIC

## Request
### Body
```json
{
  "refreshToken": "string"
}
```

## Required
| field         | location | required |
|---------------|----------|----------|
| refreshToken  | body     | x        |

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
- **(400 Bad Request)** - errorCode: `243` - Refresh token is missing
- **(400 Bad Request)** - errorCode: `202` - Request body has invalid data type or JSON
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Refresh token is invalid
- **(401 Unauthorized)** - errorCode: `234` - Refresh token is expired
- **(401 Unauthorized)** - errorCode: `248` - Refresh token is revoked or does not match
- **(404 Not Found)** - errorCode: `227` - User not found
- **(403 Forbidden)** - errorCode: `249` - User is blocked
- **(403 Forbidden)** - errorCode: `233` - Email is not verified

```json
{
  "success": false,
  "errorCode": "string",
  "errorMessage": "string",
  "data": null
}
```

## Logic (Internal)
1. Validate refresh token signature and claims
2. Validate refresh token against storage (database)
3. Verify user status (not blocked)
4. Issue new access token and rotate refresh token
5. Update tokens in database

## Notes
- Refresh token rotation revokes the previous token
- New token pair is returned on successful refresh
