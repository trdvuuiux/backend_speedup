# GET /api/content/exam/history

## Summary
- Lấy lịch sử tất cả các lần làm bài của user hiện tại
- Sắp xếp theo thời gian mới nhất

## Auth & Permissions
- **Bearer Token** (Yêu cầu đăng nhập)

## Response
### Success (200)
```json
{
  "attempts": [
    {
      "id": 1,
      "account_id": 5,
      "exercise_id": 1,
      "total_score": 8.5,
      "started_at": "2026-03-05T10:00:00",
      "finished_at": "2026-03-05T10:30:00",
      "created_at": "2026-03-05T10:30:00",
      "exercise": {
        "id": 1,
        "specialization_id": 1,
        "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
        "difficulty_level": "easy",
        "time_limit": 45,
        "created_by": null,
        "created_at": "2026-02-28T00:00:00"
      }
    },
    {
      "id": 2,
      "account_id": 5,
      "exercise_id": 3,
      "total_score": 6.0,
      "started_at": "2026-03-04T14:00:00",
      "finished_at": "2026-03-04T14:45:00",
      "created_at": "2026-03-04T14:45:00",
      "exercise": {
        "id": 3,
        "specialization_id": 2,
        "name": "Bài kiểm tra: Con lắc lò xo",
        "difficulty_level": "medium",
        "time_limit": 45,
        "created_by": null,
        "created_at": "2026-02-28T00:00:00"
      }
    }
  ]
}
```

### No attempts (200)
```json
{
  "attempts": []
}
```

### Error - Unauthorized (401)
```json
{
  "detail": "Invalid token"
}
```
