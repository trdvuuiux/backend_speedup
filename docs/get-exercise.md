# GET /api/content/exercises/{exercise_id}

## Summary
- Get exercise detail by ID (tên bài kiểm tra, độ khó, thời gian...)

## Auth & Permissions
- PUBLIC

## Path Parameters
| Parameter    | Type | Required | Description            |
|--------------|------|----------|------------------------|
| exercise_id  | int  | Yes      | ID of the exercise     |

## Response
### Success (200)
```json
{
  "id": 1,
  "specialization_id": 1,
  "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
  "difficulty_level": "easy",
  "time_limit": 45,
  "created_by": null,
  "created_at": "2026-02-28T00:00:00"
}
```

### Error - Not found (200)
```json
{
  "success": false,
  "errorCode": "404",
  "errorMessage": "Exercise not found",
  "data": null
}
```
