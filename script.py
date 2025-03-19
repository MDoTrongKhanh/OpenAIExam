import random
import datetime
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Sử dụng API Key từ môi trường

def generate_question(prompt):
    """Gọi OpenAI API để tạo câu hỏi theo cú pháp mới."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Bạn là một giáo viên tạo đề kiểm tra."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def create_exam():
    """Tạo đề kiểm tra với 5 câu trắc nghiệm và 3 câu tự luận."""
    exam_date = datetime.datetime.now().strftime("%Y-%m-%d")
    subject = "Toán học"
    level = "Lớp 7"
    
    exam_content = f"# Đề kiểm tra môn {subject} - {level}\n"
    exam_content += f"## Ngày: {exam_date}\n\n"
    
    # Tạo câu hỏi trắc nghiệm
    exam_content += "## Phần 1: Trắc nghiệm (Chọn 1 đáp án đúng)\n"
    for i in range(1, 6):
        question = generate_question(f"Hãy tạo một câu hỏi trắc nghiệm toán lớp 7 với 4 đáp án.")
        exam_content += f"**Câu {i}:** {question}\n\n"
    
    # Tạo câu hỏi tự luận
    exam_content += "## Phần 2: Tự luận\n"
    for i in range(1, 4):
        question = generate_question(f"Hãy tạo một bài toán tự luận lớp 7.")
        exam_content += f"**Câu {i}:** {question}\n\n"
    
    return exam_content

def save_and_commit_exam():
    """Lưu đề thi vào file Markdown riêng và commit lên GitHub."""
    exam_text = create_exam()
    exam_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"exam_{exam_date}.md"
    
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(exam_text)
    
    os.system(f"git add {file_name}")
    os.system(f"git commit -m 'Thêm đề kiểm tra ngày {exam_date}'")
    os.system("git push origin main")

if __name__ == "__main__":
    save_and_commit_exam()
