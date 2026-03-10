# GET /api/auth/profile

## Summary
- Get current user's profile.

## Auth & Permissions
- Bearer Token (Access Token)

## Request
### Headers
```
Authorization: Bearer <access_token>
```

## Response
### Success (200)
```json
{
  "id": 1,
  "email": "user@example.com",
  "fullName": "Nguyen Van A",
  "phoneNumber": "0123456789",
  "avatarUrl": "https://example.com/avatar.jpg",
  "address": "Ha Noi",
  "role": "student",
  "emailVerified": true,
  "subscriptionType": "plus",
  "subscriptionStart": "2026-02-28T00:00:00",
  "subscriptionEnd": "2026-03-28T00:00:00",
  "isActive": true
}
```

### Errors
- **(401 Unauthorized)** - Invalid or expired token

## Notes
- subscriptionType: `free`, `plus`, `pro`, `vip`, `max`
