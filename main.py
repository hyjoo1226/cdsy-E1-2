from game import QuizGame
from quiz_data import DEFAULT_QUIZZES

def main():
    game = QuizGame()

    # 저장 파일 로드 시도
    loaded = game.load_state()
    # 로드 실패 시 기본 퀴즈 사용
    if not loaded:
        game.quizzes = DEFAULT_QUIZZES

    # 게임 시작
    try:
        # 퀴즈 이어하기
        if game.current_session.get("remaining_quizzes"):
            print("\n🚀 메인 메뉴를 건너뛰고 바로 퀴즈를 시작합니다!")
            game.play_quiz()

        # 문제 추가 이어하기
        if game.current_session.get("draft"):
            print("\n📝 작성 중이던 퀴즈 초안이 발견되었습니다!")
            game.add_quiz()

        # 이어하기가 아닌 경우 메인 메뉴
        game.show_menu()
        
    # 비정상 종료 예외 처리
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 비정상 종료 감지!")
        game.save_state()
        print("💾 저장 완료 후 종료합니다.")

if __name__ == "__main__":
    main()