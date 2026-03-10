# GET /api/content/topics/{topic_id}/specializations

## Summary
- Get all specializations (chuyên đề) by topic ID

## Auth & Permissions
- PUBLIC

## Path Parameters
| Parameter  | Type | Required | Description          |
|------------|------|----------|----------------------|
| topic_id   | int  | Yes      | ID of the topic      |

## Response
### Success (200)
```json
{
  "specializations": [
    {
      "id": 1,
      "topic_id": 101,
      "name": "Bài 1: Làm quen với Vật Lý",
      "description": null,
      "order_index": 1,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    },
    {
      "id": 2,
      "topic_id": 101,
      "name": "Bài 2: Các quy tắc an toàn trong phòng thực hành Vật Lý",
      "description": null,
      "order_index": 2,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

### Error - Topic not found (200)
```json
{
  "specializations": []
}
```
