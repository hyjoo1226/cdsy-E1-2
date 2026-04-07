import json
import os
from models import Quiz
from utils import get_int_input

class QuizGame:
    # QuizGame 객체 초기화
    def __init__(self):
        self.quizzes = []          # Quiz 객체 리스트
        self.best_score = 0        # 최고 점수

        # 퀴즈 진행 상황
        self.current_session = {
            "remaining_quizzes": [],  # 아직 안 푼 퀴즈 ID 목록
            "correct_count": 0,       # 현재까지 맞춘 개수
            "total": 0                # 전체 문제 수
        }


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
        
        # 이어하기 여부 확인
        remaining_ids = self.current_session.get("remaining_quizzes", [])
        
        if remaining_ids:
            print("\n🔄 지난번 중단된 퀴즈부터 이어서 시작합니다!")
            target_quizzes = [q for q in self.quizzes if q.id in remaining_ids]
            total = self.current_session["total"]
            correct_count = self.current_session["correct_count"]
        else:
            target_quizzes = self.quizzes
            total = len(self.quizzes)
            correct_count = 0
            
            # 세션 초기화
            self.current_session["total"] = total
            self.current_session["correct_count"] = 0
            self.current_session["remaining_quizzes"] = [quiz.id for quiz in self.quizzes]
            print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        print("=" * 40)
        
        # 퀴즈 풀이 루프
        for quiz in target_quizzes:
            # 문제 출력
            current_index = total - len(self.current_session["remaining_quizzes"]) + 1
            quiz.display_quiz(current_index)
            
            # 사용자 입력 예외처리
            user_input = get_int_input("\n정답 입력 (1~4): ", 1, 4)
            
            # 정답 확인
            if quiz.is_correct(user_input):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")

            # 진행 상황 업데이트
            self.current_session["correct_count"] = correct_count
            self.current_session["remaining_quizzes"].remove(quiz.id)
            self.save_state()
        
        # 퀴즈 풀기 종료 후 세션 초기화
        self.reset_session()

        # 결과 출력 및 저장
        self.display_result(correct_count, total)
        self.save_state()

    # 게임 결과 출력
    def display_result(self, correct_count, total):
        score = int((correct_count / total) * 100)
        
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        # 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            print(f"🎉 새로운 최고 점수! {score}점")
        else:
            print(f"📊 현재 최고 점수: {self.best_score}점")
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


    # ==================== 파일 관리 ====================
    # 게임 상태 저장 (최고 점수, 퀴즈 목록, 현재 진행 상황)
    def save_state(self):
        state = {
            "best_score": self.best_score,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "current_session": self.current_session
        }
        
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
        
        print("💾 저장되었습니다.")

    # 게임 상태 불러오기
    def load_state(self):
        # 1. 파일 존재 여부 확인
        if not os.path.exists("state.json"):
            print("📂 저장 파일 없음 → 기본 데이터로 시작합니다.")
            return False

        # 2. 파일 읽기 및 JSON 파싱
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                state = json.load(f)

        except (json.JSONDecodeError, UnicodeDecodeError):
            print("⚠️ 저장 파일이 손상되었습니다 → 기본 데이터로 복구합니다.")
            os.remove("state.json")
            return False

        # 3. 필수 키 존재 여부 확인
        if "best_score" not in state or "quizzes" not in state:
            print("⚠️ 저장 파일 구조가 올바르지 않습니다 → 기본 데이터로 복구합니다.")
            os.remove("state.json")
            return False

        # 4. 퀴즈 목록 복구
        loaded_quizzes = []

        for i, quiz_data in enumerate(state["quizzes"]):
            try:
                quiz = Quiz.from_dict(quiz_data)
                loaded_quizzes.append(quiz)
            except Exception:
                print(f"⚠️ {i+1}번째 퀴즈 데이터 손상 → 기본 데이터로 복구합니다.")
                os.remove("state.json")
                return False

        self.quizzes = loaded_quizzes

        # 5. 최고 점수 복구
        try:
            self.best_score = int(state["best_score"])
        except (ValueError, TypeError):
            print("⚠️ 최고 점수 데이터 손상 → 0점으로 초기화합니다.")
            self.best_score = 0

        # 6. 현재 진행 상황 복구
        session = state.get("current_session", {})
        valid_remaining = [] # 최종적으로 이어서 풀 목록

        try:
            remaining = session.get("remaining_quizzes", [])
            correct_count = int(session.get("correct_count", 0))
            total = int(session.get("total", 0))

            # 퀴즈 ID 유효성 검사
            valid_ids = {quiz.id for quiz in self.quizzes}
            valid_remaining = [uid for uid in remaining if uid in valid_ids]

            is_session_corrupted = False
            if (remaining and len(remaining) != len(valid_remaining)) or \
               (correct_count < 0 or total < 0 or correct_count > total):
                is_session_corrupted = True

            if is_session_corrupted:
                print("⚠️ 세션 데이터가 유효하지 않아 초기화합니다.")
                self.reset_session(save=True)
                valid_remaining = []

            else:
                self.current_session = {
                    "remaining_quizzes": valid_remaining,
                    "correct_count": correct_count,
                    "total": total
                }

        except (ValueError, TypeError):
            print("⚠️ 세션 데이터 형식이 잘못되어 초기화합니다.")
            self.reset_session(save=True)
            valid_remaining = []

        # 7. 이어하기 확인
        if valid_remaining:
            print(f"✅ 로드 완료! (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
            print(f"⚠️ 이전에 중단된 퀴즈가 있어요! ({len(valid_remaining)}문제 남음)")
            
            while True:
                choice = input("이어서 풀까요? (y/n): ").strip().lower()
                if choice in ['y', 'n']:
                    break
                print("⚠️ 'y' 또는 'n'만 입력해주세요.")

            # 이어하기 취소 시 세션 초기화
            if choice == "n":
                self.reset_session(save=True)
                print("🧹 이전 세션 정보가 초기화되었습니다.")
                valid_remaining = []
        else:
            # 이어할 목록이 없거나, 위에서 손상되어 초기화된 경우
            print(f"✅ 로드 완료! (최고점수 {self.best_score}점)")

        return True
    


    # 세션 초기화 공통 메서드
    def reset_session(self, save=False):
        self.current_session = {
            "remaining_quizzes": [],
            "correct_count": 0,
            "total": 0
        }
        # 필요에 따라 초기화 즉시 파일에 저장
        if save:
            self.save_state()