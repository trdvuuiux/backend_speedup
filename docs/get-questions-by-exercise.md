# GET /api/content/exercises/{exercise_id}/questions

## Summary
- Get all questions by exercise ID (chỉ câu hỏi, không kèm đáp án)

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
  "questions": [
    {
      "id": 1,
      "exercise_id": 1,
      "content": "Một vật dao động điều hòa với phương trình x = 5cos(2πt + π/3) cm. Biên độ dao động là?",
      "type": "single",
      "level": "easy",
      "point": 1.0,
      "correct_text": null,
      "explanation": "Biên độ A = 5 cm, đọc trực tiếp từ phương trình.",
      "created_at": "2026-02-28T00:00:00"
    },
    {
      "id": 2,
      "exercise_id": 1,
      "content": "Chu kỳ dao động điều hòa T liên hệ với tần số góc ω bởi công thức nào?",
      "type": "single",
      "level": "medium",
      "point": 1.0,
      "correct_text": null,
      "explanation": "T = 2π/ω",
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

### No questions found (200)
```json
{
  "questions": []
}
```
