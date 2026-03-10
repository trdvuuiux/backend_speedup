# PUT /api/auth/profile

## Summary
- Update current user's profile.

## Auth & Permissions
- Bearer Token (Access Token)

## Request
### Headers
```
Authorization: Bearer <access_token>
```

### Body
```json
{
  "fullName": "Nguyen Van A",
  "phoneNumber": "0123456789",
  "avatarUrl": "https://example.com/avatar.jpg",
  "address": "Ha Noi"
}
```

## Required
| field       | location | required |
|-------------|----------|----------|
| fullName    | body     |          |
| phoneNumber | body     |          |
| avatarUrl   | body     |          |
| address     | body     |          |

All fields are optional.

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
- **(401 Unauthorized)** - errorCode: `UNAUTHORIZED` - Invalid or expired token
- **(404 Not Found)** - errorCode: `238` - User not found

```json
{
  "success": false,
  "errorCode": "UNAUTHORIZED",
  "errorMessage": "Invalid token",
  "data": null
}
```

## Notes
- Requires valid access token in Authorization header
- Only provided fields will be updated
- Other fields remain unchanged
