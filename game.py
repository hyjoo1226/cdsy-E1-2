import json
import os
from models import Quiz
from utils import get_int_input

class QuizGame:
    # QuizGame 객체 초기화
    def __init__(self):
        self.quizzes = []          # Quiz 객체 리스트
        self.best_score = 0        # 최고 점수


    # ==================== 게임 진행 ====================
    # 메인 메뉴 출력 및 선택
    def show_menu(self):
        while True:
            print("\n" + "=" * 40)
            print("       🧠 심리학 퀴즈 게임")
            print("=" * 40)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 종료")
            print("=" * 40)

            choice = get_int_input("메뉴 선택: ", 1, 3)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                print("\n👋 게임을 종료합니다.")
                break

    # 퀴즈 풀기
    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        
        total = len(self.quizzes)
        correct_count = 0
        
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        print("=" * 40)
        
        for i, quiz in enumerate(self.quizzes, 1):
            # 문제 출력
            quiz.display_quiz(i)
            
            # 사용자 입력 예외처리
            user_input = get_int_input("\n정답 입력 (1~4): ", 1, 4)
            
            # 정답 확인
            if quiz.is_correct(user_input):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")
        
        # 결과 출력
        self.display_result(correct_count, total)

    # 게임 결과 출력
    def display_result(self, correct_count, total):
        score = int((correct_count / total) * 100)
        
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        print("=" * 40)

    # 퀴즈 추가
    def add_quiz(self):
        print("\n[ 퀴즈 추가 ]")
        print("=" * 40)

        # 문제 입력
        while True:
            question = input("문제를 입력하세요: ").strip()
            if question:
                break
            print("문제를 입력하세요.")

        # 선택지 4개 입력
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}번: ").strip()
                if choice:
                    choices.append(choice)
                    break
                print("선택지를 입력하세요.")

        # 정답 번호 입력
        answer = get_int_input("정답 번호 (1~4): ", 1, 4)

        # 힌트 입력 (선택사항)
        hint = input("힌트를 입력하세요 (없으면 Enter): ").strip()

        # Quiz 객체 생성 후 목록에 추가
        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint if hint else ""
        )
        self.quizzes.append(new_quiz)

        # 파일에 저장
        self.save_state()
        print(f"\n퀴즈가 추가되었습니다! (현재 총 {len(self.quizzes)}개)")


    #
    def save_state(self):
        state = {
            "best_score": self.best_score,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }
        
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
        
        print("💾 저장되었습니다.")