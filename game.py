import json
import os
from datetime import datetime
import random
from models import Quiz
from utils import get_int_input

class QuizGame:
    # QuizGame 객체 초기화
    def __init__(self):
        self.quizzes = []          # Quiz 객체 리스트
        self.best_score = 0        # 최고 점수
        self.history = []           # 게임 플레이 기록
        
        # 퀴즈 진행 상황
        self.current_session = {
            "remaining_quizzes": [],  # 아직 안 푼 퀴즈 ID 목록
            "correct_count": 0,       # 현재까지 맞춘 개수
            "score_points": 0.0,      # 실제 계산용 점수 (힌트 사용 감점 반영)
            "total": 0,                # 전체 문제 수
            "draft": None              # 퀴즈 추가 중 입력 임시 저장
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
            print("3. 퀴즈 목록")
            print("4. 퀴즈 삭제")
            print("5. 기록 및 점수")
            print("6. 종료")
            print("=" * 40)

            choice = get_int_input("메뉴 선택: ", 1, 6)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.show_history()
            elif choice == 6:
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
            score_points = self.current_session.get("score_points", 0.0)

        else:
            print("\n[ 🎲 출제 방식 선택 ]")
            print("1. 등록순 풀기")
            print("2. 랜덤 풀기")
            # 게임 모드 선택
            mode = get_int_input("선택: ", 1, 2)
            target_quizzes = self.quizzes[:]
            if mode == 2:
                random.shuffle(target_quizzes)
                print("🔀 문제를 무작위로 섞었습니다!")
            else:
                print("📋 등록된 순서대로 시작합니다.")

            # 문제 수 선택
            max_quizzes = len(target_quizzes)
            print(f"\n[ 📝 문제 수 선택 ] (최대 {max_quizzes}문제)")
            num_to_solve = get_int_input(f"몇 문제를 푸시겠습니까? (1~{max_quizzes}): ", 1, max_quizzes)
            target_quizzes = target_quizzes[:num_to_solve]

            total = num_to_solve
            score_points = 0.0  # 실제 계산용 점수 (0.5점 포함)
            correct_count = 0   # 맞힌 문제 수
            
            # 세션 초기화
            self.current_session["total"] = total
            self.current_session["correct_count"] = 0
            self.current_session["score_points"] = 0.0
            self.current_session["remaining_quizzes"] = [quiz.id for quiz in target_quizzes]
            print(f"\n🚀 퀴즈를 시작합니다! (총 {total}문제 중 {num_to_solve}문제 선택)")

        print("=" * 40)
        
        # 퀴즈 풀이 루프
        for quiz in target_quizzes:
            # 문제 출력
            current_index = total - len(self.current_session["remaining_quizzes"]) + 1
            hint_used = False # 힌트 사용 여부

            while True:
                quiz.display_quiz(current_index)
                print("\n💡 힌트가 필요하면 '0'을 입력하세요. (사용 시 획득 점수 감점)")
                user_input = get_int_input("정답 입력 (1~4, 힌트 0): ", 0, 4)

                if user_input == 0:
                    if not hint_used:
                        quiz.display_hint()
                        hint_used = True
                    else:
                        print("⚠️ 이미 힌트를 사용했습니다!")
                    continue
                else:
                    break
            
            # 정답 확인
            if quiz.is_correct(user_input):
                correct_count += 1
                if hint_used:
                    print("✅ 정답입니다! (힌트 사용으로 50% 점수만 획득)")
                    score_points += 0.5
                else:
                    print("✅ 정답입니다!")
                    score_points += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")

            # 진행 상황 업데이트
            self.current_session["correct_count"] = correct_count
            self.current_session["score_points"] = score_points
            self.current_session["remaining_quizzes"].remove(quiz.id)
            self.save_state()
        
        # 퀴즈 풀기 종료 후 세션 초기화
        self.reset_session()

        # 결과 출력 및 저장
        self.display_result(correct_count, score_points, total)
        self.save_state()

    # 게임 결과 출력
    def display_result(self, correct_count, score_points, total):
        score = int((score_points / total) * 100)

        now_time = datetime.now().strftime("%Y-%m-%d %H:%M")    # 현재 시간
        # 히스토리 객체 생성 및 추가
        record = {
            "date": now_time,
            "total": total,
            "correct": correct_count,
            "score": score
        }
        self.history.append(record) # 기록 저장

        
        final_score = int((score_points / total) * 100)
        
        print("\n" + "=" * 40)
        print(f"📊 통계: {total}문제 중 {correct_count}문제를 맞혔습니다!")
        print(f"🏆 최종 점수: {final_score}점 (힌트 사용 감점 반영)")

        # 최고 점수 갱신
        if final_score > self.best_score:
            self.best_score = final_score
            print(f"🎉 새로운 최고 점수! {final_score}점")
        else:
            print(f"📊 현재 최고 점수: {self.best_score}점")
        print("=" * 40)

    # 퀴즈 추가
    def add_quiz(self):
        print("\n[ 퀴즈 추가 ]")
        print("=" * 40)

        # 기존 초안 있으면 불러오기
        draft = self.current_session.get("draft")

        if draft:
            print("📝 작성 중이던 퀴즈가 있습니다.")
            print(f"질문: {draft.get('question', '(미입력)')}")

            while True:
                choice = input("이어서 작성할까요? (y/n): ").strip().lower()
                if choice in ['y', 'n']: break
                print("⚠️ 'y' 또는 'n'만 입력해주세요.")

            if choice == 'n':
                self.current_session["draft"] = None
                self.save_state()
                return

        if draft is None:
            draft = {"question": "", "choices": [], "answer": 0, "hint": None }

        # 문제 입력
        if not draft["question"]:
            while True:
                question = input("문제를 입력하세요: ").strip()
                if question:
                    draft["question"] = question
                    self.current_session["draft"] = draft
                    self.save_state()
                    break
                print("문제를 입력하세요.")

        # 선택지 입력
        while len(draft["choices"]) < 4:
            i = len(draft["choices"]) + 1
            while True:
                choice = input(f"선택지 {i}번: ").strip()
                if choice:
                    draft["choices"].append(choice)
                    self.current_session["draft"] = draft
                    self.save_state()
                    break
                print(f"{i}번 선택지를 입력하세요.")

        # 정답 번호 입력
        if draft.get("answer") == 0:
            answer = get_int_input("정답 번호 (1~4): ", 1, 4)
            draft["answer"] = answer
            self.current_session["draft"] = draft
            self.save_state()

        # 힌트 입력 (선택사항)
        if draft.get("hint") is None:
            hint = input("힌트를 입력하세요 (없으면 Enter): ").strip()
            draft["hint"] = hint if hint else ""
            self.current_session["draft"] = draft
            self.save_state()

        # Quiz 객체 생성 후 목록에 추가
        try:
            new_quiz = Quiz(
                question=draft["question"],
                choices=draft["choices"],
                answer=draft["answer"],
                hint=draft["hint"]
            )
            self.quizzes.append(new_quiz)
            
            # 초안 삭제
            self.current_session["draft"] = None
            self.save_state()
            
            print(f"\n✅ 퀴즈가 성공적으로 추가되었습니다! (현재 총 {len(self.quizzes)}개)")
            
        except Exception as e:
            print(f"⚠️ 퀴즈 생성 중 오류 발생: {e}")


    # 퀴즈 목록 보기
    def list_quizzes(self):
        print("\n[ 📚 저장된 퀴즈 목록 ]")
        print("=" * 40)

        # 퀴즈가 없는 경우
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            print("=" * 40)
            return

        # 퀴즈 목록 출력
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"{i}. {quiz.question}")
        
        print("-" * 40)
        print(f"총 {len(self.quizzes)}개의 문제가 등록되어 있습니다.")
        print("=" * 40)
        
        input("\n계속하려면 Enter를 누르세요...")

    # 최고 점수 및 기록 확인
    def show_history(self):
        print("\n[ 📊 퀴즈 도전 기록 ]")
        print("=" * 50)
        print(f"⭐ 현재 최고 점수: {self.best_score}점")
        print("-" * 50)

        if not self.history:
            print("아직 도전 기록이 없습니다.")
        else:
            print(f"{'일시':<16} | {'문제수':<2} | {'정답':<1} | {'점수':<2}")
            print("-" * 50)
            for rec in reversed(self.history):
                print(f"{rec['date']:<18} | {rec['total']:^6} | {rec['correct']:^4} | {rec['score']:>3}점")

        print("=" * 50)
        input("\n계속하려면 Enter를 누르세요...")

    # 퀴즈 삭제 기능
    def delete_quiz(self):
        print("\n[ 🗑️ 퀴즈 삭제 ]")
        print("=" * 40)

        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return

        # 현재 목록 출력
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"{i}. {quiz.question}")
        
        print("-" * 40)
        print("0. 취소 (메인 메뉴로)")

        # 삭제할 번호 선택
        choice = get_int_input(f"삭제할 퀴즈 번호를 입력하세요 (0~{len(self.quizzes)}): ", 0, len(self.quizzes))

        if choice == 0:
            print("❌ 삭제가 취소되었습니다.")
            return

        # 삭제 후 저장
        target_index = choice - 1
        deleted_quiz = self.quizzes.pop(target_index)

        self.save_state()
        print(f"\n✅ 삭제 완료: \"{deleted_quiz.question}\"")
        print(f"현재 남은 퀴즈: {len(self.quizzes)}개")

    # ==================== 파일 관리 ====================
    # 게임 상태 저장 (최고 점수, 퀴즈 목록, 현재 진행 상황)
    def save_state(self):
        state = {
            "best_score": self.best_score,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "history": self.history,
            "current_session": self.current_session
        }
        
        temp_file = "state.json.tmp"
        target_file = "state.json"

        try:
            # 1. 임시 파일에 먼저 기록
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=4)
            
            # 2. 쓰기가 완벽히 끝나면 기존 파일에 덮어쓰기
            os.replace(temp_file, target_file)

        except (Exception, OSError, PermissionError) as e:
            print(f"❌ 데이터 저장 실패: {e}")
            # 임시 파일이 남아있다면 삭제
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass

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

        # 6. 점수 기록 히스토리 복구
        self.history = state.get("history", [])
        if not isinstance(self.history, list):
            print("⚠️ 히스토리 데이터 형식이 잘못되어 초기화합니다.")
            self.history = []

        # 7. 현재 진행 상황 복구
        session = state.get("current_session", {})
        valid_remaining = [] # 최종적으로 이어서 풀 목록

        try:
            remaining = session.get("remaining_quizzes", [])
            correct_count = int(session.get("correct_count", 0))
            score_points = float(session.get("score_points", 0.0))
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
                    "score_points": score_points,
                    "total": total,
                    "draft": session.get("draft")
                }

        except (ValueError, TypeError):
            print("⚠️ 세션 데이터 형식이 잘못되어 초기화합니다.")
            self.reset_session(save=True)
            valid_remaining = []

        # 8. 이어하기 확인
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
            "score_points": 0.0,
            "total": 0,
            "draft": None
        }
        # 필요에 따라 초기화 즉시 파일에 저장
        if save:
            self.save_state()