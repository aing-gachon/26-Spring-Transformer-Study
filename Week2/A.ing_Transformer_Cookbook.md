# A.ing Transformer CookBook

각 절의 `> 허브:` 표기는 [논문 가이드](../Week1/transformer_paper_guide.md)의 R 항목을 가리킵니다. 개념 요약은 [치트시트](../Week1/A.ing_Transformer_Cheat_sheet.md), 자기점검은 [퀴즈](../Week1/A.ing_Transformer_Questions.md) 참고.

각 절 머리의 `> 대응:` 표기는 그 절이 담당하는 **치트시트 절 `[CS§n]`과 노트북 빈칸 `[N-k]`**입니다. 노트북에서 막히면 그 빈칸 번호로 여기 절을 찾으시면 됩니다.

[source: Week2/A.ing_Transformer_Cookbook.md]

---

<a id="c0"></a>
## [0] 먼저 읽기 — `nn.Module`  `[C0]`

[빈칸 노트북](A.ing_Transformer_from_scratch_blank.ipynb)의 빈칸 36개는 모두 아래와 같은 **클래스 안**에 있습니다. Transformer 전체 구조에 들어가기 전에 가장 단순한 블록으로 틀을 봅시다. 지금은 Linear와 ReLU의 계산보다 부품을 만들고 연결하는 방법에 집중하세요. 두 모듈은 아래에서 더 자세히 다룹니다.

```python
import torch
from torch import nn

class TinyBlock(nn.Module):
    def __init__(self):             # ① 부품을 만들어 두는 곳
        super().__init__()         # 모듈을 등록하기 전에 부모 클래스 초기화
        self.project = nn.Linear(7, 11)
        self.activation = nn.ReLU()

    def forward(self, x):          # ② 만들어 둔 부품을 쓰는 곳
        h = self.project(x)
        h = self.activation(h)
        return h
```

실행하면:

```python
block = TinyBlock()
y = block(torch.randn(2, 3, 7))     # block(...)을 호출하면 forward가 실행됩니다
print(y.shape)                     # torch.Size([2, 3, 11])
```

### 여기서 가져갈 것 셋

**(1) `__init__`은 만들고, `forward`는 씁니다.**
`self.project = nn.Linear(7, 11)`은 입력 특징 7개를 출력 특징 11개로 바꾸는 레이어를 저장합니다. 실제 데이터는 `forward`의 `self.project(x)`에 넣습니다. 생성할 때 괄호 안에는 **설정값**, 실행할 때는 **데이터**가 들어갑니다. 학습할 레이어를 `forward`에서 매번 새로 만들면 이전 호출에서 학습한 파라미터를 이어 쓸 수 없습니다.

**(2) 저장한 이름 그대로 부릅니다.**
`self.project`로 저장했으면 같은 이름으로 호출합니다. 노트북에는 `W_Q`, `W_K`, `W_V`, `norm1`, `norm2`처럼 역할이나 번호가 붙은 이름이 있습니다. 빈칸을 채우기 전에 해당 클래스의 `__init__`에서 **실제로 어떤 이름으로 저장했는지** 확인하세요. 없는 이름을 부르면 `AttributeError`가 납니다.

**(3) 앞의 결과를 다음 입력으로 넘깁니다.**
`h = self.project(x)` 다음에는 `self.activation(h)`가 와야 합니다. 이 예에서 실수로 `self.activation(x)`를 쓰면 선형 변환 결과가 버려집니다. 코드가 실행되더라도 의도한 계산은 아닙니다. 노트북의 `x`, `out`, `query`도 각 단계에서 무엇을 담고 있는지 확인하며 이어 주세요.

### 자주 나오는 모양 셋

| 모양 | 언제 | 왜 |
| --- | --- | --- |
| `nn.Linear(in_features, out_features)` | 특징 차원을 바꿀 때 | 앞쪽 배치·길이 축을 유지하고 마지막 축만 변환합니다 → [C6](#c6) |
| `nn.Sequential(...)` | 여러 모듈을 정해진 순서로 실행할 때 | 앞 모듈의 출력을 다음 모듈의 입력으로 자동 전달합니다 → [C14](#c14) |
| `nn.ModuleList([...])` | 여러 블록을 저장하고 직접 반복할 때 | 파라미터를 등록하면서 블록마다 여러 인자를 전달할 수 있습니다 → [C15](#c15) |

> **`ModuleList`와 `Sequential`의 차이**: `ModuleList`는 모듈을 보관하지만 스스로 차례대로 실행하지 않습니다. `for layer in self.layers:` 안에서 직접 호출해야 합니다. `Sequential`은 입력 하나를 받아 모듈들을 순서대로 실행하는 FFN에 적합합니다.

이 문서의 작은 예제는 API 사용법을 보여 줍니다. 전체 구현은 [정답 노트북](A.ing_Transformer_from_scratch_answer.ipynb)을 참고하세요. `SelfAttention`, `TransformerBlock`, `DecoderBlock`은 PyTorch 기본 API가 아니라 노트북에서 만드는 클래스입니다.

Shape는 `(배치, 길이, 특징)` 순서로 읽습니다. 아래에서는 `N`을 배치 크기, `S`를 source 길이, `T`를 decoder 입력 길이, `E`를 모델 차원, `h`를 head 수, `d_k = E / h`를 head 차원으로 씁니다. 예시는 주로 `N=2, S=5, T=3, E=12, h=3, d_k=4`입니다. 어휘 크기는 head 수와 구별해 `Vocab`으로 표기합니다.

---

<a id="c1"></a>
## **[1) 입력 토큰 텐서와 Shape]**  `[C1]`

> 허브: [R02](../Week1/transformer_paper_guide.md#r02)
> 대응: [CS§6](../Week1/A.ing_Transformer_Cheat_sheet.md#cs6) · [N-6]

문장은 먼저 토큰 ID의 나열로 바뀝니다. 토큰 ID와 임베딩 벡터를 구별해야 이후의 축을 올바르게 읽을 수 있습니다.

<a id="c1-1"></a>
### 1. Tensor 생성과 크기 확인  `[C1-1]`

> 대응: [N-6]

- **코드**
    - `torch.tensor()` : 리스트 등의 데이터로 텐서를 생성
    - `tensor.shape`, `tensor.size()` : 각 축의 크기를 확인
- **패턴**
    - `torch.tensor([[1, 2, 0], [3, 4, 5]], dtype=torch.long)`
    - `batch_size = x.shape[0]`
- **설명**: 한 행은 한 문장이고, 각 칸은 어휘 사전의 정수 ID입니다. ID의 숫자 자체가 의미 벡터는 아닙니다. 임베딩을 통과한 뒤에 특징 축이 생깁니다.
- **코드 사용법**
    - 토큰 ID는 `torch.long`으로 준비합니다. source와 target은 배치 크기가 같아도 길이는 다를 수 있습니다.
    - `shape[0]`은 배치, `shape[1]`은 길이입니다. `[N-6]`에서는 토큰 ID가 아니라 attention에 전달된 `query`에서 배치 크기를 읽습니다.
    - ID를 담은 `(N, L)`과 특징을 담은 `(N, L, E)`를 혼동하지 마세요.
- **Shape 흐름**
    - **Input:** 정수 리스트 `[[1, 2, 0], [3, 4, 5]]`
    - **Operation:** `torch.tensor(..., dtype=torch.long)`로 변환
    - **Output:** 토큰 ID `(2, 3)`; 임베딩 이후에는 `(2, 3, E)`

---

<a id="c2"></a>
## **[2) Multi-Head 분해 조건]**  `[C2]`

> 허브: [R05](../Week1/transformer_paper_guide.md#r05)
> 대응: [CS§2](../Week1/A.ing_Transformer_Cheat_sheet.md#cs2) · [N-1]

여러 head가 서로 다른 관계를 계산하도록 모델의 특징 축을 나눕니다. 이 노트북은 모든 head의 차원을 같게 설정합니다.

<a id="c2-1"></a>
### 1. 나머지 검사와 정수 나눗셈  `[C2-1]`

> 대응: [N-1]

- **코드**
    - `assert` : 조건이 거짓이면 중단하는 Python 문법
    - `%`, `//` : 나머지와 정수 나눗셈
- **패턴**
    - `assert embed_size % heads == 0`
    - `head_dim = embed_size // heads`
- **설명**: 특징 12개를 head 3개로 나누면 각 head에는 특징 4개가 들어갑니다. 나누는 대상은 문장 길이가 아니라 마지막 특징 축입니다.
- **코드 사용법**
    - `heads`는 양의 정수여야 합니다. `E=10, h=3`처럼 나누어떨어지지 않는 설정은 사용할 수 없습니다.
    - `/`는 실수를 반환하므로 shape에 넣을 차원은 `//`로 구합니다.
    - 빈칸 `[N-1]`은 `self.d_model`을 `self.h`로 나누는 head 차원 계산입니다. 나누어떨어지는지 확인하는 `assert`는 제공됩니다. 서로 다른 단어를 head별로 나눠 맡기는 규칙이 아닙니다.
- **Shape 흐름**
    - **Input:** 설정값 `E=12`, `h=3`
    - **Operation:** `12 % 3 == 0` 확인 후 `12 // 3` 계산
    - **Output:** `d_k=4`; 텐서 자체는 아직 변하지 않음

---

<a id="c3"></a>
## **[3) Source Padding Mask와 Target Causal Mask]**  `[C3]`

> 허브: [R07](../Week1/transformer_paper_guide.md#r07)
> 대응: [CS§4](../Week1/A.ing_Transformer_Cheat_sheet.md#cs4) · [N-28] · [N-29] · [N-30] · [N-31] · [N-32]

마스크는 attention이 참고해도 되는 위치를 표시합니다. 이 노트북에서는 `True` 또는 `1`이 허용, `False` 또는 `0`이 차단입니다.

<a id="c3-1"></a>
### 1. 비교 연산과 `unsqueeze`  `[C3-1]`

> 대응: [N-28] · [N-29] · [N-30]

- **코드**
    - `!=` : PAD가 아닌 위치를 비교
    - `tensor.unsqueeze(dim)` : 크기가 1인 축을 추가
- **패턴**
    - `valid = token_ids != pad_idx`
    - `mask = valid.unsqueeze(1).unsqueeze(2)`
- **설명**: Source의 PAD는 실제 단어가 아니므로 key로 참고하지 않도록 가립니다. head 축과 query 축을 크기 1로 만들어 모든 head와 query가 같은 source 유효 위치를 공유하게 합니다.
- **코드 사용법**
    - `unsqueeze`는 기존 원소를 복제하지 않고 축을 추가합니다. `(N, S)`에 첫 번째 축을 추가하면 `(N, 1, S)`, 이어 두 번째 축을 추가하면 `(N, 1, 1, S)`입니다.
    - 마지막 축은 항상 source의 key 길이 `S`여야 합니다. Encoder self-attention과 decoder cross-attention 모두 이 마스크를 사용합니다.
    - 마스크는 PAD key를 가립니다. PAD인 query 위치의 출력 벡터까지 자동으로 0이 되는 것은 아닙니다.
- **Shape 흐름**
    - **Input:** source ID `(2, 5)`
    - **Operation:** PAD 비교 → `(2, 5)` → 축 두 개 추가
    - **Output:** source mask `(2, 1, 1, 5)`

<a id="c3-2"></a>
### 2. `ones`, `tril`, `expand`, `to`  `[C3-2]`

> 대응: [N-31] · [N-32]

- **코드**
    - `torch.ones()` : 1로 채운 텐서 생성
    - `torch.tril()` : 대각선과 아래쪽을 남기고 위쪽을 0으로 변경
    - `tensor.expand()` : 크기 1인 축이나 새 앞쪽 축을 확장
    - `tensor.to(device)` : 지정한 장치로 이동
- **패턴**
    - `triangle = torch.tril(torch.ones(3, 3))`
    - `mask = triangle.expand(2, 1, 3, 3).to(device)`
- **설명**: Target의 각 query는 자기 위치와 앞쪽 key만 참고해야 합니다. 행이 query, 열이 key이므로 아래 삼각형을 남깁니다. 대각선을 포함하는 이유는 현재 decoder 입력 토큰까지는 이미 주어진 정보이기 때문입니다.
- **코드 사용법**
    - 길이 `T`에 대해 정사각형 `(T, T)`을 만듭니다. `T=3`이면 행별 허용 값은 `[1,0,0]`, `[1,1,0]`, `[1,1,1]`입니다.
    - `expand`는 데이터를 복사해 배치를 만드는 방식이 아닙니다. 확장한 텐서에 직접 값을 쓰는 작업은 피하세요.
    - 노트북의 target mask는 causal mask입니다. 오른쪽 PAD를 쓰고 PAD 정답은 loss에서 제외하는 학습 흐름을 전제로 합니다. 왼쪽 PAD 등 다른 배치 방식에는 추가 처리가 필요합니다.
    - 새로 생성한 마스크와 attention 점수는 같은 장치에 있어야 합니다. `device`는 모델이 사용하는 장치로 준비합니다.
- **Shape 흐름**
    - **Input:** target ID `(2, 3)`에서 읽은 길이 `T=3`
    - **Operation:** `ones` → `tril`: `(3, 3)` → 배치·head 축 확장
    - **Output:** target mask `(2, 1, 3, 3)`

---

<a id="c4"></a>
## **[4) 토큰 ID를 임베딩 벡터로 변환]**  `[C4]`

> 허브: [R09](../Week1/transformer_paper_guide.md#r09)
> 대응: [CS§6](../Week1/A.ing_Transformer_Cheat_sheet.md#cs6) · 제공 코드 이해 / 준비 단계

임베딩은 어휘 사전의 각 토큰에 대응하는 학습 가능한 벡터 표입니다.

<a id="c4-1"></a>
### 1. `nn.Embedding`  `[C4-1]`

> 대응: 제공 코드 이해 / 준비 단계

- **코드**
    - `nn.Embedding(num_embeddings, embedding_dim)` : ID에 해당하는 벡터 조회
- **패턴**
    - `embedding = nn.Embedding(100, 12)`
    - `vectors = embedding(token_ids)`
- **설명**: 토큰 ID 하나를 길이 `E`의 벡터로 바꿉니다. 같은 임베딩 층에서 같은 ID를 조회하면 같은 벡터가 나오며, 이 벡터는 학습 과정에서 갱신됩니다. 문맥에 따른 변화는 뒤의 attention 블록에서 만들어집니다.
- **코드 사용법**
    - `num_embeddings`는 어휘 크기, `embedding_dim`은 모델 차원 `E`입니다.
    - ID는 `0` 이상 `num_embeddings` 미만이어야 합니다. 범위를 벗어나면 인덱스 오류가 납니다.
    - `nn.Embedding`의 출력이 PAD 위치에서 자동으로 0이라고 가정하지 마세요. 이 노트북에서는 PAD를 참고하지 않도록 별도 마스크를 만듭니다.
- **Shape 흐름**
    - **Input:** source ID `(2, 5)`
    - **Operation:** ID마다 길이 12인 벡터 조회
    - **Output:** 임베딩 `(2, 5, 12)`

---

<a id="c5"></a>
## **[5) 위치 임베딩과 입력 표현]**  `[C5]`

> 허브: [R10](../Week1/transformer_paper_guide.md#r10)
> 대응: [CS§6](../Week1/A.ing_Transformer_Cheat_sheet.md#cs6) · [N-16] · [N-17] · [N-18] · [N-23] · [N-24] · [N-25]

Attention에 토큰의 순서를 알려 주기 위해 토큰 벡터에 위치 벡터를 더합니다. 노트북은 학습형 위치 임베딩을 사용합니다.

<a id="c5-1"></a>
### 1. 위치 ID 생성과 임베딩 덧셈  `[C5-1]`

> 대응: [N-16] · [N-17] · [N-18] · [N-23] · [N-24] · [N-25]

- **코드**
    - `torch.arange()` : 연속된 위치 번호 생성
    - `tensor.expand()` : 같은 위치 번호를 배치에 공유
    - `nn.Embedding()` : 위치 번호를 위치 벡터로 변환
- **패턴**
    - `positions = torch.arange(length, device=device).expand(batch_size, length)`
    - `position_vectors = self.position_embedding(positions)`
    - `combined = token_vectors + position_vectors`
- **설명**: 위치 0, 1, 2에는 서로 다른 학습 가능한 벡터가 대응합니다. 토큰 정보와 위치 정보를 더하면 모델 차원은 그대로 유지하면서 단어와 순서를 함께 담을 수 있습니다.
- **코드 사용법**
    - `self.position_embedding`은 `__init__`에서 저장한 모듈 이름입니다. PyTorch에 같은 이름의 기본 함수가 있는 것은 아닙니다.
    - 위치 임베딩 표가 `nn.Embedding(max_length, E)`라면 입력 길이는 `max_length`를 넘을 수 없습니다.
    - source와 target은 각각 자기 길이로 위치 ID를 만듭니다. 두 임베딩의 shape가 같아야 위치별로 더할 수 있습니다.
    - 더한 결과에 dropout을 적용합니다. 원논문의 sinusoidal positional encoding 및 토큰 임베딩의 배율과 현재 실습 설정은 [CS§6](../Week1/A.ing_Transformer_Cheat_sheet.md#cs6)에서 구별해 읽으세요.
- **Shape 흐름**
    - **Input:** 위치 ID `(5,)`, 토큰 벡터 `(2, 5, 12)`
    - **Operation:** 위치 ID 확장 `(2, 5)` → 위치 임베딩 `(2, 5, 12)` → 덧셈
    - **Output:** 입력 표현 `(2, 5, 12)`

---

<a id="c6"></a>
## **[6) Q·K·V 선형 변환]**  `[C6]`

> 허브: [R03](../Week1/transformer_paper_guide.md#r03)
> 대응: [CS§1](../Week1/A.ing_Transformer_Cheat_sheet.md#cs1) · [N-2] · [N-3] · [N-4]

Attention은 query로 참고할 정보를 찾고, key로 관련도를 계산하며, value의 내용을 가져옵니다. 각 역할에 맞는 표현을 학습하도록 별도의 선형 변환을 만듭니다.

<a id="c6-1"></a>
### 1. `nn.Linear`  `[C6-1]`

> 대응: [N-2] · [N-3] · [N-4]

- **코드**
    - `nn.Linear(in_features, out_features)` : 마지막 특징 축에 학습 가능한 선형 변환 적용
- **패턴**
    - `projection = nn.Linear(12, 12)`
    - `projected = projection(hidden)`
- **설명**: 입출력 차원이 같아도 값은 달라집니다. `Linear(E, E)`는 아무것도 하지 않는 층이 아니라 학습 가능한 가중치와 편향으로 특징을 조합하는 층입니다.
- **코드 사용법**
    - `W_Q`, `W_K`, `W_V`는 각각 별도의 `nn.Linear` 인스턴스로 만듭니다. 하나의 인스턴스를 여러 이름에 대입하면 파라미터가 공유됩니다.
    - `SelfAttention.forward(values, keys, query, mask)`의 인자 순서를 확인하세요. 이름이 비슷해도 query에 적용할 변환과 value에 적용할 변환을 바꾸면 안 됩니다.
    - Cross-attention에서는 query가 decoder에서, key와 value가 encoder에서 옵니다. 따라서 query 길이 `T`와 key/value 길이 `S`를 따로 유지합니다.
- **Shape 흐름**
    - **Input:** query `(2, 3, 12)`, key/value 각각 `(2, 5, 12)`
    - **Operation:** 각 입력의 마지막 12차원에 독립적인 선형 변환
    - **Output:** Q `(2, 3, 12)`, K·V 각각 `(2, 5, 12)`

---

<a id="c7"></a>
## **[7) Multi-Head 형태로 Reshape]**  `[C7]`

> 허브: [R05](../Week1/transformer_paper_guide.md#r05)
> 대응: [CS§2](../Week1/A.ing_Transformer_Cheat_sheet.md#cs2) · [N-7] · [N-8] · [N-9]

선형 변환한 Q·K·V의 특징 축을 head 축과 head 내부 특징 축으로 나눕니다.

<a id="c7-1"></a>
### 1. `reshape`  `[C7-1]`

> 대응: [N-7] · [N-8] · [N-9]

- **코드**
    - `tensor.reshape(...)` : 전체 원소 수를 유지하며 shape 변경
- **패턴**
    - `split = projected.reshape(batch_size, length, heads, head_dim)`
- **설명**: 길이 12인 특징 축을 head 3개와 head당 특징 4개로 해석합니다. 토큰 개수를 늘리거나 원소를 새로 계산하는 단계가 아닙니다.
- **코드 사용법**
    - 변환 전후 전체 원소 수가 같아야 합니다. Q에는 query 길이, K와 V에는 각자의 길이를 사용합니다.
    - 이 노트북의 축 순서는 `(N, 길이, h, d_k)`입니다. 다른 구현의 `(N, h, 길이, d_k)`와 혼동하지 마세요.
    - `reshape`는 축의 의미를 맞바꾸는 `transpose`와 다릅니다. 또한 메모리 배치에 따라 복사가 일어날 수 있으므로 항상 view를 반환한다고 가정하지 마세요.
- **Shape 흐름**
    - **Input:** Q `(2, 3, 12)`, K·V 각각 `(2, 5, 12)`
    - **Operation:** 특징 축 `12 = 3 × 4`로 분해
    - **Output:** Q `(2, 3, 3, 4)`, K·V 각각 `(2, 5, 3, 4)`

---

<a id="c8"></a>
## **[8) Query와 Key의 Attention 점수]**  `[C8]`

> 허브: [R03](../Week1/transformer_paper_guide.md#r03)
> 대응: [CS§1](../Week1/A.ing_Transformer_Cheat_sheet.md#cs1) · [N-10]

각 head에서 모든 query–key 쌍의 관련도를 구합니다. 이 단계의 값은 아직 확률이 아닌 점수입니다.

<a id="c8-1"></a>
### 1. `torch.einsum`으로 내적 계산  `[C8-1]`

> 대응: [N-10]

- **코드**
    - `torch.einsum(equation, ...)` : 축 이름으로 곱셈과 합산을 지정
- **패턴**
    - `scores = torch.einsum("nqhd,nkhd->nhqk", queries, keys)`
- **설명**: 같은 배치와 head 안에서 Q와 K의 특징을 곱하고 `d`축을 합산합니다. 결과에는 query 위치와 key 위치가 모두 남으므로 두 문장의 길이가 달라도 계산할 수 있습니다.
- **코드 사용법**
    - `n`은 배치, `q`는 query 길이, `k`는 key 길이, `h`는 head, `d`는 head 차원입니다. 문자의 의미는 입력 텐서의 축 순서와 함께 읽습니다.
    - 출력에서 사라진 `d`가 합산 대상입니다. `q`나 `k`까지 없애면 위치별 관계를 잃습니다.
    - Self-attention에서는 `q`와 `k`의 크기가 같지만 서로 다른 축입니다. Cross-attention에서는 크기가 다를 수 있습니다.
- **Shape 흐름**
    - **Input:** Q `(2, 3, 3, 4)`, K `(2, 5, 3, 4)`
    - **Operation:** 각 query–key 쌍에 대해 head 내부 4개 특징의 내적
    - **Output:** 점수 `(2, 3, 3, 5)` = `(N, h, query_len, key_len)`

---

<a id="c9"></a>
## **[9) Attention 점수에 마스크 적용]**  `[C9]`

> 허브: [R07](../Week1/transformer_paper_guide.md#r07)
> 대응: [CS§4](../Week1/A.ing_Transformer_Cheat_sheet.md#cs4) · [N-11]

참고하면 안 되는 key에 매우 작은 점수를 넣어, 이어지는 softmax에서 그 위치의 가중치가 사실상 0이 되게 합니다.

<a id="c9-1"></a>
### 1. `masked_fill`  `[C9-1]`

> 대응: [N-11]

- **코드**
    - `tensor.masked_fill(condition, value)` : 조건이 True인 위치의 값을 교체
- **패턴**
    - `masked_scores = scores.masked_fill(mask == 0, -1e20)`
- **설명**: 우리 마스크는 허용 위치가 1이므로 `mask == 0`인 곳을 채웁니다. `masked_fill`에 허용 마스크를 그대로 넣으면 오히려 허용 위치를 가리게 됩니다.
- **코드 사용법**
    - 작은 마스크는 broadcasting으로 head·query 축에 적용됩니다. 실제 점수와 마지막 key 축 길이가 맞는지 먼저 확인하세요.
    - 0을 넣는 것만으로는 softmax 가중치를 0으로 만들 수 없습니다. 다른 점수와 비교해 충분히 작은 값이 필요합니다.
    - `-1e20`은 현재 float32 실습에 쓰인 값입니다. 다른 dtype에서는 표현 범위를 확인해야 합니다.
    - 한 query의 모든 key를 가리는 입력은 피하세요. 유한한 동일 값만 남으면 원치 않는 균등 분포가, 모두 `-inf`이면 NaN이 생길 수 있습니다.
- **Shape 흐름**
    - **Input:** cross-attention 점수 `(2, 3, 3, 5)`, source mask `(2, 1, 1, 5)`
    - **Operation:** source mask를 각 head와 query에 공유해 차단 위치를 교체
    - **Output:** 마스킹한 점수 `(2, 3, 3, 5)`; target self-attention에는 `(2, 1, 3, 3)` causal mask 사용

---

<a id="c10"></a>
## **[10) 스케일링과 Softmax]**  `[C10]`

> 허브: [R04](../Week1/transformer_paper_guide.md#r04)
> 대응: [CS§1](../Week1/A.ing_Transformer_Cheat_sheet.md#cs1) · 제공 코드 이해 / 준비 단계

관련도 점수를 key별 가중치로 바꿉니다. 각 query가 어떤 위치의 정보를 얼마나 가져올지를 정하는 단계입니다.

<a id="c10-1"></a>
### 1. 제곱근으로 나누기와 `softmax`  `[C10-1]`

> 대응: 제공 코드 이해 / 준비 단계

- **코드**
    - `torch.softmax(input, dim)` : 지정한 축을 따라 합이 1인 가중치로 변환
- **패턴**
    - `attention = torch.softmax(scores / (head_dim ** 0.5), dim=-1)`
- **설명**: 내적에 참여하는 특징 수가 커지면 점수의 크기도 커질 수 있습니다. `sqrt(d_k)`로 나누어 softmax가 지나치게 한 위치에 몰리는 현상을 완화합니다. 그 뒤 각 query의 key 점수들을 함께 정규화합니다.
- **코드 사용법**
    - 분모는 전체 모델 차원 `E`가 아니라 head 차원 `d_k`의 제곱근입니다.
    - 점수의 마지막 축은 key입니다. `dim=-1`로 설정하면 각 query가 참고할 key들의 가중치 합이 1이 됩니다.
    - 마스크를 적용한 점수를 사용합니다. softmax만 적용한다고 PAD나 미래 위치가 자동으로 제외되지는 않습니다.
    - Softmax는 별도의 학습 파라미터를 갖지 않습니다. 가중치를 결정하는 Q·K 선형 변환은 loss를 통해 학습됩니다.
- **Shape 흐름**
    - **Input:** 마스킹한 점수 `(2, 3, 3, 5)`
    - **Operation:** `sqrt(4)=2`로 나누고 길이 5인 key 축에 softmax
    - **Output:** attention 가중치 `(2, 3, 3, 5)`

---

<a id="c11"></a>
## **[11) Value의 가중합]**  `[C11]`

> 허브: [R03](../Week1/transformer_paper_guide.md#r03)
> 대응: [CS§1](../Week1/A.ing_Transformer_Cheat_sheet.md#cs1) · [N-12]

앞에서 만든 가중치만으로는 단어의 정보가 담긴 출력 벡터가 되지 않습니다. 각 key에 대응하는 value를 그 가중치만큼 모아야 합니다.

<a id="c11-1"></a>
### 1. `einsum`으로 Value 모으기  `[C11-1]`

> 대응: [N-12]

- **코드**
    - `torch.einsum()` : key 위치를 따라 가중치를 곱하고 합산
- **패턴**
    - `head_output = torch.einsum("nhqk,nkhd->nqhd", attention, values)`
- **설명**: query 하나마다 모든 value 벡터의 가중합을 구합니다. 합산되는 축은 key 길이이고, 남는 위치 축은 query 길이입니다. 따라서 source가 길어져도 decoder 출력의 위치 수는 target 길이를 따릅니다.
- **코드 사용법**
    - attention의 마지막 축과 value의 길이 축이 같아야 합니다. key와 value는 같은 위치끼리 대응합니다.
    - `k`는 출력에서 사라지고 `q`는 남습니다. 출력 축 순서 `(N, query_len, h, d_k)`를 다음 reshape와 함께 확인하세요.
    - 가중치 행렬 자체를 반환하거나 key 벡터를 모으는 것은 이 단계의 목적과 다릅니다.
- **Shape 흐름**
    - **Input:** attention `(2, 3, 3, 5)`, V `(2, 5, 3, 4)`
    - **Operation:** 5개 key 위치의 value를 가중합
    - **Output:** head별 출력 `(2, 3, 3, 4)`

---

<a id="c12"></a>
## **[12) Head 결합과 출력 선형 변환]**  `[C12]`

> 허브: [R05](../Week1/transformer_paper_guide.md#r05)
> 대응: [CS§2](../Week1/A.ing_Transformer_Cheat_sheet.md#cs2) · [N-5] · [N-13]

여러 head가 모은 정보를 하나의 모델 표현으로 합쳐 다음 블록에 전달합니다.

<a id="c12-1"></a>
### 1. `reshape`와 `W_O`  `[C12-1]`

> 대응: [N-5] · [N-13]

- **코드**
    - `tensor.reshape()` : head 축과 head 차원을 결합
    - `nn.Linear(E, E)` : 결합한 특징들을 다시 조합
- **패턴**
    - `joined = head_output.reshape(batch_size, query_len, embed_size)`
    - `out = self.W_O(joined)`
- **설명**: Head별 결과를 이어 붙이면 다시 길이 `E`인 벡터가 됩니다. 출력 선형 변환 `W_O`는 여러 head의 특징을 섞어 다음 층에서 사용할 표현을 만듭니다.
- **코드 사용법**
    - `W_O`는 `__init__`에서 만든 학습 가능한 모듈입니다. head를 단순히 합치는 reshape와 역할이 다릅니다.
    - 앞 단계의 축 순서가 `(N, query_len, h, d_k)`일 때 마지막 두 축을 합칩니다. 축 순서가 바뀌었다면 같은 reshape를 그대로 적용할 수 없습니다.
    - 출력 길이는 query 길이입니다. source 길이로 reshape하면 cross-attention에서 원소 수 오류가 나거나 의미가 어긋납니다.
- **Shape 흐름**
    - **Input:** head별 출력 `(2, 3, 3, 4)`
    - **Operation:** head 결합 `(2, 3, 12)` → `Linear(12, 12)`
    - **Output:** attention 출력 `(2, 3, 12)`

---

<a id="c13"></a>
## **[13) Attention 뒤 Residual·LayerNorm·Dropout]**  `[C13]`

> 허브: [R08](../Week1/transformer_paper_guide.md#r08)
> 대응: [CS§5](../Week1/A.ing_Transformer_Cheat_sheet.md#cs5) · [N-14] · [N-21]

Attention으로 얻은 정보에 해당 query의 원래 표현을 더하고, 특징의 크기를 정규화합니다.

<a id="c13-1"></a>
### 1. Residual 덧셈과 `nn.LayerNorm`  `[C13-1]`

> 대응: [N-14] · [N-21]

- **코드**
    - `+` : 입력 표현과 attention 출력을 위치별로 더함
    - `nn.LayerNorm(E)` : 토큰 하나의 마지막 특징 축을 정규화
- **패턴**
    - `residual = attention_output + query`
    - `normalized = self.norm1(residual)`
- **설명**: Residual 연결은 입력 표현이 다음 단계까지 전달될 경로를 만듭니다. LayerNorm은 각 토큰의 `E`개 특징을 기준으로 정규화한 뒤 학습 가능한 크기와 이동 파라미터를 적용합니다.
- **코드 사용법**
    - 더하는 두 텐서는 의도상 같은 `(N, query_len, E)`여야 합니다. 의도하지 않은 broadcasting으로 덧셈이 성공하지 않는지도 확인하세요.
    - Cross-attention에서도 residual의 기준은 query입니다. Encoder의 key나 value를 더하면 문장 길이와 역할이 맞지 않습니다.
    - `nn.LayerNorm(E)`는 배치 전체나 문장 길이 축을 한꺼번에 정규화하지 않습니다. 학습과 평가 모두 현재 입력의 통계를 사용합니다.
    - TransformerBlock에서는 `norm1`, DecoderBlock의 masked self-attention 뒤에서는 `norm`이라는 저장 이름을 사용합니다.
- **Shape 흐름**
    - **Input:** attention 출력과 query 각각 `(2, 3, 12)`
    - **Operation:** Residual 덧셈 → 각 토큰의 마지막 12개 특징 정규화
    - **Output:** 정규화한 표현 `(2, 3, 12)`

<a id="c13-2"></a>
### 2. `nn.Dropout`  `[C13-2]`

> 대응: 제공 코드 이해 / 준비 단계

- **코드**
    - `nn.Dropout(p)` : 학습 중 일부 원소를 확률 p로 0으로 만듦
- **패턴**
    - `dropout = nn.Dropout(p=0.1)`
    - `out = dropout(normalized)`
- **설명**: 일부 특징에만 의존하지 않도록 학습 중 값을 무작위로 가립니다. 살아남은 값은 `1/(1-p)`배로 조정되며, 평가 모드에서는 입력을 그대로 통과시킵니다.
- **코드 사용법**
    - 현재 노트북의 순서는 `덧셈 → LayerNorm → Dropout`입니다. 원논문의 sublayer dropout은 residual 덧셈 전에 적용되므로 두 설정을 구별하세요.
    - `model.train()`과 `model.eval()`이 dropout의 동작을 바꿉니다. 마스크의 인과성 등을 비교할 때는 평가 모드로 무작위성을 제거합니다.
    - `torch.no_grad()`는 gradient 기록을 끄는 기능입니다. 이것만으로 dropout이 평가 모드가 되지는 않습니다.
- **Shape 흐름**
    - **Input:** 정규화한 표현 `(2, 3, 12)`
    - **Operation:** 학습 모드에서 원소 일부를 가림; 평가 모드에서는 그대로 전달
    - **Output:** 출력 `(2, 3, 12)`

---

<a id="c14"></a>
## **[14) Position-wise FFN과 두 번째 Add & Norm]**  `[C14]`

> 허브: [R08](../Week1/transformer_paper_guide.md#r08)
> 대응: [CS§5](../Week1/A.ing_Transformer_Cheat_sheet.md#cs5) · [N-15]

Attention이 위치 사이의 정보를 모았다면, FFN은 각 위치 안에서 특징을 비선형으로 변환합니다.

<a id="c14-1"></a>
### 1. `nn.Sequential`, `nn.Linear`, `nn.ReLU`  `[C14-1]`

> 대응: 제공 코드 이해 / 준비 단계

- **코드**
    - `nn.Sequential()` : 모듈들을 순서대로 실행
    - `nn.Linear()` : 특징 차원을 확장하거나 축소
    - `nn.ReLU()` : 음수는 0으로, 양수는 그대로 전달
- **패턴**
    - `ffn = nn.Sequential(nn.Linear(12, 48), nn.ReLU(), nn.Linear(48, 12))`
    - `forward = ffn(x)`
- **설명**: 첫 선형 층으로 특징을 넓히고, ReLU로 비선형 변환을 거친 뒤, 두 번째 선형 층으로 모델 차원에 돌아옵니다. 같은 FFN을 모든 위치에 적용하지만 서로 다른 위치의 벡터를 직접 섞지는 않습니다.
- **코드 사용법**
    - 중간 차원은 `forward_expansion * E`입니다. 이 예시는 확장 비율 4를 사용합니다.
    - 두 선형 층 사이의 ReLU가 빠지면 두 선형 변환을 하나의 affine 변환으로 합칠 수 있어 비선형 표현력이 사라집니다.
    - 노트북은 중간 결과를 관찰하려고 `self.feed_forward[0]`, `[1]`, `[2]`를 각각 호출하기도 합니다. 순서대로 결과를 이어야 합니다.
- **Shape 흐름**
    - **Input:** 블록의 중간 표현 `(2, 3, 12)`
    - **Operation:** `Linear`: `(2, 3, 48)` → ReLU → `Linear`
    - **Output:** FFN 출력 `(2, 3, 12)`

<a id="c14-2"></a>
### 2. 두 번째 Residual과 정규화  `[C14-2]`

> 대응: [N-15]

- **코드**
    - `+`, `nn.LayerNorm()`, `nn.Dropout()` : FFN 입력을 더하고 정규화·dropout 적용
- **패턴**
    - `residual = forward + x`
    - `out = self.dropout(self.norm2(residual))`
- **설명**: FFN의 결과에 FFN으로 들어간 표현을 더합니다. Attention 뒤에 쓴 정규화 층과 FFN 뒤에 쓸 정규화 층은 별도 파라미터를 갖습니다.
- **코드 사용법**
    - 여기서 더할 입력은 FFN 직전의 `x`입니다. 블록 맨 처음의 query와 구별하세요.
    - `norm1`을 재사용하지 않고 `norm2`를 사용합니다. Dropout 위치는 [C13](#c13)의 실습 설정을 따릅니다.
- **Shape 흐름**
    - **Input:** FFN 입력과 출력 각각 `(2, 3, 12)`
    - **Operation:** 덧셈 → `norm2` → dropout
    - **Output:** 블록 출력 `(2, 3, 12)`

---

<a id="c15"></a>
## **[15) Encoder 블록 반복]**  `[C15]`

> 허브: [R06](../Week1/transformer_paper_guide.md#r06)
> 대응: [CS§3](../Week1/A.ing_Transformer_Cheat_sheet.md#cs3) · [N-19]

Encoder는 같은 구조의 블록을 여러 층 쌓습니다. 각 층은 직전 층의 출력을 받아 source 표현을 갱신합니다.

<a id="c15-1"></a>
### 1. `nn.ModuleList`와 반복 호출  `[C15-1]`

> 대응: [N-19]

- **코드**
    - `nn.ModuleList()` : 하위 모듈들을 등록해 보관
    - `for` : 등록한 블록을 직접 순서대로 실행
- **패턴**
    - `self.layers = nn.ModuleList([make_block() for _ in range(num_layers)])`
    - `out = layer(out, out, out, src_padding_mask)`
- **설명**: Encoder self-attention은 query·key·value가 모두 현재 source 표현에서 나옵니다. 블록을 지날 때마다 값은 달라지지만 문장 길이와 모델 차원은 유지됩니다.
- **코드 사용법**
    - 위 패턴의 `make_block()`은 매번 새 블록을 만든다는 뜻의 예시 이름입니다. 실제 노트북에서는 `TransformerBlock(...)`을 생성합니다.
    - `[block] * num_layers`는 같은 인스턴스를 반복 참조합니다. 독립적인 층을 만들려면 반복할 때마다 새 인스턴스를 생성해야 합니다.
    - `ModuleList`는 일반 Python 리스트와 달리 내부 모듈을 등록해 `model.parameters()`나 `model.to(device)`에 포함시킵니다. 실행은 별도 반복문이 필요합니다.
    - 각 반복에서 `out`을 갱신합니다. 처음 임베딩을 모든 층에 다시 넣으면 층을 쌓은 계산이 되지 않습니다.
- **Shape 흐름**
    - **Input:** 임베딩과 위치 정보를 합친 source `(2, 5, 12)`
    - **Operation:** 각 Encoder 블록에 현재 `out`을 Q·K·V의 입력으로 전달
    - **Output:** 최종 encoder 출력 `(2, 5, 12)`

---

<a id="c16"></a>
## **[16) Decoder의 Masked Self-Attention]**  `[C16]`

> 허브: [R06](../Week1/transformer_paper_guide.md#r06)
> 대응: [CS§3](../Week1/A.ing_Transformer_Cheat_sheet.md#cs3) · [N-20]

Decoder는 먼저 지금까지 주어진 target 토큰끼리 정보를 모읍니다. 미래 target 위치는 causal mask로 차단합니다.

<a id="c16-1"></a>
### 1. 직접 구현한 `SelfAttention` 호출  `[C16-1]`

> 대응: [N-20]

- **코드**
    - `SelfAttention` : 노트북의 attention 클래스
- **패턴**
    - `attention = self.attention(x, x, x, trg_mask)`
- **설명**: 이 클래스의 호출 순서는 value, key, query, mask입니다. Masked self-attention에서는 세 입력이 모두 현재 target 표현이므로 같은 `x`를 전달합니다.
- **코드 사용법**
    - 클래스 이름이 `SelfAttention`이어도 내부 계산은 전달한 입력을 사용합니다. Cross-attention에도 사용되는 공통 attention 구현입니다.
    - target 길이에 맞춘 causal mask를 넣습니다. source padding mask를 넣으면 미래 target을 가릴 수 없습니다.
    - 출력은 [C13](#c13)의 residual·정규화·dropout을 거쳐 다음 cross-attention의 query가 됩니다.
    - 학습 시 target 입력을 오른쪽으로 한 칸 밀어 준비하므로 대각선의 현재 입력 토큰을 보는 것은 정답 누출이 아닙니다.
- **Shape 흐름**
    - **Input:** target 표현 `(2, 3, 12)`, causal mask `(2, 1, 3, 3)`
    - **Operation:** 미래 위치를 제외하고 target 내부 attention 계산
    - **Output:** attention 출력 `(2, 3, 12)`

---

<a id="c17"></a>
## **[17) Decoder의 Cross-Attention과 FFN]**  `[C17]`

> 허브: [R06](../Week1/transformer_paper_guide.md#r06)
> 대응: [CS§3](../Week1/A.ing_Transformer_Cheat_sheet.md#cs3) · [N-22]

Decoder의 현재 표현이 Encoder의 source 표현을 참고합니다. 두 입력의 길이가 달라도 동작해야 합니다.

<a id="c17-1"></a>
### 1. 직접 구현한 `TransformerBlock` 호출  `[C17-1]`

> 대응: [N-22]

- **코드**
    - `TransformerBlock` : attention과 FFN, 두 residual·정규화를 포함한 클래스
- **패턴**
    - `out = self.transformer_block(value, key, query, src_mask)`
- **설명**: query는 masked self-attention 뒤의 decoder 표현이고, key와 value는 최종 encoder 출력입니다. 블록 안에서 source 정보를 모은 뒤 FFN까지 거쳐 DecoderBlock의 출력을 만듭니다.
- **코드 사용법**
    - 호출 순서는 value, key, query, mask입니다. Decoder에서 온 query와 Encoder에서 온 key/value의 자리를 구분하세요.
    - 마지막 점수 축은 source key이므로 source padding mask가 필요합니다. Target causal mask는 앞의 self-attention에서 사용합니다.
    - 이 호출에는 FFN과 Add & Norm까지 포함되어 있습니다. Cross-attention 점수만 반환하는 함수로 생각하면 뒤에 중복 계산을 붙이게 됩니다.
    - 이 블록의 출력 길이와 residual 입력 길이는 모두 query의 길이 `T`입니다.
- **Shape 흐름**
    - **Input:** query `(2, 3, 12)`, encoder key/value 각각 `(2, 5, 12)`
    - **Operation:** cross-attention 점수 `(2, 3, 3, 5)` → source 정보의 가중합 → residual·FFN
    - **Output:** DecoderBlock 출력 `(2, 3, 12)`

---

<a id="c18"></a>
## **[18) Decoder 스택과 어휘별 Logit]**  `[C18]`

> 허브: [R02](../Week1/transformer_paper_guide.md#r02) · [R06](../Week1/transformer_paper_guide.md#r06) · [R09](../Week1/transformer_paper_guide.md#r09)
> 대응: [CS§3](../Week1/A.ing_Transformer_Cheat_sheet.md#cs3) · [CS§7](../Week1/A.ing_Transformer_Cheat_sheet.md#cs7) · [N-26] · [N-27]

Decoder 블록을 모두 지난 뒤, 각 위치의 표현을 다음 토큰 후보들의 점수로 바꿉니다.

<a id="c18-1"></a>
### 1. `DecoderBlock` 반복  `[C18-1]`

> 대응: [N-26]

- **코드**
    - `DecoderBlock` : masked self-attention, cross-attention, FFN을 포함한 클래스
    - `nn.ModuleList()` : Decoder 블록들을 등록해 보관
- **패턴**
    - `x = layer(x, enc_out, enc_out, src_padding_mask, trg_causal_mask)`
- **설명**: 각 블록은 직전 decoder 출력을 받아 갱신합니다. 모든 decoder 층은 동일한 최종 encoder 출력을 참고하지만, 각 층의 attention 파라미터는 별도로 학습됩니다.
- **코드 사용법**
    - 노트북의 `DecoderBlock.forward` 인자 순서는 `x, value, key, src_mask, trg_mask`입니다. [C17](#c17)의 내부 TransformerBlock 호출과 구별하세요.
    - 반복에서 갱신할 값은 `x`입니다. `enc_out`을 decoder 출력으로 덮어쓰면 다음 층이 잘못된 source를 참고합니다.
- **Shape 흐름**
    - **Input:** decoder 표현 `(2, 3, 12)`, encoder 출력 `(2, 5, 12)`
    - **Operation:** 여러 DecoderBlock을 순서대로 통과
    - **Output:** 최종 decoder 표현 `(2, 3, 12)`

<a id="c18-2"></a>
### 2. 어휘 차원으로 `nn.Linear` 적용  `[C18-2]`

> 대응: [N-27]

- **코드**
    - `nn.Linear(E, trg_vocab_size)` : 각 위치에서 어휘별 점수 생성
- **패턴**
    - `logits = self.fc_out(x)`
- **설명**: 길이 `E`의 특징 벡터를 어휘 수만큼의 점수로 바꿉니다. 이 값은 아직 확률이 아닌 logit이며, 각 위치마다 다음 토큰 후보를 비교하는 데 쓰입니다.
- **코드 사용법**
    - `trg_vocab_size`는 target 어휘 크기입니다. source 어휘 크기나 최대 문장 길이와 혼동하지 마세요.
    - `CrossEntropyLoss`에 전달할 때는 softmax를 먼저 적용하지 않습니다. Loss 함수가 raw logits에서 필요한 정규화를 처리합니다.
    - 확률을 보고 싶을 때는 어휘 축에 softmax를 적용합니다. 학습 loss 입력과 관찰용 확률을 구별하세요.
- **Shape 흐름**
    - **Input:** 최종 decoder 표현 `(2, 3, 12)`
    - **Operation:** `Linear(12, Vocab)`으로 마지막 축 변환
    - **Output:** logits `(2, 3, Vocab)`

---

<a id="c19"></a>
## **[19) Transformer 전체 실행 연결]**  `[C19]`

> 허브: [R02](../Week1/transformer_paper_guide.md#r02)
> 대응: [CS§0](../Week1/A.ing_Transformer_Cheat_sheet.md#cs0) · [N-33] · [N-34] · [N-35] · [N-36]

Source와 decoder 입력 토큰을 받아 두 종류의 마스크를 만들고, Encoder의 결과를 Decoder에 전달합니다.

<a id="c19-1"></a>
### 1. 마스크·Encoder·Decoder 연결  `[C19-1]`

> 대응: [N-33] · [N-34] · [N-35] · [N-36]

- **코드**
    - `make_src_mask()`, `make_trg_mask()` : 노트북의 마스크 생성 메서드
    - `Encoder`, `Decoder` : 노트북에서 정의한 모델 구성 클래스
- **패턴**
    - `src_mask = self.make_src_mask(src_token_ids)`
    - `trg_mask = self.make_trg_mask(trg_token_ids)`
    - `enc_src = self.encoder(src_token_ids, src_mask)`
    - `out = self.decoder(trg_token_ids, enc_src, src_mask, trg_mask)`
- **설명**: Encoder는 source를 한 번 표현하고 Decoder는 그 표현과 현재 target 입력을 함께 사용합니다. 두 마스크의 역할을 끝까지 유지해 source의 PAD와 target의 미래 위치를 각각 가립니다.
- **코드 사용법**
    - 이 호출에서 `trg_token_ids`는 decoder에 넣을 입력입니다. 학습용 전체 target이 따로 있다면 호출 전에 `trg[:, :-1]`을 입력, `trg[:, 1:]`을 정답으로 나눕니다.
    - 예를 들어 `[BOS, A, B, EOS]`에서 입력은 `[BOS, A, B]`, 정답은 `[A, B, EOS]`입니다. 모델의 각 출력 위치는 바로 다음 토큰을 예측합니다.
    - PAD 정답은 loss 계산에서 제외합니다. Source PAD mask만으로 target loss의 PAD가 무시되지는 않습니다.
    - 모델, 토큰 ID, 위치 ID, 마스크가 같은 device에 있어야 합니다. `forward`의 반환값은 logits이며 loss 계산과 파라미터 갱신은 학습 루프에서 수행합니다.
- **Shape 흐름**
    - **Input:** source ID `(2, 5)`, decoder 입력 ID `(2, 3)`
    - **Operation:** source mask `(2, 1, 1, 5)` · target mask `(2, 1, 3, 3)` → encoder 출력 `(2, 5, 12)` → decoder
    - **Output:** 최종 logits `(2, 3, Vocab)`

---

<a id="debug"></a>
## **[부록) 에러 메시지별 디버깅 표]**

> 허브: [R05](../Week1/transformer_paper_guide.md#r05) · [R07](../Week1/transformer_paper_guide.md#r07) · [R11](../Week1/transformer_paper_guide.md#r11)

에러 메시지의 문구는 실행 환경에 따라 조금씩 다를 수 있습니다. 메시지에 등장하는 축의 크기를 확인하고, 아래 절에서 해당 연산의 입력과 출력을 다시 맞춰 보세요. 에러 없이 결과만 잘못되는 경우도 함께 정리했습니다.

| 에러 메시지 또는 관찰 | 원인·확인할 내용 | 돌아갈 절 |
| --- | --- | --- |
| `AttributeError: ... has no attribute ...` | `__init__`에서 저장한 모듈 이름과 호출 이름이 다름 | [C0](#c0) |
| head 분해 조건의 `AssertionError` | `E`가 head 수 `h`로 나누어떨어지지 않음 | [C2](#c2) |
| `shape ... is invalid for input of size ...` | reshape 전후 원소 수 불일치; query 길이와 key 길이 혼동 | [C7](#c7), [C12](#c12) |
| `einsum(): subscript ... has size ...` | einsum 문자와 실제 축 순서 불일치; key/value 길이 불일치 | [C8](#c8), [C11](#c11) |
| `The size of tensor a ... must match ...` | mask의 key 축 길이 또는 residual의 query 길이 불일치 | [C3](#c3), [C9](#c9), [C13](#c13) |
| `Expected all tensors to be on the same device` | 새로 만든 위치 ID나 마스크가 모델과 다른 장치에 있음 | [C3](#c3), [C5](#c5), [C19](#c19) |
| `IndexError: index out of range in self` | 토큰 ID가 어휘 범위를 벗어나거나 위치 ID가 최대 길이를 넘음 | [C4](#c4), [C5](#c5) |
| Cross-attention 출력 길이가 source 길이임 | query와 key/value를 바꾸어 넣었거나 출력 reshape에 source 길이를 사용함 | [C11](#c11), [C12](#c12), [C17](#c17) |
| 미래 target을 바꾸자 이전 위치 logits도 바뀜 | 평가 모드에서 재확인; causal mask 방향과 전달 경로 확인 | [C3](#c3), [C16](#c16), [C19](#c19) |
| Source 뒤에 PAD를 덧붙이자 logits가 바뀜 | 평가 모드에서 재확인; Encoder와 cross-attention 모두에 source mask가 전달되는지 확인 | [C3](#c3), [C15](#c15), [C17](#c17) |
| loss나 attention에 `NaN`이 나타남 | 모든 key가 차단된 행, 과도한 점수, dtype 범위 등을 확인 | [C9](#c9), [C10](#c10) |
| 실행되지만 loss가 줄지 않음 | target 입력·정답의 한 칸 이동, PAD loss 제외, raw logits, 모듈 등록 및 학습 루프 확인 | [C0](#c0), [C15](#c15), [C18](#c18), [C19](#c19) |
| 빈칸 기호에 대한 `NameError` | 아직 채우지 않은 빈칸이 실행됨; 인접한 `[N-k]` 번호 확인 | 각 절의 `대응:` 및 [빈칸 노트북](A.ing_Transformer_from_scratch_blank.ipynb) |

> **읽는 법**: 오류가 처음 드러난 줄만 고치기보다, 그 줄로 들어오는 텐서의 축을 먼저 적어 보세요. 마스크 비교나 출력 비교는 `model.eval()`에서 수행하고, 부동소수점 계산의 작은 오차를 허용해 판단합니다. Shape가 맞는다고 마스크 방향이나 입력 역할까지 맞는 것은 아닙니다.
