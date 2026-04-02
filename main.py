from game import QuizGame
from quiz_data import DEFAULT_QUIZZES

def main():
    game = QuizGame()

    # 기본 퀴즈 추가
    game.quizzes = DEFAULT_QUIZZES

    # 퀴즈 풀기
    game.play_quiz()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.")
    except EOFError:
        print("\n입력 스트림이 종료되었습니다. 프로그램을 종료합니다.")