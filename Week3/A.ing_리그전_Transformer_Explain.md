# A.ing 리그전 — Transformer 구조 비교

Colab **NVIDIA T4**에서 같은 데이터와 공통 학습 규칙으로 Transformer 구조와 학습 하이퍼파라미터 조합을 비교합니다. 제한된 파라미터를 폭·깊이·Encoder/Decoder·FFN에 어떻게 배분하는지 실험합니다. 최종 점수는 **최고 validation checkpoint의 test BLEU**입니다.

[리그전 노트북](Aing_리그전_Transformer_Finetune.ipynb)은 ResNet처럼 **규칙 → STEP1~7 → 학습 곡선 → test 예시**로 구성했습니다. 기존 링크를 유지하기 위해 파일명을 보존했으며, 내용은 사전학습 없이 처음부터 학습하는 구조 비교입니다.

## 공통 규칙

| 항목 | 설정 |
| --- | --- |
| 환경 / seed | Colab T4 / **42 고정** |
| 데이터 | Multi30k de→en, train 16,000 / validation 1,014 |
| Tokenizer / 길이 | train으로만 학습한 joint ByteLevel BPE 8,000 / 최대 96토큰 |
| 모델 상한 | **학습 파라미터 800만 이하** |
| Quick / Full | 첫 500 updates / **최대 4,000 updates** |
| Batch | micro 16 × accumulation 4 = 64 |
| Optimizer 공통 세부값 | Adam/AdamW의 betas=(0.9,0.98), eps=1e-9 |
| Scheduler | warmup 100 → 최대 4,000 updates 기준 cosine |
| Label smoothing / gradient clipping | 0.1 / 1.0 |
| 평가 | 매 **500 updates** 전체 validation BLEU |
| Early stopping | 최소 **1,500 updates 이후**, **3회 연속 0.1점 초과 개선 없음** |
| 모델 선택 / 최종 점수 | 최고 validation BLEU checkpoint / test BLEU |

참가자는 seed를 바꾸거나 여러 seed의 평균을 제출하지 않습니다. 모든 실험은 **seed 42**로 비교합니다. test는 checkpoint 선택이나 early stopping에 사용하지 않습니다.

## 실행 순서

1. **STEP1 — 환경 확인:** tokenizer·평가기 버전 설치와 import
2. **STEP2 — 공통 규칙:** 고정 seed·학습 예산·T4 확인
3. **STEP3 — 데이터:** 고정 split과 tokenizer 준비
4. **STEP4 — 모델:** Encoder–Decoder 구현과 파라미터·mask·메모리 검사 함수
5. **STEP5 — 튜닝 설정:** `ARCH`·`TRAIN_HP`와 실행 방식 선택
6. **STEP6 — 학습/평가:** 공통 함수 정의
7. **STEP7 — 실행/점수:** 검사·학습·최고 모델의 valid/test 점수 표시·제출
8. **추가 자료:** 학습 곡선과 test 번역 예시

처음에는 위에서부터 모두 실행합니다. 함수 정의 셀은 접혀 있으므로 필요하면 펼쳐 읽을 수 있습니다. 이후 구조 실험은 **STEP5 → STEP7**을 다시 실행하면 됩니다.

VS Code에서는 공식 Colab 확장의 **Select Kernel → Colab → GPU → T4**로 연결합니다. STEP2 출력에서 T4인지 확인하세요. 토크나이저는 `tokenizers==0.22.2`, 평가기는 `sacrebleu==2.6.0`입니다. PyTorch/CUDA 실제 버전은 결과에 기록하며, 재개 시 기존 환경과 일치해야 합니다.

## STEP5에서 한 번에 튜닝하기

```python
ARCH = dict(
    d_model=256,
    encoder_layers=3,
    decoder_layers=3,
    num_heads=4,
    ffn_ratio=4,
    norm_first=False,
)
TRAIN_HP = dict(
    optimizer="AdamW",
    learning_rate=1e-3,
    weight_decay=0.01,
    dropout=0.1,
)
LEAGUE_MODE = "quick"  # 첫 500 updates 확인 후 "full"로 변경
RESUME = True
```

| 설정 | 허용값 | 비교할 내용 |
| --- | --- | --- |
| `d_model` | 128 / 192 / 256 / 384 | 토큰 표현의 폭 |
| `encoder_layers` / `decoder_layers` | 각각 1 / 2 / 3 / 4 | source 처리와 target 생성에 배분하는 깊이 |
| `num_heads` | 2 / 4 / 8 | 특징 축을 나누는 방식 |
| `ffn_ratio` | 2 / 4 | FFN 중간 차원의 크기 |
| `norm_first` | False / True | Post-LN / Pre-LN |

`ARCH` 바로 아래의 `TRAIN_HP`에서 학습 설정도 조정합니다. 기본값은 시작점이며 최적값을 보장하지 않습니다.

| 학습 설정 | 기본값 / 허용값 | 무엇을 바꾸나요? |
| --- | --- | --- |
| `optimizer` | AdamW / Adam | 가중치 갱신 방식 |
| `learning_rate` | 기본 1e-3, 유한한 양수 | warmup 후 도달할 최대 학습률 |
| `weight_decay` | 기본 0.01, 유한한 0 이상 값 | 가중치 정규화 강도 |
| `dropout` | 기본 0.1, 0 이상 1 미만 | Embedding과 Transformer 내부 dropout 확률 |

Adam과 AdamW는 weight decay 적용 방식이 다릅니다. 같은 숫자가 같은 정규화 효과를 뜻하지 않으므로 optimizer를 바꿀 때 decay도 함께 검토하세요. Dropout은 학습에서만 적용하며 평가에서는 꺼집니다. Scheduler 형태, warmup, label smoothing, batch와 early stopping 규칙은 계속 공통입니다.

**변경 후 STEP5 셀과 STEP7만 다시 실행**하면 됩니다. 구조뿐 아니라 네 학습 설정 중 하나라도 바뀌면 새로운 run ID로 저장합니다. 데이터·tokenizer를 다시 만들 필요는 없으며, 데이터 패키지는 튜닝 값에 의존하지 않습니다. 결과표에는 각 실험의 optimizer·learning rate·weight decay·dropout도 표시합니다.

허용값 조합이어도 **800만 파라미터를 넘으면 거부**합니다. 최대 길이 backward 검사에서 예약 메모리 12GiB 상한도 확인합니다. 기준 모델은 약 758만 파라미터입니다. `d_model=192`를 추가해 제한된 용량 안에서 폭과 깊이를 더 세밀하게 조합할 수 있습니다.

한 항목씩 바꿔 원인을 확인한 뒤, 비슷한 파라미터 수에서 넓고 얕은 모델·좁고 깊은 모델·Encoder/Decoder 비대칭 모델·FFN 비율을 비교하세요. head 수만 늘린다고 전체 projection 파라미터가 늘어나는 것은 아닙니다.

## Early stopping과 최고 모델 저장

학습은 500 updates마다 validation을 평가합니다. Early stopping에는 **마지막으로 0.1점 초과 개선한 점수**를 기준으로 사용합니다. 예를 들어 기준이 20.00이면 20.05는 patience를 초기화하지 않지만, 이후 20.15에 도달하면 기준을 갱신하고 초기화합니다.

- 1,500 updates 이전에는 기준 점수를 갱신하되 미개선 횟수는 세지 않습니다.
- 1,500 updates 이후 3회 연속 개선이 없으면 종료합니다. 가장 이른 종료는 2,500 updates입니다.
- 개선이 계속되면 최대 4,000 updates까지 학습합니다.
- **최고 모델 저장에는 0.1점 조건을 적용하지 않습니다.** 20.00 → 20.05도 최고 점수라면 `best.pt`를 갱신합니다.
- 조기 종료 시점의 모델이 아니라, 학습 전체에서 최고 validation BLEU를 기록한 모델로 최종 평가합니다.

이 규칙은 모든 참가자에게 공통입니다. 실제 updates는 모델별로 달라질 수 있으며, 공통 최대 예산과 중단 규칙 아래에서 비교합니다. 오래 학습할수록 구조 간 점수 차이가 커진다고 보장하지는 않습니다.

## Quick / Full과 재개

`quick`은 별도 스케줄이 아닌 같은 학습의 첫 500 updates입니다. `full`로 바꾸면 저장된 500 update부터 이어가며, cosine의 전체 길이도 계속 4,000을 기준으로 유지합니다.

- `latest.pt`: 모델·optimizer·GradScaler·난수·진행 상태·early stopping 상태·TRAIN_HP
- `best.pt`: validation 최고 모델과 선택 시점
- `summary.json`: 점수·실행 시간·평가 이력·종료 사유

재개할 때 구조·TRAIN_HP·환경과 평가 이력·저장된 patience가 일치하는지 검사합니다. 이전 결과를 평가하거나 제출할 때에는 현재 셀 값이 아닌 그 실험에 저장된 TRAIN_HP를 사용합니다. 이미 정상 종료한 `full`을 다시 실행하면 추가 학습하지 않고 결과를 불러옵니다. 정상 종료 사유는 `max_steps` 또는 `early_stopping`입니다. `quick_limit`은 제출 가능한 종료가 아닙니다.

프로토콜은 `architecture-league-v3-tuning`, 저장 폴더는 `transformer_league_runs_v3`입니다. 이전 v1/v2 실험과 혼합하거나 그 checkpoint를 이어 학습하지 않습니다. Colab 런타임 종료 전 실험 폴더를 다운로드하세요. 임의의 신뢰할 수 없는 checkpoint를 불러오지 마세요.

## 점수와 제출

ResNet처럼 STEP7에서 valid/test loss·BLEU·chrF를 출력합니다. Quick 결과도 표시하되 공식 제출 대상과 구분합니다. 후보를 고르는 기준은 validation이며, 최종 모델의 test 결과를 확인합니다.

Loss는 PAD를 제외한 target 토큰당 cross entropy입니다. BLEU/chrF는 길이 제한으로 잘라낸 정답 대신 원문 reference를 사용합니다. Greedy 생성에는 정답 target을 전달하지 않습니다.

```python
SUBMISSION = export_submission(RESULT['run_id'])
```

**T4에서 full 정상 종료한 모델**만 제출할 수 있습니다. 최대 4,000 updates에 도달한 경우와 공통 early stopping으로 종료한 경우 모두 인정합니다. 종료 플래그만 믿지 않고 평가 이력으로 중단 규칙을 다시 확인합니다.

ZIP에는 `best.pt`, `summary.json`, `tokenizer.json`, `data_manifest.json`, `checksums.json`이 포함됩니다. `DATA_PACKAGE`는 운영자가 공지한 값과 같아야 합니다. 파일 해시는 무결성 확인용이며 부정행위를 방지하는 서명은 아닙니다.

운영자는 공통 노트북과 [evaluate_submission.py](evaluate_submission.py)로 제출물을 재검증할 수 있습니다.

```bash
python evaluate_submission.py 제출폴더 --expected-package 운영자가_공지한_DATA_PACKAGE
```

## 실행 시간과 검증 범위

기존 T4 측정은 1,200 updates 설정에서 수행했습니다. 이 수치를 새 4,000 updates·800만 상한 설정의 실측으로 해석하면 안 됩니다.

새 구현은 로컬에서 조기 종료, 최고 모델 선택, 재개 가중치 일치, 정상 종료 후 재실행, 제출 검증을 확인했습니다. 새 규칙의 T4 실행 시간과 비슷한 크기 구조들 사이의 변별력은 별도 실측이 필요합니다. 목표 실행 시간 8~12분은 보장값이 아닙니다.

튜닝 추가 후에는 Adam/AdamW 생성, learning rate·weight decay·dropout의 실제 적용, 각 설정별 run ID 분리, 저장된 설정으로 평가·제출, Adam의 quick→full 재개 가중치 일치도 검증했습니다. 새 튜닝 버전의 T4 실행은 아직 수행하지 않았습니다.
