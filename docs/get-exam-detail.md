# GET /api/content/exercises/{exercise_id}/exam

## Summary
- Get full exam detail: exercise info + all questions with answer options
- Dùng để tạo bài thi cho học sinh — lấy 1 lần đầy đủ thông tin bài kiểm tra

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
  "exercise": {
    "id": 1,
    "specialization_id": 1,
    "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
    "difficulty_level": "easy",
    "time_limit": 45,
    "created_by": null,
    "created_at": "2026-02-28T00:00:00"
  },
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
      "created_at": "2026-02-28T00:00:00",
      "options": [
        {
          "id": 5,
          "question_id": 2,
          "content": "T = ω/2π",
          "is_correct": false
        },
        {
          "id": 6,
          "question_id": 2,
          "content": "T = 2π/ω",
          "is_correct": true
        },
        {
          "id": 7,
          "question_id": 2,
          "content": "T = πω",
          "is_correct": false
        },
        {
          "id": 8,
          "question_id": 2,
          "content": "T = 2ω/π",
          "is_correct": false
        }
      ]
    }
  ]
}
```

### Error - Exercise not found (200)
```json
{
  "success": false,
  "errorCode": "404",
  "errorMessage": "Exercise not found",
  "data": null
}
```

## Notes
- API này trả về đầy đủ: thông tin bài kiểm tra + tất cả câu hỏi + đáp án
- Phù hợp để frontend gọi 1 lần khi học sinh bắt đầu làm bài
- `time_limit` tính bằng phút
- `is_correct` cho biết đáp án đúng (có thể ẩn ở frontend khi đang làm bài)
