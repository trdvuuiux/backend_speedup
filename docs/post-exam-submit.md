# POST /api/content/exam/submit

## Summary
- Nộp bài kiểm tra, tự động chấm điểm trắc nghiệm
- Câu hỏi single/multi choice: chấm điểm tự động
- Câu hỏi essay: lưu lại, giáo viên chấm sau (tự động chấm nếu có `correct_text`)

## Auth & Permissions
- **Bearer Token** (Yêu cầu đăng nhập)

## Request
```json
{
  "exercise_id": 1,
  "answers": [
    {
      "question_id": 1,
      "selected_option_ids": [2],
      "text_answer": null
    },
    {
      "question_id": 2,
      "selected_option_ids": [6],
      "text_answer": null
    },
    {
      "question_id": 3,
      "selected_option_ids": [],
      "text_answer": "Đáp án tự luận của học sinh"
    }
  ]
}
```

### Request Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| exercise_id | int | Yes | ID bài kiểm tra |
| answers | array | Yes | Danh sách câu trả lời |
| answers[].question_id | int | Yes | ID câu hỏi |
| answers[].selected_option_ids | int[] | No | Danh sách ID đáp án đã chọn (cho trắc nghiệm) |
| answers[].text_answer | string | No | Câu trả lời tự luận (cho essay) |

## Response
### Success (200)
```json
{
  "attempt_id": 1,
  "total_score": 8.5,
  "total_questions": 10,
  "correct_count": 8,
  "total_points": 10.0,
  "earned_points": 8.5
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| attempt_id | int | ID lần làm bài |
| total_score | float | Điểm tổng (thang 10) |
| total_questions | int | Tổng số câu hỏi |
| correct_count | int | Số câu đúng |
| total_points | float | Tổng điểm tối đa |
| earned_points | float | Điểm đạt được |

### Error - Exercise not found (404)
```json
{
  "detail": "Exercise not found"
}
```

### Error - Unauthorized (401)
```json
{
  "detail": "Invalid token"
}
```

## Scoring Logic
- **Single choice**: Đúng nếu chọn đúng 1 đáp án correct
- **Multi choice**: Đúng nếu chọn đúng TẤT CẢ đáp án correct (không thừa, không thiếu)
- **Essay**: Tự động chấm nếu có `correct_text` (so sánh không phân biệt hoa thường), nếu không thì điểm = 0 chờ giáo viên chấm
- **Điểm tổng**: `(earned_points / total_points) * 10`
