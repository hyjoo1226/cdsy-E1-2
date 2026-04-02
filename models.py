class Quiz:
    # Quiz 객체 초기화   
    def __init__(self, quiz_id, question, choices, answer, hint=None):
        self.id = quiz_id   # 문제 고유 ID (int)
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
        if quiz_id is None:
            raise ValueError("퀴즈 ID가 없습니다.")
        
        return cls(
            quiz_id=quiz_id,
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint"),
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