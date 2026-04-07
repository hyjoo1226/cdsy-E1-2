import uuid

class Quiz:
    # Quiz 객체 초기화   
    def __init__(self, question, choices, answer, hint=None, quiz_id=None):
        self.id = quiz_id if quiz_id else str(uuid.uuid4())    # 문제 고유 ID (str)
        self.question = question    # 문제 내용 (str)
        self.choices = choices  # 4개의 선택지 (list of str)
        self.answer = answer    # 정답 번호 1~4 (int)
        self.hint = hint    # 문제 관련 힌트 (str, optional)

    # 문제 출력
        # index: 문제 번호 (int)
    def display_quiz(self, index):
        print(f"\n[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    # 힌트 출력
    def display_hint(self):
        if self.hint:
            print(f"💡 힌트: {self.hint}")
        else:
            print("이 문제에는 힌트가 없습니다.")

    # 정답 확인
        # user_input: 사용자가 입력한 번호 (int)
    def is_correct(self, user_input):
        return user_input == self.answer

    # 데이터 불러오기(JSON 데이터에서 Quiz 객체 생성)
        # data: JSON 데이터 (dict)
    @classmethod
    def from_dict(cls, data):
        quiz_id=data.get("id")
        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")
        hint = data.get("hint")

        # 데이터 유효성 검사
        if None in [quiz_id, question, choices, answer, hint]:
            raise ValueError("필수 데이터 키가 누락되었습니다.")
        
        if not isinstance(quiz_id, str) or not quiz_id.strip():
            raise ValueError("ID는 비어있을 수 없는 문자열이어야 합니다.")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어있을 수 없는 문자열이어야 합니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        
        if any(not str(c).strip() for c in choices):
            raise ValueError("비어있는 선택지가 포함되어 있습니다.")
        
        if not isinstance(answer, int) or not (1 <= answer <= 4):
            raise ValueError("정답 번호는 1~4 사이의 숫자여야 합니다.")
        
        return cls(
            quiz_id=quiz_id,
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=hint if hint else ""
        )

    #  데이터 저장하기(Quiz 객체를 JSON 데이터로 변환)
    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }