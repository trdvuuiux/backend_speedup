# GET /api/content/grades/{grade_id}/topics

## Summary
- Get all topics by grade ID

## Auth & Permissions
- PUBLIC

## Response
### Success (200)
```json
{
  "topics": [
    {
      "id": 1,
      "grade_id": 1,
      "name": "Chương 1: Động học chất điểm",
      "description": "Nghiên cứu về chuyển động cơ học",
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```
