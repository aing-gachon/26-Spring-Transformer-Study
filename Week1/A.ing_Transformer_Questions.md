# Transformer (Vaswani et al., 2017) 질문 정리 (Questions Only)

각 문항의 `> 허브:` 표기는 [논문 가이드](transformer_paper_guide.md)의 R 항목을 가리킵니다. 답은 [퀴즈_모범답안](transformer_questions_sample_answer.md).

각 문항 머리에 `> 근거:`로 **개념은 [치트시트](A.ing_Transformer_Cheat_sheet.md) `[CS§n]`, 구현은 [쿡북](../Week2/A.ing_Transformer_Cookbook.md) `[Cn]`, 코드는 노트북 `[N-k]`** 좌표를 함께 답니다. 막히면 그 좌표부터 다시 읽으시면 됩니다.

[source: Week1/A.ing_Transformer_Questions.md]

> *Attention Is All You Need* 기반 문제 정리\
> (모범답안 제외 버전)

**난이도 표기** — 소문항마다 붙어 있습니다.

| 태그 | 뜻 | 필요한 것 |
| --- | --- | --- |
| `[기본]` | 논문을 읽었으면 답할 수 있습니다 | 해당 절·그림 |
| `[응용]` | 논문 + 코드 연결이 필요합니다 | 허브 R + 쿡북/노트북 좌표 |
| `[심화]` | 논문에 직접 안 적힌 추론 | 논증을 스스로 구성 |

`[심화]`는 못 풀어도 진도에 지장 없습니다. 먼저 `[기본]`을 전부 채우고 넘어갈 것.

---

<a id="q1"></a>
## 1) Transformer가 Multi-Head Attention을 사용하는 이유는 무엇인가?  `[Q1]`

> 허브: [R05](transformer_paper_guide.md#r05)
> 근거: [CS§2](A.ing_Transformer_Cheat_sheet.md#cs2) · [C2](../Week2/A.ing_Transformer_Cookbook.md#c2) · [C6](../Week2/A.ing_Transformer_Cookbook.md#c6) · [C7](../Week2/A.ing_Transformer_Cookbook.md#c7) · [C12](../Week2/A.ing_Transformer_Cookbook.md#c12) · N-1–N-13

논문 Section 3.2.2에서 Multi-Head Attention을 다음과 같이 정의한다.

$$MultiHead(Q, K, V) = Concat(head_1,\dots,head_h)W^O$$

각 head는 $Attention(QW_i^Q, KW_i^K, VW_i^V)$ 형태로 **서로 다른 선형변환(=서로 다른 관점)** 을 가진다.

- (1) `[기본]` 단일 Attention과 Multi-Head Attention의 차이를 설명하시오.
- (2) `[응용]` 여러 head의 서로 다른 가중합을 concat하는 이유를 설명하고, C7/C12에서 어떤 축을 나누고 합치는지 적으시오.
- (3) `[심화]` Transformer는 각 head의 결과를 이어 붙인 뒤(concat), 출력 선형변환을 적용합니다. 이를 바꾸어 모든 head의 결과를 단순히 평균 낸다고 가정하겠습니다. 두 방법은 서로 다른 head가 찾아낸 정보를 보존하고 활용하는 방식에서 어떤 차이가 있습니까? Concat 뒤의 학습 가능한 선형변환이 단순 평균보다 다양한 결합을 표현할 수 있는 이유를 설명하시오.

---

<a id="q2"></a>
## 2) 왜 Transformer는 Scaled Dot-Product Attention에서 $QK^\top$를 그대로 softmax에 넣지 않고 $\sqrt{d_K}$로 나눈 뒤 softmax를 적용하는가?  `[Q2]`

> 허브: [R04](transformer_paper_guide.md#r04)
> 근거: [CS§1](A.ing_Transformer_Cheat_sheet.md#cs1) · [C8](../Week2/A.ing_Transformer_Cookbook.md#c8) · [C10](../Week2/A.ing_Transformer_Cookbook.md#c10) · N-10–N-12

논문 Section 3.2.1은 $d_k$가 커질수록 dot-product 값이 커져 softmax가 **saturation(포화)** 될 수 있다고 설명한다.

(1) `[기본]` $QK^\top$의 분산 관점에서 scaling이 필요한 이유를 설명하시오.

(2) `[응용]` scaling을 하지 않을 경우 softmax의 saturation과 gradient에 어떤 문제가 발생하며, 이것이 학습 안정성과 어떤 관계가 있는지 설명하시오.

---

<a id="q3"></a>
## 3) 왜 Transformer는 RNN과 CNN 대비 장기의존성(long-range dependency)에 유리하다고 주장하는가?  `[Q3]`

> 허브: [R01](transformer_paper_guide.md#r01) · [R11](transformer_paper_guide.md#r11)
> 근거: [CS§0](A.ing_Transformer_Cheat_sheet.md#cs0) · 논문 Table 1의 세 비교 축 · E01/E02 및 Table 1

논문 Section 4와 Table 1은 self-attention, RNN(recurrent), CNN(convolution)의 **복잡도**와 **maximum path length**를 비교한다.

(1) `[기본]` Maximum Path Length의 의미를 설명하시오.

(2) `[응용]` Table 1의 Maximum Path Length 비교를 근거로, Self-attention이 long-range dependency 학습에 왜 유리한지 설명하시오.

---

<a id="q4"></a>
## 4) Attention layer만 여러 층 쌓는 대신, FFN을 함께 사용하는 이유는 무엇인가?  `[Q4]`

> 허브: [R08](transformer_paper_guide.md#r08) · [R03](transformer_paper_guide.md#r03)
> 근거: [CS§5](A.ing_Transformer_Cheat_sheet.md#cs5) · [C13](../Week2/A.ing_Transformer_Cookbook.md#c13) · [C14](../Week2/A.ing_Transformer_Cookbook.md#c14) · N-14–N-15

Transformer는 각 layer에서 Multi-Head Attention 뒤에 position-wise Feed-Forward Network(FFN)을 둔다.

$$FFN(x) = max(0, xW_1 + b_1)W_2 + b_2$$

(1) `[기본]` Transformer에서 Attention 뒤에 FFN을 두는 이유를 position-wise 비선형성 관점(각 위치마다 독립적으로 적용되는 비선형 변환)에서 설명하시오.

(2) `[응용]` Attention sub-layer만 여러 층 쌓는 구조와 비교하여, FFN이 모델의 표현력을 어떻게 확장하는지 설명하시오.

(3) `[심화]` FFN의 두 선형변환 사이에서 ReLU를 제거하면 다음과 같이 됩니다.

$$FFN(x) = (xW_1 + b_1)W_2 + b_2$$

이 식을 하나의 선형변환과 편향으로 정리하시오. 중간 차원을 크게 만드는 것만으로 비선형 표현을 얻을 수 있습니까? 그렇다면 FFN에서 ReLU를 제거한 Transformer 전체도 선형 모델이라고 결론 내려도 됩니까? Attention과 LayerNorm을 함께 고려하여 설명하시오.

---

<a id="q5"></a>
## 5) Decoder의 self-attention에는 look-ahead mask가 필요한 이유는 무엇인가?  `[Q5]`

> 허브: [R02](transformer_paper_guide.md#r02) · [R07](transformer_paper_guide.md#r07) · [R08](transformer_paper_guide.md#r08)
> 근거: [CS§4](A.ing_Transformer_Cheat_sheet.md#cs4) · [C3](../Week2/A.ing_Transformer_Cookbook.md#c3) · [C16](../Week2/A.ing_Transformer_Cookbook.md#c16) · [C19](../Week2/A.ing_Transformer_Cookbook.md#c19) · N-20/N-28–N-36

논문의 Section 3.2.3에서는 decoder의 self-attention에서 미래 위치를 참조하지 못하도록 masking을 적용한다고 명시한다.

(1) `[기본]` auto-regressive 조건이 무엇인지 설명하시오.

(2) `[응용]` look-ahead mask가 없으면 auto-regressive 조건이 어떻게 위배되는지 설명하시오.

(3) `[심화]` 한 학생이 decoder 입력을 한 칸 이동하지 않고, 입력과 정답에 똑같이 `[I, eat, apples, EOS]`를 사용했습니다. 대신 self-attention에서 미래 위치뿐 아니라 현재 위치까지 가려, 앞선 위치만 참고하도록 만들었습니다.

이 학생은 “현재 정답을 attention에서 참고할 수 없으므로 정답 유출을 막았다”고 주장합니다. 이 주장이 맞는지 판단하시오. Fig.1에서 입력 embedding이 residual 연결을 통해 전달되는 경로를 근거로 설명하시오.

단, 첫 위치에서 참고할 토큰이 없는 문제는 별도로 처리했다고 가정합니다.

---

## 참고 문헌

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin.\
  *Attention Is All You Need.* NIPS 2017.
