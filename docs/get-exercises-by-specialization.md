# GET /api/content/specializations/{specialization_id}/exercises

## Summary
- Get all exercises (bài kiểm tra) by specialization ID

## Auth & Permissions
- PUBLIC

## Path Parameters
| Parameter          | Type | Required | Description                |
|--------------------|------|----------|----------------------------|
| specialization_id  | int  | Yes      | ID of the specialization   |

## Response
### Success (200)
```json
{
  "exercises": [
    {
      "id": 1,
      "specialization_id": 1,
      "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
      "difficulty_level": "easy",
      "time_limit": 45,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    },
    {
      "id": 2,
      "specialization_id": 1,
      "name": "Bài kiểm tra: Dao động điều hòa - Nâng cao",
      "difficulty_level": "hard",
      "time_limit": 60,
      "created_by": 1,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

### No exercises found (200)
```json
{
  "exercises": []
}
```
