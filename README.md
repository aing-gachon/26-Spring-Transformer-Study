## License

Original code by [Aladdin Persson](https://github.com/aladdinpersson/Machine-Learning-Collection): ![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)<br>
Modified for educational purposes by A.ing: [![CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc/4.0/)
## Introduction

A.ing 주니어 트랙 Transformer 세션은 Transformer에 대한 근본적인 이해를 목표로 합니다.<br>
단순히 모델을 가져다 쓰는 것이 아니라, 그 내부 구조와 작동 원리를 이해하고, 자신의 데이터에 맞춰 수정하고 개선할 수 있는 능력을 기르는 것을 목표로 합니다.<br>

## Eligibility

### Required

- 기초 파이썬 프로그래밍 능력
- 로컬 Jupyter Notebook 또는 Python 스크립트 실행 환경을 설정할 수 있는 능력
- 팀 프로젝트에 적극적으로 참여하고 지속할 수 있는 의지
### Recommended

- 머신러닝/딥러닝 기본 개념에 대한 이해
- PyTorch 또는 TensorFlow와 같은 딥러닝 프레임워크 경험
- 자연어 처리 또는 시퀀스 모델링에 대한 기본 지식
- 선형대수에 대한 기본 이해 (행렬 연산, 벡터 공간 등)
### Expected Outcomes

- Transformer의 아키텍처와 핵심 아이디어에 대한 깊은 이해
- 논문의 수식을 직접 코드로 구현할 수 있는 능력
- 자신의 데이터에 맞게 모델을 수정하고 개선할 수 있는 능력
- 팀 프로젝트를 통해 협업 능력과 문제 해결 능력 향상

## 자료가 서로 연결되는 방식

치트시트·쿡북·빈칸 노트북·퀴즈를 함께 읽을 수 있도록 **논문 가이드** [`Week1/transformer_paper_guide.md`](Week1/transformer_paper_guide.md)를 중심으로 자료를 연결했습니다. 논문에서 읽을 위치와 질문을 확인하고, 관련 개념·구현·문제로 이동할 수 있습니다.

```text
           [논문 가이드] transformer_paper_guide.md
                         R01 ~ R13
             ┌────────┬──────┴──────┬────────┐
          치트시트     쿡북       빈칸 노트북     퀴즈
           [CS§n]     [Cn]          [N-k]     [Qn]/[An]
```

가이드의 각 R 항목에는 관련 자료 번호가 있고, 각 자료에서도 해당 R 항목으로 돌아갈 수 있습니다. 시작 전 배경지식은 [선수자료](Week1/transformer_prerequisites.md)에서 점검하세요.

| 표기 | 가리키는 것 |
| --- | --- |
| `[R01]`~`[R13]` | 논문 가이드의 읽기 항목 |
| `[CS§0]`~`[CS§7]` | 치트시트의 개념 설명 |
| `[C0]`~`[C19]` | 쿡북의 구현 설명. C1~C19는 기존 step 번호와 같음 |
| `[N-1]`~`[N-36]` | 노트북의 빈칸 문장. 한 문장의 여러 인자는 같은 번호 |
| `[Q1]`~`[Q5]` / `[A1]`~`[A5]` | 퀴즈 문항 / 해설 |
| `E01` / `E02` | scaling / 위치 정보 비교 실험 |

대괄호 표기는 자료를 찾는 **번호**입니다. 문서의 연결 링크를 누르거나, 노트북 주석에 적힌 번호로 해당 자료를 찾아가세요.

## Weekly Plan

| 주차 | 단계 | 자료 | 세부 사항 |
| --- | --- | --- | --- |
| 0 | 준비 | [선수자료](Week1/transformer_prerequisites.md) | 토큰·텐서 축·broadcasting·모듈·teacher forcing 기초 점검 |
| 1 | 스터디 | 논문, [가이드](Week1/transformer_paper_guide.md), [치트시트](Week1/A.ing_Transformer_Cheat_sheet.md), [퀴즈](Week1/A.ing_Transformer_Questions.md) | R01~R11을 논문과 함께 읽고 기본·응용 문제로 확인. 심화는 선택 |
| 2 | 구현 | [쿡북](Week2/A.ing_Transformer_Cookbook.md), [빈칸 노트북](Week2/A.ing_Transformer_from_scratch_blank.ipynb) | N-1~N-36 구현, Check로 동작 확인, E01/E02 비교 실험. Multi30k 학습은 선택 |
| 3 | 실험 | [리그전 설명](Week3/A.ing_%EB%A6%AC%EA%B7%B8%EC%A0%84_Transformer_Explain.md), [리그전 노트북](Week3/Aing_%E1%84%85%E1%85%B5%E1%84%80%E1%85%B3%E1%84%8C%E1%85%A5%E1%86%AB_Transformer_Finetune.ipynb) | T4 고정 조건에서 Transformer 구조 비교 |
| 4 | 정리 | 실험 데이터 기록, [가이드 R11~R13](Week1/transformer_paper_guide.md#r11) | 1등 팀의 전략 발표 및 로그 분석. 관찰·해석·실험의 한계를 나누어 기록 |

## Paper Link

[Attention Is All You Need](https://arxiv.org/abs/1706.03762)

## Transformer_Youtube_Playlist

https://youtube.com/playlist?list=PL-PHXChFg8_tv0e8bNxYuh5VdWH0JO1sl&si=1K1-1GJuzpGGlA13

## Folder Structure

```text
26-Spring-Transformer-Study/
├─ README.md
├─ rules.md                                        # 출석·결석·공결 규칙
├─ Week1/
│  ├─ transformer_paper_guide.md                    # 논문 가이드 R01~R13
│  ├─ transformer_prerequisites.md                  # 시작 전 배경지식과 자기점검
│  ├─ A.ing_Transformer_Cheat_sheet.md              # 개념 정리 CS§0~CS§7
│  ├─ A.ing_Transformer_Questions.md                # 퀴즈 Q1~Q5
│  └─ transformer_questions_sample_answer.md         # 해설 A1~A5
├─ Week2/
│  ├─ A.ing_Transformer_Cookbook.md                 # API·입출력 설명과 오류 진단 표
│  ├─ A.ing_Transformer_from_scratch_blank.ipynb    # 빈칸 N-1~N-36, Check, E01/E02
│  └─ A.ing_Transformer_from_scratch_answer.ipynb   # 완성 모델과 동일한 핵심 검사
└─ Week3/
   ├─ A.ing_리그전_Transformer_Explain.md            # 구조 비교 리그전 진행 안내
   ├─ Aing_리그전_Transformer_Finetune.ipynb       # T4 기반 Transformer 구조 비교 리그전
   └─ evaluate_submission.py                      # 운영자용 제출 모델 재평가
```

빈칸 노트북을 **먼저 스스로 채운 뒤에** [정답 노트북](Week2/A.ing_Transformer_from_scratch_answer.ipynb)을 여세요. 쿡북은 API 사용법과 입출력 조건을 설명하고, 전체 정답은 별도 노트북에서 제공합니다.

## 담당자

| 이름 | 이메일 |
|------|--------|
| 전제오(자료 제작 총괄) | chris11122@gachon.ac.kr |
| 이영민 | dudals4087@naver.com |
| 정진용 | wlsdyd5373@gachon.ac.kr |
| 전지우 | jiwoo424@gachon.ac.kr |

질문이나 도움이 필요하면 언제든 연락 주세요!<br>
한 학기 동안 함께 열심히 공부해봅시다!

------

해당 교육 자료는 [Aladdin Persson의 Machine-Learning-Collection](https://github.com/aladdinpersson/Machine-Learning-Collection)을 기반으로 A.ing에서 교육 목적에 맞춰 수정 및 재구성하였습니다. 원본 코드의 로직은 MIT 라이선스를 따르며, 수정된 부분 및 실습 구성에 대해서는 CC BY-NC 4.0 라이선스를 적용합니다. <br>
This educational material is based on [Aladdin Persson's Machine-Learning-Collection](https://github.com/aladdinpersson/Machine-Learning-Collection) and has been modified and restructured by A.ing for educational purposes. The logic of the original code follows the MIT license, and the modified parts and practice composition are subject to the CC BY-NC 4.0 license.
