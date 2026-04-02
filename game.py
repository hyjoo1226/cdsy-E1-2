from utils import get_int_input
class QuizGame:
    # QuizGame 객체 초기화
    def __init__(self):
        self.quizzes = []          # Quiz 객체 리스트
        self.best_score = 0        # 최고 점수


    # ==================== 게임 진행 ====================
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