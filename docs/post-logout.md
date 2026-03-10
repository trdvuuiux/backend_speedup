# POST /api/auth/logout

## Summary
- Revoke a refresh token.

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
  "data": null
}
```

### Errors
- **(400 Bad Request)** - errorCode: `243` - Refresh token is missing
- **(400 Bad Request)** - errorCode: `202` - Request body has invalid data type or JSON

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
2. Decode refresh token to get user ID
3. Clear user tokens from database

## Notes
- Logout is idempotent for unknown tokens
- Clears both access and refresh tokens
