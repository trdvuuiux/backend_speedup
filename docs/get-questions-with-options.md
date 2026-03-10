# GET /api/content/exercises/{exercise_id}/questions-with-options

## Summary
- Get all questions with their answer options by exercise ID (câu hỏi kèm đáp án)

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
      "created_at": "2026-02-28T00:00:00",
      "options": [
        {
          "id": 1,
          "question_id": 1,
          "content": "3 cm",
          "is_correct": false
        },
        {
          "id": 2,
          "question_id": 1,
          "content": "5 cm",
          "is_correct": true
        },
        {
          "id": 3,
          "question_id": 1,
          "content": "2π cm",
          "is_correct": false
        },
        {
          "id": 4,
          "question_id": 1,
          "content": "π/3 cm",
          "is_correct": false
        }
      ]
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
