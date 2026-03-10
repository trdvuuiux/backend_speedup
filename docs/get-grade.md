# GET /api/content/grades/{grade_id}

## Summary
- Get grade by ID

## Auth & Permissions
- PUBLIC

## Response
### Success (200)
```json
{
  "id": 1,
  "name": "Lớp 10",
  "description": "Mô tả lớp 10"
}
```

### Errors
- **(404 Not Found)** - Grade not found
