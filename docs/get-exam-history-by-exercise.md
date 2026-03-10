# GET /api/content/exam/history/exercise/{exercise_id}

## Summary
- Lấy lịch sử các lần làm bài của user hiện tại cho 1 bài kiểm tra cụ thể
- Sắp xếp theo thời gian mới nhất

## Auth & Permissions
- **Bearer Token** (Yêu cầu đăng nhập)

## Path Parameters
| Parameter   | Type | Required | Description             |
|-------------|------|----------|-------------------------|
| exercise_id | int  | Yes      | ID của bài kiểm tra     |

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
      "id": 5,
      "account_id": 5,
      "exercise_id": 1,
      "total_score": 7.0,
      "started_at": "2026-03-03T09:00:00",
      "finished_at": "2026-03-03T09:40:00",
      "created_at": "2026-03-03T09:40:00",
      "exercise": {
        "id": 1,
        "specialization_id": 1,
        "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
        "difficulty_level": "easy",
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
