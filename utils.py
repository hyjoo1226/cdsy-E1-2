# 공통 입력 예외 처리(숫자)
def get_int_input(prompt, min_val, max_val):
    while True:
        try:
            # 앞뒤 공백 제거
            user_input = input(prompt).strip()

            # 빈 입력 처리
            if not user_input:
                print("값을 입력해주세요.")
                continue

            # 숫자 변환 실패 처리
            temp_number = int(user_input)

            # 허용 범위 밖 숫자 처리
            if not (min_val <= temp_number <= max_val):
                print(f"{min_val}~{max_val} 사이의 숫자를 입력해주세요.")
                continue

            validate_input = temp_number

            return validate_input

        except ValueError:
            print("숫자를 입력해주세요.")