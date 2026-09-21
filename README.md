## License

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

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
자료 4종(치트시트·쿡북·빈칸 노트북·퀴즈)은 각자 영어 논문만 참조하기 때문에, 논문을 못 읽으면 4개가 전부 파편이 됩니다.
그래서 **논문 좌표 허브** [`Week1/transformer_paper_guide.md`](Week1/transformer_paper_guide.md)를 하나 두고 모든 자료가 그쪽을 가리킵니다.

```text
           [논문 가이드] transformer_paper_guide.md
                         R01 ~ R13
             ┌────────┬──────┴──────┬────────┐
          치트시트     쿡북       빈칸 노트북     퀴즈
           [CS§n]     [Cn]          [N-k]     [Qn]/[An]
```

허브의 각 R 항목은 자기를 참조하는 자료 좌표를 전부 나열하고, 각 자료는 자기 절이 어느 R인지 밝힙니다 (양방향).

| 표기 | 가리키는 것 |
| --- | --- |
| `[R05]` | 허브의 R 항목 |
| `[CS§n]` | 치트시트 n번 절 |
| `[Cn-m]` | 쿡북 n절 m번 항목 |
| `[N-k]` | 빈칸 노트북 k번 빈칸 |
| `[Qn]` / `[An]` | 퀴즈 문항 / 모범답안 |

대괄호 한 겹이라 링크가 아니라 **좌표**입니다. 막히면 그 좌표를 따라가면 됩니다.

## Weekly Plan

| 주차 | 단계 | 자료 | 세부 사항 |
| --- | --- | --- | --- |
| 0 | 준비 | [선수자료](Week1/transformer_prerequisites.md) | 자연어처리 기초와 Transformer이전 아키텍처에 대한 이해 |
| 1 | 스터디 | 논문, [가이드](Week1/transformer_paper_guide.md), [치트시트](Week1/A.ing_Transformer_Cheat_sheet.md), [퀴즈](Week1/A.ing_Transformer_Questions.md) | R01~R11을 논문과 나란히 읽고 퀴즈로 확인 |
| 2 | 구현 | [쿡북](Week2/A.ing_Transformer_Cookbook.md), [빈칸 노트북](Week2/A.ing_Transformer_from_scratch_blank.ipynb) | N-1~N-36 구현, Check로 동작 확인, E01/E02 비교 실험. Multi30k 학습은 선택 |
| 3 | 실험 | [리그전 설명](Week3/A.ing_%EB%A6%AC%EA%B7%B8%EC%A0%84_Transformer_Explain.md), [리그전 노트북](Week3/Aing_%E1%84%85%E1%85%B5%E1%84%80%E1%85%B3%E1%84%8C%E1%85%A5%E1%86%AB_Transformer_Finetune.ipynb) | 하이퍼파라미터 튜닝 및 리그전  |
| 4 | 정리 | 실험 데이터 기록, [가이드 R11~R13](Week1/transformer_paper_guide.md#r11) | 1등 팀의 전략 발표 및 로그 분석 |

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
   └─ Aing_리그전_Transformer_Finetune.ipynb       # 튜닝 리그전 (FIXED/TUNE 구분)
```

빈칸 노트북은 **먼저 스스로 채운 뒤에** 정답 노트북을 여세요. 쿡북에는 정답 코드가 없고 API 사용법만 있습니다.


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

Copyright © 2026 A.ing. Licensed under CC BY-NC 4.0.

