# GET /api/content/exam/attempts/{attempt_id}

## Summary
- Lấy chi tiết đầy đủ 1 lần làm bài: thông tin bài kiểm tra, tất cả câu hỏi, câu trả lời của học sinh, điểm từng câu
- Chỉ user tạo attempt mới được xem

## Auth & Permissions
- **Bearer Token** (Yêu cầu đăng nhập, chỉ xem attempt của chính mình)

## Path Parameters
| Parameter  | Type | Required | Description          |
|------------|------|----------|----------------------|
| attempt_id | int  | Yes      | ID lần làm bài       |

## Response
### Success (200)
```json
{
  "attempt": {
    "id": 1,
    "account_id": 5,
    "exercise_id": 1,
    "total_score": 7.5,
    "started_at": "2026-03-05T10:00:00",
    "finished_at": "2026-03-05T10:30:00",
    "created_at": "2026-03-05T10:30:00"
  },
  "exercise": {
    "id": 1,
    "specialization_id": 1,
    "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
    "difficulty_level": "easy",
    "time_limit": 45,
    "created_by": null,
    "created_at": "2026-02-28T00:00:00"
  },
  "responses": [
    {
      "id": 1,
      "attempt_id": 1,
      "question_id": 1,
      "text_answer": null,
      "teacher_comment": null,
      "score_earned": 1.0,
      "selected_choices": [
        {
          "id": 1,
          "response_id": 1,
          "selected_option_id": 2
        }
      ],
      "question": {
        "id": 1,
        "exercise_id": 1,
        "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
        "type": "single",
        "level": "easy",
        "point": 1.0,
        "correct_text": null,
        "explanation": "Biên độ A = 5 cm",
        "created_at": "2026-02-28T00:00:00",
        "options": [
          { "id": 1, "question_id": 1, "content": "3 cm", "is_correct": false },
          { "id": 2, "question_id": 1, "content": "5 cm", "is_correct": true },
          { "id": 3, "question_id": 1, "content": "2π cm", "is_correct": false },
          { "id": 4, "question_id": 1, "content": "π/3 cm", "is_correct": false }
        ]
      }
    },
    {
      "id": 2,
      "attempt_id": 1,
      "question_id": 3,
      "text_answer": "Năng lượng được bảo toàn trong dao động điều hòa",
      "teacher_comment": null,
      "score_earned": 0,
      "selected_choices": [],
      "question": {
        "id": 3,
        "exercise_id": 1,
        "content": "Giải thích sự bảo toàn năng lượng trong dao động điều hòa.",
        "type": "essay",
        "level": "hard",
        "point": 2.0,
        "correct_text": null,
        "explanation": null,
        "created_at": "2026-02-28T00:00:00",
        "options": []
      }
    }
  ],
  "total_questions": 2,
  "correct_count": 1,
  "total_points": 3.0,
  "earned_points": 1.0
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| attempt | object | Thông tin lần làm bài |
| exercise | object | Thông tin bài kiểm tra |
| responses | array | Chi tiết từng câu trả lời |
| responses[].selected_choices | array | Đáp án đã chọn (trắc nghiệm) |
| responses[].question | object | Câu hỏi + đáp án đúng |
| responses[].score_earned | float | Điểm đạt được cho câu này |
| total_questions | int | Tổng số câu hỏi |
| correct_count | int | Số câu đúng |
| total_points | float | Tổng điểm tối đa |
| earned_points | float | Tổng điểm đạt được |

### Error - Attempt not found (404)
```json
{
  "detail": "Attempt not found"
}
```

### Error - Access denied (403)
```json
{
  "detail": "Access denied"
}
```
