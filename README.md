# 🧠 심리학 퀴즈 게임 (Python CLI)

## 프로젝트 개요
**"Git과 함께하는 Python 첫 발자국"** 입학 연수 미션으로 제작된 콘솔 기반 퀴즈 게임입니다.
게임의 상태(진행 상황, 퀴즈 목록, 점수 기록)를 JSON 파일로 저장하여 프로그램을 껐다 켜도 데이터가 유지되는 **데이터 영속성**을 구현했습니다.
<br>
<br>

### 퀴즈 주제 선정 이유
제 심리학 도메인을 바탕으로, 일상에서 흔히 겪는 현상들이나 성격 유형 검사(MBTI) 등 사람들이 흥미를 가질 만한 **'심리학'**을 주제로 선정했습니다.
<br>
<br>

### 실행 방법
```
python main.py
```
<br>

### 기능 목록
1. 메인 메뉴
<img width="744" height="191" alt="스크린샷 2026-04-08 오후 1 42 40" src="https://github.com/user-attachments/assets/9e7c0bfa-fdbe-4fc2-8cbd-8772ecddb1fb" />
<br>
<br>

2. 퀴즈 풀기(랜덤 모드, 문제 수 선택, 힌트 사용)
<img width="751" height="152" alt="스크린샷 2026-04-08 오후 1 44 32" src="https://github.com/user-attachments/assets/dd1440ab-4833-40cc-962c-40df59510462" />
<img width="752" height="296" alt="스크린샷 2026-04-08 오후 1 45 21" src="https://github.com/user-attachments/assets/03a913b8-30f2-4f86-9a58-41e26da348e3" />
<img width="782" height="190" alt="스크린샷 2026-04-08 오후 1 46 24" src="https://github.com/user-attachments/assets/cd4fd3f9-b411-4451-a969-0018539c95c7" />
<img width="776" height="77" alt="스크린샷 2026-04-08 오후 1 47 06" src="https://github.com/user-attachments/assets/bb094ed4-680a-4165-8f1c-1a37f5b9616a" />
<br>
<br>

3. 퀴즈 추가
<img width="787" height="168" alt="스크린샷 2026-04-08 오후 1 51 50" src="https://github.com/user-attachments/assets/06cdb01e-ddc0-4575-a9c9-9a61467edc49" />
<br>
<br>

4. 퀴즈 목록
<img width="781" height="167" alt="스크린샷 2026-04-08 오후 1 56 02" src="https://github.com/user-attachments/assets/3c59a66a-4c65-47f8-a869-58c670e4540c" />
<br>
<br>

5. 퀴즈 삭제
<img width="768" height="213" alt="스크린샷 2026-04-08 오후 1 56 29" src="https://github.com/user-attachments/assets/7b789c4e-cd56-4e51-9f7e-f5209d9080ba" />
<br>
<br>

6. 퀴즈 도전 기록
<img width="774" height="137" alt="스크린샷 2026-04-08 오후 1 56 59" src="https://github.com/user-attachments/assets/0a844c4d-cad6-42f5-894b-ff0af32fded1" />
<br>
<br>

### 파일 구조
```
📦 cdsy-E1-2
 ┣ 📦 docs          # 개발문서, 스크린샷 등 폴더
 ┣ 📜 main.py       # 프로그램 실행 진입점
 ┣ 📜 game.py       # 퀴즈 게임의 핵심 로직 (QuizGame 객체 정의 - 메뉴, 플레이, 세션 관리, 파일 입출력)
 ┣ 📜 models.py     # 데이터 모델 클래스 (Quiz 객체 정의)
 ┣ 📜 quiz_data.py  # 초기 기본 심리학 퀴즈 데이터 모음
 ┣ 📜 utils.py      # 공통 유틸리티 함수 (안전한 정수 입력 검증 등)
 ┣ 📜 state.json    # 사용자 데이터가 저장되는 로컬 JSON 파일 (게임 시 자동 생성)
 ┗ 📜 README.md     # 프로젝트 설명 문서
```
<br>

### 데이터 파일 설명
```
{
    "best_score": 33,                                       # 플레이 최고 점수
    "quizzes": [                                            # 전체 퀴즈 객체들의 리스트
        {
            "id": "e4f06e01-3840-4f46-99a5-2e33a0613f73",   # 퀴즈 식별을 위한 고유 UUID
            "question": "mbti에서 'I'는 무엇을 의미할까요?",       # 퀴즈 문제
            "choices": ["감정적", "외향적", "내향적", "사고적"],   # 4개의 선택지가 담긴 배열
            "answer": 3,                                    # 정답 번호
            "hint": "'I'는 'Introversion'의 약자입니다."         # 힌트
        }
    ],
    "history": [                                             # 모든 게임 플레이 결과 히스토리
        {
            "date": "2026-04-08 14:26",                       # 게임 플레이 시점
            "total": 3,                                       # 풀기로 선택한 총 문제 수
            "correct": 1,                                     # 실제로 맞힌 정답 개수
            "score": 33                                       # 최종 점수
        }
    ],
    "current_session": {                                      # 중단된 게임, 작성 중 퀴즈를 위한 임시 상태 정보
        "remaining_quizzes": [],                              # 현재 세션에서 남은 문제들의 id 리스트
        "correct_count": 0,                                   # 현재 세션에서 획득한 누적 점수
        "total": 0,                                           # 현제 세션의 총 문제 수
        "draft": {                                            # 작성 중 퀴즈를 위한 임시 데이터
            "question": "",                                   # 작성 중이던 문제 내용
            "choices": [],                                    # 작성 중이던 선택지 배열
            "answer": 0,                                      # 작성 중이던 정답 번호
            "hint": null                                      # 작성 중이던 힌트
        }                                        
    }
}
```

<br>

### 추가 제출
<img width="1241" height="1329" alt="vscode" src="https://github.com/user-attachments/assets/8126f667-4928-49f8-8887-b45e1dafd8f3" />
<img width="739" height="271" alt="gitlog" src="https://github.com/user-attachments/assets/daa1e8a4-397d-4921-a0e0-0b805a602bfa" />


