# Transformer 논문 가이드 (허브)

- 논문: Vaswani et al., *Attention Is All You Need*, arXiv:1706.03762v7 — [PDF](https://arxiv.org/pdf/1706.03762v7) / [HTML](https://arxiv.org/html/1706.03762v7)
- 스터디 자료 4종: 치트시트 / 쿡북 / 빈칸 노트북 / 퀴즈

## 이 폴더의 문서

시작 전 배경은 [선수자료](transformer_prerequisites.md). 개념 요약은 [치트시트](A.ing_Transformer_Cheat_sheet.md), 구현 API는 [쿡북](../Week2/A.ing_Transformer_Cookbook.md),
확인 문제는 [퀴즈](A.ing_Transformer_Questions.md)와 [퀴즈_모범답안](transformer_questions_sample_answer.md). 노트북은 [빈칸](../Week2/A.ing_Transformer_from_scratch_blank.ipynb)과 [정답](../Week2/A.ing_Transformer_from_scratch_answer.ipynb), 튜닝은 [리그전](../Week3/A.ing_리그전_Transformer_Explain.md).

## 참조 문법

| 표기 | 가리키는 것 |
| --- | --- |
| `[R05]` | 이 허브의 R 항목 |
| `[CS§n]` | 치트시트 n번 절 |
| `[Cn]` | 쿡북 n번 절 |
| `[N-k]` | 빈칸 노트북 k번 빈칸 |
| `[Qn]` | 퀴즈 n번 문항 |
| `[An]` | 퀴즈 모범답안 n번 문항 |

허브의 각 R은 자기를 참조하는 자료 좌표를 `자료 좌표` 칸에 전부 나열하고,
각 자료는 자기 절이 어느 R인지 밝힙니다 (**양방향**).

## 각 R 항목의 6칸 템플릿

| 칸 | 내용 |
| --- | --- |
| `논문 위치` | §번호, 식 번호, Table/Fig 번호 |
| `읽기 전 질문` | 이 대목을 읽기 **전에** 품고 갈 질문 1~2개 |
| `원문 핵심` | 영어 원문 발췌 1~2문장 (3줄 이내) |
| `확인 질문` | **논문을 근거로 설명하는** 질문 2~3개 + 어디를 볼지 |
| `해석 노트` | 논문이 **명시하지 않은 것**만 — 오해 교정·코드 연결·자료 간 모순 (3줄) |
| `자료 좌표` | `[CS§n] [Cn] [N-k] [Qn] [An]` |

읽는 법: `읽기 전 질문`을 품고 논문의 `논문 위치`를 편 다음, 읽고 나서 `확인 질문`에 답합니다.
`원문 핵심`으로 문맥을 잡고, `확인 질문`에서 지정한 본문·식·그림·표를 함께 확인하세요. 답에는 근거 위치와 자신의 설명을 적습니다.

## 범위

이 허브가 덮는 범위는 스터디 4주가 다루는 **§1, §3~§3.5, §4, §5.1~§5.4, §6.1~§6.2**뿐입니다.

**범위 밖 (의도적으로 다루지 않음)**

- §2 Background
- §6.3 English Constituency Parsing
- §7 Conclusion과 부록 Attention Visualizations

## 주차별 읽기 경로

R 번호는 **논문 순서**라 학습 순서와 다릅니다. 주차별로는 이 순서를 따릅니다.

| 주차 | R 범위 | 비고 |
| --- | --- | --- |
| Week 1 (논문 정독) | R01 R02 R03 R04 R05 R06 R07 R08 R09 R10 R11 | 개념과 논증 |
| Week 2 (구현) | R02 R09 R10 R03 R04 R05 R07 R06 R08 R12 R13 | 입력 표현 → attention → 블록 → 학습·평가 |
| Week 3 (리그전) | R06 R08 R09 R10 R12 R13 | 구조·학습 조건·validation 선택을 리그전 규칙과 연결 |
| Week 4 (분석) | R11 R12 R13 | 계산 비용·학습 조건·실험 결과 해석 |

논문 순서대로만 읽으면 R09·R10이 attention 뒤에 오는데, encoder·decoder의 입력을 구현하려면 그 둘을 먼저 알아야 합니다.
이 표가 그 역전을 막습니다.

## 목차

### §1 Introduction

| ID | 제목 |
| --- | --- |
| [R01](#r01) | 순차 계산을 줄이려는 이유 |

### §3–§3.1 Encoder–Decoder의 전체 구조

| ID | 제목 |
| --- | --- |
| [R02](#r02) | Encoder–Decoder와 한 칸 이동 |

### §3.2 Attention의 연산과 사용 위치

| ID | 제목 |
| --- | --- |
| [R03](#r03) | Q·K·V와 가중합 |
| [R04](#r04) | 왜 √d_k로 나누는가 |
| [R05](#r05) | Multi-Head: 분할과 결합 |
| [R06](#r06) | 세 종류의 Attention |
| [R07](#r07) | Mask와 정보 누출 |

### §3.1·§3.3–3.5 블록과 입출력 표현

| ID | 제목 |
| --- | --- |
| [R08](#r08) | Residual·LayerNorm·FFN |
| [R09](#r09) | Embedding과 출력 logits |
| [R10](#r10) | 위치 정보 |

### §4–6.2 비교 논리·학습·실험

| ID | 제목 |
| --- | --- |
| [R11](#r11) | 복잡도와 경로 길이 |
| [R12](#r12) | 학습 레시피와 교육용 설정 |
| [R13](#r13) | 실험 결과를 읽는 방법 |

---

<a id="r01"></a>
## R01. 순차 계산을 줄이려는 이유

- **논문 위치**: §1 2문단 + 마지막 문단 “In this work we propose the Transformer…”
- **읽기 전 질문**
    - RNN 기반 번역 모델은 앞 단어의 처리가 끝나야 다음 단어를 처리합니다. 이 기다림을 줄이면 학습에서 무엇이 달라질까요?
    - Encoder–Decoder라는 큰 구성을 유지하면서 내부의 문장 처리 방법만 바꿀 수 있을까요?
- **원문 핵심**
    - “In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.”
    - “The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.”
    - 출처: [§1 Transformer 제안 문단](https://arxiv.org/html/1706.03762v7#S1.p4.1).
- **확인 질문**
    - 1) §1의 Transformer 제안 문단에서 저자는 recurrence(순환)를 쓰는 대신 어떤 방법에 기반한다고 설명합니까? 그 **방법의 이름**을 적으세요.
    - 2) 같은 문단에서 이 구조가 학습의 병렬 처리에 어떤 이점을 준다고 주장합니까? 앞부분의 RNN 설명을 함께 읽고, 앞 위치의 계산 결과를 기다려야 한다는 제약과 연결하세요.
    - 3) §1 마지막 문단에서 저자가 보고한 학습 시간은 얼마입니까? 번역 품질에 관한 주장도 찾아, 학습 속도만 개선했다고 요약해도 되는지 판단하세요.
- **해석 노트**
    - Transformer가 유지한 것은 Encoder–Decoder 구성이고, 바꾼 것은 내부의 문맥 처리 방식입니다. 전체 구조는 [R02](#r02)와 연결해서 읽습니다.
    - 학습의 위치 병렬화와 번역문의 순차 생성은 구분합니다. 생성 시에는 앞서 만든 토큰을 기다리므로 “모든 계산이 동시에 끝난다”는 뜻이 아닙니다.
- **자료 좌표**: [CS§0](A.ing_Transformer_Cheat_sheet.md#cs0) · [Q3](A.ing_Transformer_Questions.md#q3) / [A3](transformer_questions_sample_answer.md#a3)

---

<a id="r02"></a>
## R02. Encoder–Decoder와 한 칸 이동

- **논문 위치**: §3 첫 문단 + §3.1 'Encoder'·'Decoder' 두 소제목, Fig.1
- **읽기 전 질문**
    - 원문을 읽는 encoder와 번역을 만드는 decoder는 어떤 정보를 주고받아야 할까요?
    - 정답 번역문을 학습 입력으로 사용할 때, 지금 예측해야 할 정답까지 미리 보여 주지 않으려면 어떻게 해야 할까요?
- **원문 핵심**
    - “We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions.”
    - “This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.”
    - 출처: [§3.1 Decoder 문단](https://arxiv.org/html/1706.03762v7#S3.SS1.SSS0.Px2.p1.1).
- **확인 질문**
    - 1) §3 첫 문단에서 encoder가 입력받는 것과 만들어 내는 것을 찾으세요. Decoder는 그 결과를 받아 무엇을 생성합니까? 두 부분의 역할을 각각 한 문장으로 적으세요.
    - 2) Fig.1과 §3.1에서 encoder·decoder의 층 반복 횟수와 한 층의 서브레이어 수를 채우세요: encoder ___층/___개, decoder ___층/___개. Decoder에 추가된 attention은 어느 쪽 정보를 받습니까?
    - 3) §3.1 마지막 문장은 입력을 한 칸 이동하는 것과 masking을 함께 설명합니다. 이 두 처리가 예측 위치 i에서 볼 수 있는 출력 토큰의 범위를 어떻게 제한하는지 적으세요. 아래 입력·정답 표에서는 같은 열을 기준으로 확인하세요.
- **해석 노트**
    - 정답의 앞부분을 decoder 입력으로 주는 것이 teacher forcing입니다. 아래 표는 한 칸 이동을 보여 주며, 미래 입력을 가리는 이유는 [R07](#r07)에서 확인합니다.
    - Encoder와 decoder에 별도의 정답을 주지는 않습니다. 번역 손실로 두 스택을 함께 학습하는 과정은 [R12](#r12)에 모았습니다.
    - 원문과 번역문의 길이는 달라도 됩니다. 그림의 N은 층 반복 횟수이며 실습의 배치 크기 표기와 다릅니다.
- **자료 좌표**: [CS§0](A.ing_Transformer_Cheat_sheet.md#cs0) · [C1](../Week2/A.ing_Transformer_Cookbook.md#c1) · [C19](../Week2/A.ing_Transformer_Cookbook.md#c19) · [Q5](A.ing_Transformer_Questions.md#q5) / [A5](transformer_questions_sample_answer.md#a5) · [N-6] [N-26] [N-33] [N-34] [N-35] [N-36]

**같은 위치의 입력과 정답**

| 위치 | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Decoder 입력 | BOS | I | eat | apples |
| 예측할 정답 | I | eat | apples | EOS |

---

<a id="r03"></a>
## R03. Q·K·V와 가중합

- **논문 위치**: §3.2 첫 문단 + §3.2.1 Scaled Dot-Product Attention — 식(1), Fig.2 left
- **읽기 전 질문**
    - 번역할 때 원문의 어느 위치를 얼마나 참고할지 정하는 일과, 그 위치의 내용을 가져오는 일은 어떻게 다를까요?
- **원문 핵심**
    - “An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.”
    - “The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.”
    - 출처: [§3.2 Attention 정의](https://arxiv.org/html/1706.03762v7#S3.SS2.p1.1).
- **확인 질문**
    - 1) §3.2 첫 문단에서 attention의 출력은 무엇의 가중합이라고 설명합니까? 그 가중치를 정할 때 비교하는 두 벡터의 이름도 적으세요.
    - 2) Eq.(1)과 Fig.2 왼쪽에서 내적 → scaling → softmax → value와의 행렬 곱을 찾으세요. 이 중 참고할 위치의 비율을 만드는 단계와, 그 비율로 내용을 모으는 단계는 각각 어디입니까?
    - 3) Eq.(1)의 마지막에 K가 아니라 V를 곱하는 이유를 첫 문단의 정의와 연결해 설명하세요. Attention 점수표 자체가 최종 출력이라고 말해도 됩니까?
- **해석 노트**
    - 이 attention 모듈에서 학습 대상은 Q·K·V와 최종 출력을 만드는 projection의 파라미터입니다. Attention 비율표는 현재 입력으로 계산하는 값이며 독립 파라미터가 아닙니다.
    - Self-attention에서는 Q·K·V의 입력 출처가 같습니다. 서로 다른 projection을 통과한 값까지 같다는 뜻은 아닙니다.
    - Attention 점수와 최종 출력은 다릅니다. 코드에서는 softmax가 key 위치 축에 적용되는지 확인합니다.
- **자료 좌표**: [CS§1](A.ing_Transformer_Cheat_sheet.md#cs1) · [C6](../Week2/A.ing_Transformer_Cookbook.md#c6) · [C8](../Week2/A.ing_Transformer_Cookbook.md#c8) · [C11](../Week2/A.ing_Transformer_Cookbook.md#c11) · [N-2] [N-3] [N-4] [N-10] [N-12]

---

<a id="r04"></a>
## R04. 왜 √d_k로 나누는가

- **논문 위치**: §3.2.1 마지막 문단 “We suspect that for large values of…” + 각주 4, 식(1)
- **읽기 전 질문**
    - 단어 사이의 관련성 점수가 너무 커져 한 위치에 참고 비율이 몰리면, attention을 학습할 때 어떤 문제가 생길까요?
- **원문 핵심**
    - “We suspect that for large values of $d_k$, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients<sup>4</sup>.”
    - “To counteract this effect, we scale the dot products by $\frac{1}{\sqrt{d_k}}$.”
    - 출처: [§3.2.1 scaling 설명](https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p5.1).
- **확인 질문**
    - 1) Eq.(1)의 나누는 값을 적고, §3.2.1에서 d_k가 무엇의 차원인지 확인하세요. 문장의 토큰 수를 나타내는 값입니까, Q·K 벡터의 차원 수입니까?
    - 2) §3.2.1의 scaling 설명에서, 큰 내적 값이 softmax의 기울기에 어떤 영향을 줄 수 있다고 합니까? 저자가 scaling으로 줄이려는 문제를 그 설명에 근거해 적으세요.
    - 3) 각주 4의 가정 아래 내적의 평균과 분산은 각각 얼마입니까? 그 분산을 기준으로 √d_k로 나눈 뒤의 분산을 계산하세요. 상수 a를 곱하면 분산은 a²배가 된다는 성질을 사용합니다.
- **해석 노트**
    - √d_k는 설정한 차원 수로 정해지는 배율이며 학습 파라미터가 아닙니다. 그래도 softmax를 거쳐 앞쪽 projection으로 전달되는 기울기에 영향을 줍니다.
    - 각주 4의 확률 가정을 학습된 모든 Q·K가 항상 만족한다고 해석하지 않습니다. E01의 관찰도 해당 가정의 범위에서 읽습니다.
- **자료 좌표**: [CS§1](A.ing_Transformer_Cheat_sheet.md#cs1) · [C10](../Week2/A.ing_Transformer_Cookbook.md#c10) · [Q2](A.ing_Transformer_Questions.md#q2) / [A2](transformer_questions_sample_answer.md#a2) · E01

---

<a id="r05"></a>
## R05. Multi-Head: 분할과 결합

- **논문 위치**: §3.2.2 Multi-Head Attention, Fig.2 right + §6.2 Table 3(A)·base 행
- **읽기 전 질문**
    - 한 번의 attention으로 정보를 모으는 대신 여러 갈래로 참고하면 어떤 이점이 있을까요?
    - 갈래 수인 head를 늘리면 항상 좋은 결과가 나올까요?
- **원문 핵심**
    - “Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.”
    - “With a single attention head, averaging inhibits this.”
    - 출처: [§3.2.2 여러 head를 사용하는 이유](https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p2.1).
- **확인 질문**
    - 1) §3.2.2에서 기본 head 수 h와 각 head의 d_k·d_v를 찾으세요. Fig.2 오른쪽에서 head 결과들을 이어 붙이는 부분과, 이어 붙인 결과를 다시 변환하는 부분의 이름은 무엇입니까?
    - 2) Table 3(A)와 base 행에서 h=1·8·32일 때 BLEU를 채우세요: 1개 ___, 8개 ___, 32개 ___. h=8의 결과는 base 행에서 읽으세요.
    - 3) 이 결과는 “head가 많을수록 좋다”는 해석을 뒷받침합니까? 비교한 수치와 §3.2.2의 여러 head를 사용하는 이유를 함께 근거로 설명하세요.
- **해석 노트**
    - Head별 projection과 출력 projection W^O는 번역 손실로 함께 학습됩니다. 실습의 큰 Linear를 계산한 뒤 head로 나누는 방식은 head별 projection을 묶어 계산한 것이며, reshape 자체가 관계를 학습하는 것은 아닙니다.
    - Head의 역할을 명사·동사처럼 미리 지정하지 않습니다. 서로 다른 역할이 가능하다는 것과 모든 head의 역할이 뚜렷이 나뉜다는 것은 다릅니다.
    - Table 3(A)는 head 수와 함께 각 head의 차원도 바뀝니다. Head 수 하나만 독립적으로 늘린 실험으로 읽지 않습니다.
- **자료 좌표**: [CS§2](A.ing_Transformer_Cheat_sheet.md#cs2) · [C2](../Week2/A.ing_Transformer_Cookbook.md#c2) · [C7](../Week2/A.ing_Transformer_Cookbook.md#c7) · [C12](../Week2/A.ing_Transformer_Cookbook.md#c12) · [Q1](A.ing_Transformer_Questions.md#q1) / [A1](transformer_questions_sample_answer.md#a1) · [N-1] [N-5] [N-7] [N-8] [N-9] [N-13]

---

<a id="r06"></a>
## R06. 세 종류의 Attention

- **논문 위치**: §3.2.3 세 항목 — encoder–decoder attention·encoder self-attention·decoder self-attention, Fig.1
- **읽기 전 질문**
    - 번역문 앞부분을 참고하는 것과 원문을 참고하는 것은 어떻게 다를까요?
    - Decoder가 아직 생성하지 않은 번역 토큰과 이미 주어진 원문을 같은 범위로 가려야 할까요?
- **원문 핵심**
    - “In "encoder-decoder attention" layers, the queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder.”
    - “This allows every position in the decoder to attend over all positions in the input sequence.”
    - 출처: [§3.2.3 encoder–decoder attention 항목](https://arxiv.org/html/1706.03762v7#S3.I1.i1.p1.1).
- **확인 질문**
    - 1) §3.2.3의 세 사용 방식에서 Q·K·V가 각각 어디에서 오는지 적으세요. Encoder self-attention, decoder self-attention, encoder–decoder attention의 세 행으로 나누어 정리하세요.
    - 2) Fig.1에서 encoder 출력의 화살표가 들어가는 decoder attention 박스는 아래에서 몇 번째입니까? 이 박스의 다른 입력은 decoder의 어느 앞선 부분에서 옵니까?
    - 3) §3.2.3에서 decoder self-attention이 참고하는 번역문 범위와 encoder–decoder attention이 참고하는 원문 범위를 비교하세요. 번역문의 미래를 가리면서 원문 전체를 참고하는 것이 왜 모순되지 않는지 설명하세요.
- **해석 노트**
    - 인용문의 “previous decoder layer”는 Fig.1의 화살표와 함께 읽습니다. 실습에서 cross-attention의 Q를 만드는 입력은 같은 decoder 블록의 masked self-attention과 Add & Norm을 지난 표현이며, N-22의 query에 해당합니다.
    - Cross-attention은 encoder 표현으로 만든 K·V를 사용합니다. 이 연결을 통해 번역 손실의 기울기가 encoder까지 전달됩니다.
    - 실습은 같은 클래스로 attention 모듈을 여러 개 만들지만, 각 인스턴스의 파라미터는 별개입니다. Source와 target 길이를 다르게 두면 입력 연결 오류를 찾기 쉽습니다.
- **자료 좌표**: [CS§3](A.ing_Transformer_Cheat_sheet.md#cs3) · [C15](../Week2/A.ing_Transformer_Cookbook.md#c15) · [C16](../Week2/A.ing_Transformer_Cookbook.md#c16) · [C17](../Week2/A.ing_Transformer_Cookbook.md#c17) · [N-19] [N-20] [N-22] [N-26]

---

<a id="r07"></a>
## R07. Mask와 정보 누출

- **논문 위치**: §3.1 'Decoder' 마지막 2문장 + §3.2.3 세 번째 항목, Fig.2 left의 Mask
- **읽기 전 질문**
    - 학습 입력의 뒤쪽에 예측할 정답이 이미 있다면, 모델은 어떻게 정답을 미리 볼 수 있을까요?
- **원문 핵심**
    - “We need to prevent leftward information flow in the decoder to preserve the auto-regressive property.”
    - “We implement this inside of scaled dot-product attention by masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections.”
    - 출처: [§3.2.3 decoder self-attention 항목](https://arxiv.org/html/1706.03762v7#S3.I1.i3.p1.1).
- **확인 질문**
    - 1) §3.2.3 마지막 항목에서 decoder self-attention은 현재 입력 위치를 포함합니까? 현재 위치보다 뒤의 입력 위치도 볼 수 있습니까? 허용 범위를 나누어 적으세요.
    - 2) 같은 항목과 Fig.2에서 허용되지 않는 연결의 점수를 어떤 값으로 바꾸는지 찾으세요. 이 처리는 softmax 전입니까, 후입니까? Softmax 이후 그 위치의 참고 비율은 어떻게 됩니까?
    - 3) §3.1의 한 칸 이동과 위 참조 범위를 입력 `[BOS, I, eat, apples]`에 적용하세요. “I” 위치에서 “eat”을 예측할 때 가려야 할 입력은 무엇입니까? Mask가 없다면 학습 때만 정답을 미리 볼 수 있는 이유를 설명하세요.
- **해석 노트**
    - Mask는 학습 대상이 아니라 참조 허용 규칙입니다. 금지된 연결을 가려도 허용된 연결을 만드는 projection 가중치는 학습됩니다.
    - PAD를 참고하지 않게 하는 것과 PAD 위치를 손실에서 제외하는 것은 별개입니다. 실습의 target mask는 causal mask이며 오른쪽 padding과 PAD 손실 제외를 전제로 합니다.
    - 현재 decoder 입력은 지금 예측할 정답보다 한 토큰 앞섭니다. “현재 위치까지 허용”을 정답 토큰을 보여 준다는 뜻으로 읽지 않습니다.
- **자료 좌표**: [CS§4](A.ing_Transformer_Cheat_sheet.md#cs4) · [C3](../Week2/A.ing_Transformer_Cookbook.md#c3) · [C9](../Week2/A.ing_Transformer_Cookbook.md#c9) · [Q5](A.ing_Transformer_Questions.md#q5) / [A5](transformer_questions_sample_answer.md#a5) · [N-11] [N-28] [N-29] [N-30] [N-31] [N-32]

---

<a id="r08"></a>
## R08. Residual·LayerNorm·FFN

- **논문 위치**: §3.1 'Encoder'의 residual·LayerNorm 설명 + §3.3 식(2) + §5.4 'Residual Dropout'
- **읽기 전 질문**
    - 다른 토큰의 정보를 가져오는 attention 뒤에 토큰별 변환인 FFN을 두는 이유는 무엇일까요?
    - Residual 연결로 입력을 더하려면 두 벡터의 크기는 어떤 조건을 만족해야 할까요?
- **원문 핵심**
    - “In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically.”
    - “This consists of two linear transformations with a ReLU activation in between.”
    - 출처: [§3.3 FFN 정의](https://arxiv.org/html/1706.03762v7#S3.SS3.p1.1).
- **확인 질문**
    - 1) §3.1의 출력 식과 §5.4의 Residual Dropout 설명을 함께 읽으세요. 서브레이어 계산·입력과의 덧셈·dropout·LayerNorm을 실제 적용 순서대로 배열하고, 각각의 근거 위치를 적으세요.
    - 2) Eq.(2)와 §3.3에서 FFN의 활성화 함수와 차원을 채우세요: 입력 ___ → 내부 ___ → 출력 ___. 입력과 출력 차원이 같다는 점은 §3.1의 residual 덧셈과 어떻게 연결됩니까?
    - 3) §3.3에서 FFN의 파라미터를 서로 다른 토큰 위치 사이에 공유하는지, 서로 다른 층 사이에도 공유하는지 각각 확인하세요. 같은 층에서 토큰마다 별도의 FFN을 학습한다고 설명해도 됩니까?
- **해석 노트**
    - FFN의 가중치·편향과 LayerNorm의 배율·편향은 학습됩니다. Residual 덧셈과 ReLU에는 파라미터가 없어도 그 경로로 기울기는 전달됩니다.
    - 토큰마다 별도 정답을 주어 FFN을 훈련하지 않습니다. 여러 위치에서 생긴 기울기가 공유 파라미터에 모이며, 최종 번역 손실로 attention과 함께 갱신됩니다.
    - 실습은 Add & Norm 뒤 dropout을 적용합니다. 논문의 서브레이어 출력 → dropout → Add & Norm 순서와 구분해야 합니다.
- **자료 좌표**: [CS§5](A.ing_Transformer_Cheat_sheet.md#cs5) · [C13](../Week2/A.ing_Transformer_Cookbook.md#c13) · [C14](../Week2/A.ing_Transformer_Cookbook.md#c14) · [Q4](A.ing_Transformer_Questions.md#q4) / [A4](transformer_questions_sample_answer.md#a4) · [N-14] [N-15] [N-21]

---

<a id="r09"></a>
## R09. Embedding과 출력 logits

- **논문 위치**: §3.4 Embeddings and Softmax 전체 문단 + §3.1 'Encoder' 마지막 문장, Fig.1 입력·출력단
- **읽기 전 질문**
    - 토큰 ID를 벡터로 만드는 단계와 벡터를 토큰별 점수로 만드는 단계는 어떻게 연결될까요?
- **원문 핵심**
    - “Similarly to other sequence transduction models, we use learned embeddings to convert the input tokens and output tokens to vectors of dimension $d_{\text{model}}$.”
    - “We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities.”
    - 출처: [§3.4 Embeddings and Softmax](https://arxiv.org/html/1706.03762v7#S3.SS4.p1.1).
- **확인 질문**
    - 1) §3.4에서 embedding 벡터의 차원을 나타내는 기호를 찾고, §3.1에서 base 모델의 값을 확인하세요. Decoder의 최종 벡터를 다음 토큰 확률로 바꾸는 두 단계의 이름과 순서도 적으세요.
    - 2) §3.4에서 같은 가중치 행렬을 공유한다고 명시한 세 부분은 어디입니까? 이 중 토큰 ID를 벡터로 바꾸는 부분과 벡터를 토큰별 점수로 바꾸는 부분을 나누세요.
    - 3) §3.4에서 embedding에 곱하는 배율을 찾고, R04의 attention 점수에 적용한 배율과 비교하세요. 각각 무엇에 곱하거나 나누는지, 사용하는 차원 기호는 무엇인지 적으세요.
- **해석 노트**
    - Embedding lookup은 정수 ID를 바꾸는 연산이 아닙니다. 선택한 행의 벡터가 학습 대상이며, 가중치 공유 시에는 출력 변환 경로의 기울기도 같은 행렬에 모입니다.
    - 실습은 source·target·output 가중치를 공유하지 않고 embedding 배율도 생략합니다. 논문의 가중치 공유를 구현한 코드로 소개하지 않습니다.
    - Softmax에는 학습 파라미터가 없습니다. 실습의 CrossEntropyLoss에는 softmax 전 점수인 logits를 전달합니다.
- **자료 좌표**: [CS§6](A.ing_Transformer_Cheat_sheet.md#cs6) · [CS§7](A.ing_Transformer_Cheat_sheet.md#cs7) · [C4](../Week2/A.ing_Transformer_Cookbook.md#c4) · [C18](../Week2/A.ing_Transformer_Cookbook.md#c18) · [N-27]

---

<a id="r10"></a>
## R10. 위치 정보

- **논문 위치**: §3.5 첫 문단·두 식·마지막 문단 + §6.2 Table 3(E)·base 행
- **읽기 전 질문**
    - 단어의 의미를 나타내는 벡터만으로 문장 속 순서까지 구별할 수 있을까요?
    - 위치 정보를 고정된 함수로 만드는 것과 학습하는 것에는 어떤 차이가 있을까요?
- **원문 핵심**
    - “Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.”
    - “To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks.”
    - 출처: [§3.5 위치 정보 도입 이유](https://arxiv.org/html/1706.03762v7#S3.SS5.p1.1).
- **확인 질문**
    - 1) §3.5 첫 문단에서 위치 정보를 별도로 넣는 이유를 찾으세요. Fig.1에서 위치 정보가 encoder와 decoder의 어느 부분에 더해지는지 표시하세요.
    - 2) Table 3(E)와 base 행의 PPL·BLEU를 채우세요: base ___/___, 학습형 위치 표현 ___/___. 바뀐 조건은 무엇이며 결과 차이는 어떻습니까?
    - 3) §3.5 마지막 문단에서 결과가 비슷한데도 sine·cosine 방식을 선택한 이유는 무엇입니까? 저자가 기대한 효과와 Table 3(E)에서 실제 비교한 결과를 구분해 적으세요.
- **해석 노트**
    - 고정 sine·cosine 표현에는 학습 파라미터가 없고, 실습의 위치 embedding에는 있습니다. 위치 번호 자체를 학습하는 것은 아닙니다.
    - 위치 벡터가 고정되어도 이후 층은 그 정보를 사용하는 방법을 학습합니다. “위치 표현을 학습하지 않는다”를 “위치 정보를 활용하지 않는다”로 읽지 않습니다.
    - Table 3(E)의 번역 결과만으로 훈련보다 긴 모든 시퀀스에 대한 성능을 보장할 수는 없습니다. E02 역시 작은 관찰 실험입니다.
- **자료 좌표**: [CS§6](A.ing_Transformer_Cheat_sheet.md#cs6) · [C5](../Week2/A.ing_Transformer_Cookbook.md#c5) · [N-16] [N-17] [N-18] [N-23] [N-24] [N-25] · E02

---

<a id="r11"></a>
## R11. 복잡도와 경로 길이

- **논문 위치**: §4 첫 3문단, Table 1 — 열 제목·Self-Attention 행
- **읽기 전 질문**
    - 두 단어가 적은 단계를 거쳐 연결된다는 것이 계산량도 적다는 뜻일까요?
- **원문 핵심**
    - “Learning long-range dependencies is a key challenge in many sequence transduction tasks.”
    - “One key factor affecting the ability to learn such dependencies is the length of the paths forward and backward signals have to traverse in the network.”
    - 출처: [§4 경로 길이 설명](https://arxiv.org/html/1706.03762v7#S4.p3.1).
- **확인 질문**
    - 1) §4에서 제시한 세 비교 기준을 찾으세요. Table 1의 열 제목과 연결해 각각 무엇을 비교하는 기준인지 적으세요.
    - 2) Table 1의 Self-Attention 행에서 층당 계산량·순차 연산 수·최대 경로 길이를 각각 채우세요. 여기서 n은 문장 길이, d는 표현 차원입니다.
    - 3) 표에서 n이 커질 때 함께 커지는 값과 일정하게 표시된 값을 구분하세요. “먼 위치를 직접 참고할 수 있으므로 긴 문장에서도 계산 부담이 늘지 않는다”는 해석이 맞습니까? 해당 열을 근거로 답하세요.
- **해석 노트**
    - 짧은 정보 전달 경로와 작은 계산 비용은 별개입니다. 일반적인 attention 점수표는 토큰 쌍마다 값이 있어 길이에 따라 제곱으로 커집니다.
    - 표의 attention 연산량은 projection·FFN까지 포함한 전체 모델의 실행 시간이 아닙니다. 실제 학습에는 역전파 비용과 중간값 보관도 필요합니다.
- **자료 좌표**: [Q3](A.ing_Transformer_Questions.md#q3) / [A3](transformer_questions_sample_answer.md#a3)

---

<a id="r12"></a>
## R12. 학습 레시피와 교육용 설정

- **논문 위치**: §5.1~§5.4 Training — 데이터·배치·학습 step·optimizer·regularization, 식(3)
- **읽기 전 질문**
    - 번역을 틀렸다는 결과가 encoder와 decoder의 가중치 변경으로 어떻게 이어질까요?
    - 같은 모델이라도 학습 시간과 설정이 다르면 점수를 바로 비교해도 될까요?
- **원문 핵심**
    - “During training, we employed label smoothing of value $\epsilon_{ls} = 0.1$ [36].”
    - “This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.”
    - 출처: [§5.4 Label Smoothing](https://arxiv.org/html/1706.03762v7#S5.SS4.SSS0.Px2.p1.1).
- **확인 질문**
    - 1) §5.1에서 한 배치에 포함하는 source와 target 토큰 수를 각각 찾으세요. §5.2에서 base와 big의 학습 step 수를 비교하고, 두 모델을 같은 학습 예산으로 비교한 것인지 확인하세요.
    - 2) §5.3에서 optimizer 이름과 warmup step 수를 채우세요: ___, ___ steps. Eq.(3)과 이어지는 설명에서 warmup 이전과 이후 학습률이 어떻게 변하는지 적으세요.
    - 3) §5.4에서 dropout의 적용 위치와 base의 비율, label smoothing 값을 찾으세요. Label smoothing을 적용했을 때 perplexity와 BLEU가 어떻게 달라졌다고 보고하는지 적으세요.
- **해석 노트**
    - 역전파는 손실에 대한 기울기를 계산하고 optimizer는 그 기울기를 사용해 파라미터를 갱신합니다. 각 모듈을 별도 정답으로 따로 훈련하지 않습니다.
    - Dropout은 학습 중 내부 값을 일부 가리고, label smoothing은 학습용 정답 분포를 조정합니다. 두 비율과 학습률 스케줄 자체를 optimizer가 학습하는 것은 아닙니다.
    - Epoch만으로 학습 예산을 비교하지 않습니다. 데이터 규모·처리한 토큰 수·갱신 step 수를 함께 기록해야 합니다.
- **자료 좌표**: [빈칸 노트북](../Week2/A.ing_Transformer_from_scratch_blank.ipynb)의 §8 Multi30k 학습·평가 / 관찰 기록

**학습 흐름과 갱신 대상 — 교육용 정리**

`원문 + 정답 앞부분 → 토큰별 점수 → 손실 → 역전파로 기울기 계산 → optimizer 갱신`

`[BOS, I, eat, apples]`로 `[I, eat, apples, EOS]`를 예측합니다. Label smoothing을 생략하면 입력 “I”에서 정답 “eat”을 예측하는 위치의 손실은 `−log P(eat)`입니다. PAD를 제외한 위치들의 손실을 모아, 출력단에서 decoder와 cross-attention을 거쳐 encoder까지 연결된 파라미터의 기울기를 계산합니다. Argmax로 선택한 토큰 ID가 아니라 토큰별 점수에서 손실을 계산합니다.

이전 step의 기울기를 초기화한 뒤 역전파를 수행하고 optimizer로 갱신합니다. 같은 파라미터를 여러 위치에서 사용했다면 그 위치들의 기여가 모입니다. 파라미터는 학습되는 가중치·편향이고, 기울기는 그 변화가 손실에 미치는 영향을 나타냅니다. [역전파와 파라미터 갱신의 구분](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)을 함께 참고할 수 있습니다.

| 모듈·연산 | 학습으로 갱신하는 것 | 스스로 학습하지 않는 것 |
| --- | --- | --- |
| 토큰 embedding | 토큰별 벡터가 담긴 가중치 표 | 토큰 ID, 행을 찾는 연산 |
| Multi-head attention | Q·K·V projection과 출력 projection의 가중치; 실습의 Linear는 편향도 갱신 | 입력마다 계산되는 attention 비율표를 독립 파라미터로 갱신하지 않음 |
| Scaling·softmax·mask | 별도 파라미터 없음; 연결된 앞쪽 가중치에 기울기 전달 | 차원에 따른 배율, 정규화 연산, 참조 허용 규칙 |
| FFN | 두 선형 변환의 가중치와 편향 | ReLU 연산 |
| Residual·LayerNorm | LayerNorm의 배율과 편향 | 덧셈, 입력에서 계산한 평균·분산 |
| 위치 표현 | 학습형 위치 embedding의 벡터 | 고정 sine·cosine 표현, 위치 번호 |
| 출력 Linear | 토큰별 점수로 바꾸는 가중치와 사용하는 경우 편향 | 사전의 토큰 목록 |

고정 연산에도 기울기 계산이 지나갈 수 있습니다. “학습 파라미터가 없다”는 말은 “앞쪽 가중치의 학습에 영향을 주지 않는다”는 뜻이 아닙니다. 어떤 파라미터는 해당 step에서 기울기가 0일 수 있습니다. 한 번의 갱신으로 모든 문장의 예측이 좋아진다고 보장하지도 않습니다.

**원논문과 Week 2 교육용 구현의 차이**

| 항목 | 원논문 기준 | Week2 교육용 구현 |
|---|---|---|
| 전체 구조·크기 | Encoder–Decoder, Fig.1; base는 각 6층·d_model=512·8 heads | Multi30k 기본값도 각 6층·512차원·8 heads; 작은 실행 검사는 별도 축소 모델 |
| 위치 표현 | sinusoidal 기본, learned도 비교 | learned position embedding |
| embedding | √d_model 배율, 가중치 공유 | 배율 없음, source/target/output 가중치 독립 |
| residual dropout | 서브레이어 출력에 dropout 후 Add & Norm (§5.4) | Add & Norm 뒤 dropout; 원논문과 위치가 다름 |
| target mask | 미래 정보 차단과 shifted output | causal mask만 생성; 오른쪽 PAD와 PAD loss 제외 사용 |
| 데이터·토큰화 | WMT 번역 데이터, subword | Multi30k de→en, spaCy 단어 단위 |
| 학습 | base 100,000 steps; 배치당 source·target 각각 약 25,000 tokens | 기본 실행 1 epoch·64문장/batch; Adam 설정·warmup 4,000·label smoothing 0.1 채택 |
| 평가 | beam search(beam=4); Table 2는 checkpoint 평균, Table 3은 평균 없음 | greedy, test 앞 최대 200문장·소문자 BLEU; 평가 loss는 smoothing 없는 토큰 평균, 논문 BLEU와 직접 비교하지 않음 |

Week 2 교육용 구현은 Colab에서 제한된 시간 안에 학습을 진행할 수 있도록 데이터 규모와 모델·학습·평가 설정을 조정했습니다.

---

<a id="r13"></a>
## R13. 실험 결과를 읽는 방법

- **논문 위치**: §6.1 + §6.2 첫 문단, Table 2·Table 3 caption 및 base·big·(D) 행
- **읽기 전 질문**
    - 더 큰 모델의 점수가 높으면 크기만의 효과라고 결론 내려도 될까요?
    - 정답 토큰을 예측하는 지표와 생성한 번역문을 평가하는 지표는 항상 함께 좋아질까요?
- **원문 핵심**
    - “To evaluate the importance of different components of the Transformer, we varied our base model in different ways, measuring the change in performance on English-to-German translation on the development set, newstest2013.”
    - “We used beam search as described in the previous section, but no checkpoint averaging.”
    - 출처: [§6.2 설정 변경 실험의 평가 조건](https://arxiv.org/html/1706.03762v7#S6.SS2.p1.1).
- **확인 질문**
    - 1) Table 2에서 Transformer base와 big의 EN–DE BLEU와 학습 비용을 채우세요. R12에서 확인한 학습 step 수를 함께 고려할 때, 점수 차이를 모델 크기만의 효과라고 말할 수 있습니까?
    - 2) Table 2·3의 caption과 §6.1·§6.2에서 평가 데이터와 checkpoint 평균 사용 여부를 각각 찾으세요. Table 3의 PPL 단위도 확인하고, 두 표의 base BLEU를 바로 비교해도 되는지 설명하세요.
    - 3) Table 3(D)에서 label smoothing을 제거한 행과 base 행의 PPL·BLEU를 각각 비교하세요. PPL이 좋아지면 번역 품질도 반드시 좋아진다는 주장을 이 결과가 뒷받침합니까? 두 수치의 변화를 근거로 답하세요.
- **해석 노트**
    - Table 2의 base·big은 크기뿐 아니라 학습 예산도 다릅니다. 점수 차이를 구조 하나의 효과로 단정하지 않습니다.
    - Table 3의 PPL은 wordpiece 단위입니다. 다른 토큰화의 PPL이나 label smoothing을 포함한 학습 손실과 그대로 비교하지 않습니다.
    - 검증에서는 가중치를 갱신하지 않습니다. 이 실습은 토큰별 손실로 학습하고 BLEU는 생성한 번역문에서 별도로 평가합니다.
- **자료 좌표**: [빈칸 노트북](../Week2/A.ing_Transformer_from_scratch_blank.ipynb)의 §8 Multi30k 학습·평가 / 관찰 기록

---

## 부록 A — 논문 → R 커버리지

| 논문 위치 | 담당 R |
| --- | --- |
| §1 Introduction | [R01](#r01) |
| §3 전체 구조 / §3.1 Encoder and Decoder Stacks | [R02](#r02), [R07](#r07), [R08](#r08) |
| §3.2 Attention 정의 / §3.2.1 Scaled Dot-Product Attention / Eq.(1) | [R03](#r03), [R04](#r04) |
| §3.2.2 Multi-Head Attention | [R05](#r05) |
| §3.2.3 Applications of Attention | [R06](#r06), [R07](#r07) |
| §3.3 Position-wise FFN / Eq.(2) | [R08](#r08) |
| §3.4 Embeddings and Softmax | [R09](#r09) |
| §3.5 Positional Encoding | [R10](#r10) |
| §4 Why Self-Attention / Table 1 | [R11](#r11) |
| §5.1–5.4 Training / Eq.(3) | [R12](#r12); dropout 위치는 [R08](#r08) |
| §6.1 Machine Translation / Table 2 | [R13](#r13) |
| §6.2 Model Variations / Table 3 | [R13](#r13); head 수는 [R05](#r05), 위치 표현은 [R10](#r10); (B)·(C)의 개별 설정 분석은 다루지 않음 |
| §2 Background / §6.3 / §7 / Attention Visualizations | 범위 밖 |

## 부록 B — 자료 → R 매핑

### 치트시트·쿡북·퀴즈

| 자료 절 | 담당 R |
| --- | --- |
| 치트시트 CS§0 전체 구조 | [R01](#r01), [R02](#r02) |
| 치트시트 CS§1 Scaled Dot-Product Attention | [R03](#r03), [R04](#r04) |
| 치트시트 CS§2 Multi-Head Attention | [R05](#r05) |
| 치트시트 CS§3 세 attention | [R06](#r06) |
| 치트시트 CS§4 Mask | [R07](#r07) |
| 치트시트 CS§5 Add & Norm + FFN | [R08](#r08) |
| 치트시트 CS§6 Embedding + 위치 정보 | [R09](#r09), [R10](#r10) |
| 치트시트 CS§7 출력 logits | [R09](#r09) |
| 쿡북 C0 nn.Module | 구현 준비; 직접 대응하는 논문 절 없음 |
| 쿡북 C1 입력 shape / C19 전체 실행 | [R02](#r02) |
| 쿡북 C2 head 조건 / C7 reshape / C12 head 결합 | [R05](#r05) |
| 쿡북 C3 mask 생성 / C9 mask 적용 | [R07](#r07) |
| 쿡북 C4 token embedding / C18 출력 projection | [R09](#r09) |
| 쿡북 C5 위치 embedding | [R10](#r10) |
| 쿡북 C6 QKV projection / C8 점수 / C11 가중합 | [R03](#r03) |
| 쿡북 C10 scaling과 softmax | [R04](#r04) |
| 쿡북 C13 Add & Norm / C14 FFN | [R08](#r08) |
| 쿡북 C15 encoder / C16 decoder self-attention / C17 cross-attention | [R06](#r06) |
| 퀴즈 Q1 / 해설 A1 | [R05](#r05) |
| 퀴즈 Q2 / 해설 A2 | [R04](#r04) |
| 퀴즈 Q3 / 해설 A3 | [R01](#r01), [R11](#r11) |
| 퀴즈 Q4 / 해설 A4 | [R08](#r08) |
| 퀴즈 Q5 / 해설 A5 | [R02](#r02), [R07](#r07) |

### 노트북 빈칸·실험

| 자료 좌표 | 담당 R |
| --- | --- |
| N-1, N-5, N-7–N-9, N-13: head 분할·결합 | [R05](#r05) |
| N-2–N-4, N-10, N-12: QKV·점수·가중합 | [R03](#r03) |
| N-6, N-33–N-36: 배치 크기와 전체 입력 연결 | [R02](#r02) |
| N-11, N-28–N-32: mask 적용·생성 | [R07](#r07) |
| N-14–N-15, N-21: residual·normalization·FFN | [R08](#r08) |
| N-16–N-18, N-23–N-25: embedding·위치 입력 구성 | [R10](#r10); 토큰 표현의 배경은 [R09](#r09) |
| N-19–N-20, N-22: 세 attention의 입력 연결 | [R06](#r06) |
| N-26: decoder 스택의 입력 연결 | [R02](#r02), [R06](#r06) |
| N-27: 출력 projection | [R09](#r09) |
| E01 scaling 관찰 | [R04](#r04) |
| E02 위치 정보 관찰 | [R10](#r10) |
| 선택 Multi30k 학습·평가와 관찰 기록 | [R12](#r12), [R13](#r13) |

빈칸이 없는 제공 코드에도 논문 근거가 있습니다. 예를 들어 scaling은 R04·C10에서, 학습 조건은 R12에서 확인합니다.
