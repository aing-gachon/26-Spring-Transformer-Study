# Transformer (Vaswani et al., 2017) 핵심 Q&A 정리

문항은 [퀴즈](A.ing_Transformer_Questions.md). 각 절의 `> 허브:` 표기는 [논문 가이드](transformer_paper_guide.md)의 R 항목을 가리킨다.

`> 근거:` 줄은 [퀴즈](A.ing_Transformer_Questions.md)의 같은 문항과 동일한 좌표다 — 개념은 [치트시트](A.ing_Transformer_Cheat_sheet.md) `[CS§n]`, 구현은 [쿡북](../Week2/A.ing_Transformer_Cookbook.md) `[Cn]`, 코드는 노트북 `[N-k]`.

[source: Week1/transformer_questions_sample_answer.md]


<a id="a1"></a>
## 1) Transformer가 Multi-Head Attention을 사용하는 이유는 무엇인가?  `[A1]`

> 허브: [R05](transformer_paper_guide.md#r05)
> 근거: [CS§2](A.ing_Transformer_Cheat_sheet.md#cs2) · [C2](../Week2/A.ing_Transformer_Cookbook.md#c2) · [C6](../Week2/A.ing_Transformer_Cookbook.md#c6) · [C7](../Week2/A.ing_Transformer_Cookbook.md#c7) · [C12](../Week2/A.ing_Transformer_Cookbook.md#c12) · N-1–N-13

### (1) 단일 Attention과 Multi-Head Attention의 차이

> 허브: [R05](transformer_paper_guide.md#r05)

- **단일 head:** 하나의 Q·K·V projection으로 attention 비율표를 만들고, 그 비율로 V를 가중합한다. 각 query가 참고할 위치의 분포는 한 세트다.
- **Multi-head:** head마다 서로 다른 학습 가능한 projection을 사용한다. 각 head가 attention을 계산한 뒤 결과를 이어 붙이고, 출력 projection $W^O$로 결합한다.

$$head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)$$

$$MultiHead(Q,K,V) = Concat(head_1,\dots,head_h)W^O$$

**서로 다른 표현 부분공간**은 같은 입력을 서로 다른 가중치 행렬로 변환해 얻는 표현을 말한다. 각 head는 같은 토큰에서도 서로 다른 특징과 위치 관계를 활용할 수 있다. 문법·의미 등의 역할을 사람이 미리 지정하는 것은 아니며, 모든 head가 반드시 서로 다른 역할을 학습한다고 보장하지도 않는다.

논문 base는 $d_{model}=512$, $h=8$, $d_k=d_v=64$를 사용한다. Head마다 전체 512차원을 그대로 사용하는 것이 아니라 차원을 나누므로, §3.2.2는 전체 차원을 사용하는 단일 head와 계산 비용이 비슷하다고 설명한다.

### (2) Concat의 역할과 C7/C12에서 나누고 합치는 축

> 허브: [R05](transformer_paper_guide.md#r05)

각 head가 만든 가중합을 concat하면 **head별 결과를 구분한 채** 출력 projection에 전달할 수 있다. $W^O$는 여러 head의 특징을 어떻게 조합할지 학습한다. 이는 §3.2.2에서 설명하는 여러 위치·표현 부분공간의 정보를 함께 활용하는 방식이다.

실습에서 $N$은 배치 크기, $L$은 해당 입력의 길이, $E=d_{model}$, $h$는 head 수다. 실습은 $d_k=d_v=E/h$로 둔다.

| 코드 | 입력 shape → 출력 shape | 바뀌는 축 |
| --- | --- | --- |
| C7 / N-7–N-9 | `(N, L, E)` → `(N, L, h, d_k)` | 마지막 표현 축 E를 head 축 h와 head 내부 차원으로 분리 |
| C12 / N-13 | `(N, query_len, h, d_v)` → `(N, query_len, h*d_v)` | head 축과 head 내부 차원을 합침 |
| C12의 출력 Linear | `(N, query_len, h*d_v)` → `(N, query_len, E)` | 이어 붙인 특징을 학습 가능한 가중치로 결합 |

C7의 L은 Q에서는 query 길이, K·V에서는 key/value 길이다. Cross-attention에서는 이 길이가 서로 다를 수 있다. **나누고 합치는 것은 토큰 길이 축이 아니라 표현 차원 축**이다. Reshape 자체에는 학습 파라미터가 없다.

Table 3(A)에서 head 1개의 BLEU는 24.9, base의 head 8개는 25.8이다. 다만 head 32개는 25.4이므로, 이 결과를 “head가 많을수록 항상 좋다”로 일반화할 수는 없다.

### (3) 심화: Concat 뒤 선형변환과 단순 평균의 차이

> 허브: [R05](transformer_paper_guide.md#r05)

**단순 평균은 head별 결과를 같은 비중으로 먼저 섞고, concat은 구분해서 전달한 뒤 결합 방법을 학습한다.** 아래는 §3.2.2의 식에서 도출한 비교이며, 논문이 두 방식을 직접 비교한 실험 결과는 아니다.

한 토큰 위치에서 각 head의 출력을 행벡터 $u_i\in\mathbb{R}^{d_v}$라고 하자. $W^O$를 head에 대응하는 행 블록 $W_i^O$로 나누면 다음과 같다.

$$Concat(u_1,\dots,u_h)W^O = \sum_{i=1}^{h}u_iW_i^O$$

각 $W_i^O$가 다르므로 head별로 서로 다른 특징을 선택하고 변환할 수 있다. 반면 평균은 다음과 같다.

$$\bar{u}=\frac{1}{h}\sum_{i=1}^{h}u_i$$

평균 뒤에 출력 차원을 맞추는 공통 선형변환 $W$를 추가하더라도 결과는 $\sum_i u_i(W/h)$다. 모든 head에 같은 변환이 적용되는 형태로 제한된다. Concat 방식에서 모든 $W_i^O=W/h$로 두면 이 평균 방식을 표현할 수 있지만, 그 반대로 모든 head별 변환을 표현할 수는 없다.

예를 들어 두 head가 스칼라를 출력할 때 `(1, −1)`과 `(0, 0)`의 평균은 모두 0이다. 평균만 받은 후속 층은 두 경우를 구별할 수 없다. Concat 뒤 가중치를 각각 1과 −1로 두면 출력이 2와 0이 되어 구별할 수 있다.

이 결론은 **같은 head 출력들을 어떤 방식으로 결합하는가**에 대한 것이다. 평균 방식에서도 앞쪽 projection은 학습할 수 있으므로, 이 비교만으로 재학습한 모델의 번역 점수까지 단정하지 않는다.

---

<a id="a2"></a>
## 2) 왜 Transformer는 Scaled Dot-Product Attention에서 $QK^\top$를 그대로 softmax에 넣지 않고 $\sqrt{d_K}$로 나눈 뒤 softmax를 적용하는가?  `[A2]`

> 허브: [R04](transformer_paper_guide.md#r04)
> 근거: [CS§1](A.ing_Transformer_Cheat_sheet.md#cs1) · [C8](../Week2/A.ing_Transformer_Cookbook.md#c8) · [C10](../Week2/A.ing_Transformer_Cookbook.md#c10) · N-10–N-12

### (1) 내적의 분산과 scaling이 필요한 이유

> 허브: [R04](transformer_paper_guide.md#r04)

논문 §3.2.1의 PDF 각주 4는 Q·K의 성분들이 서로 독립이고 평균 0, 분산 1이라고 가정한다. 이 가정 아래 내적은 다음과 같다.

$$q\cdot k=\sum_{i=1}^{d_k}q_i k_i$$

각 곱 $q_i k_i$의 평균은 0, 분산은 1이며 서로 다른 항들의 공분산은 0이다. 따라서:

$$\mathbb{E}[q\cdot k]=0,\qquad Var(q\cdot k)=d_k$$

$d_k$가 커질수록 내적의 전형적인 크기인 표준편차가 $\sqrt{d_k}$에 비례해 커진다. 이를 $\sqrt{d_k}$로 나누면:

$$Var\left(\frac{q\cdot k}{\sqrt{d_k}}\right)=\frac{d_k}{d_k}=1$$

이 계산은 **차원이 커질 때 점수의 크기가 함께 커지는 효과를 보정**한다는 근거다. 실제 학습된 Q·K가 항상 이 가정을 만족하거나, scaling 뒤 분산이 반드시 1이 된다는 뜻은 아니다.

### (2) Softmax 포화·기울기·학습 안정성의 관계

> 허브: [R04](transformer_paper_guide.md#r04)

Softmax는 입력 점수들의 **차이**가 커지면 한 위치에 거의 모든 비율을 배정할 수 있다. 모든 점수에 같은 상수를 더하는 것만으로는 분포가 달라지지 않는다.

출력을 $p_i$, 입력 점수를 $z_j$라고 하면 softmax의 미분은 다음과 같다. 여기서 $\delta_{ij}$는 $i=j$일 때 1, 나머지는 0이다.

$$\frac{\partial p_i}{\partial z_j}=p_i(\delta_{ij}-p_j)$$

- 한 $p_i$가 거의 1이고 나머지가 거의 0이면 $p_i(1-p_i)$와 $p_i p_j$가 작아진다.
- Attention 비율을 거쳐 Q·K projection으로 전달되는 기울기가 약해질 수 있다.
- Scaling은 점수 차이가 지나치게 커지는 것을 완화하여, 어느 위치를 참고할지 학습하는 데 도움을 준다.

C10은 `attention_logits_QK / sqrt(d_k)` 뒤 key 위치 축에 softmax를 적용한다. 이는 **attention 내부 softmax 경로**에 대한 설명이며, 모든 파라미터의 기울기가 사라진다는 뜻은 아니다. V를 통해 전달되는 기울기는 별도 경로다. Scaling 하나로 모든 학습 불안정성을 해결하는 것도 아니다.

---

<a id="a3"></a>
## 3) 왜 Transformer는 RNN과 CNN 대비 장기의존성(long-range dependency)에 유리하다고 주장하는가?  `[A3]`

> 허브: [R01](transformer_paper_guide.md#r01) · [R11](transformer_paper_guide.md#r11)
> 근거: [CS§0](A.ing_Transformer_Cheat_sheet.md#cs0) · 논문 Table 1의 세 비교 축 · E01/E02 및 Table 1

### (1) Maximum Path Length의 의미

> 허브: [R11](transformer_paper_guide.md#r11)

두 위치 사이에 정보가 전달될 수 있는 **가장 짧은 연결 경로**를 생각하고, 가능한 위치 쌍들 중 그 길이가 가장 큰 값을 비교한 것이다. 네트워크 안에서 일부러 돌아가는 모든 경로 중 가장 긴 것을 고른다는 뜻은 아니다.

논문 §4는 멀리 떨어진 위치 사이에서 forward 신호와 backward 기울기가 거쳐야 하는 경로가 짧을수록 장거리 의존성을 학습하기 쉽다고 설명한다. Table 1의 계산량·순차 연산 수·최대 경로 길이는 서로 다른 비교 기준이다.

### (2) Self-attention이 장거리 의존성 학습에 유리한 이유

> 허브: [R01](transformer_paper_guide.md#r01) · [R11](transformer_paper_guide.md#r11)

| 구조 | 최대 경로 길이 | 정보가 전달되는 방식 |
| --- | --- | --- |
| Self-attention | $O(1)$ | 한 층에서 허용된 모든 위치를 직접 참고 |
| RNN | $O(n)$ | 먼 위치에 도달하려면 중간 상태들을 순서대로 거침 |
| Dilated CNN | $O(\log_k n)$ | 층을 쌓아 참조 범위를 확장 |

여기서 n은 시퀀스 길이, k는 convolution의 kernel 폭이다. Table 1의 CNN 경로 길이는 dilated convolution에 해당하며, §4 본문은 연속된 kernel을 쓰는 경우 필요한 층 수 $O(n/k)$도 구분한다.

Self-attention은 먼 토큰의 정보를 중간 위치마다 반복해서 전달할 필요가 없다. 그만큼 정보와 기울기가 지나는 경로를 줄일 수 있다는 것이 논문의 비교 논리다. 이는 **모든 데이터에서 장거리 관계를 반드시 정확히 학습한다**는 보장은 아니다.

또한 $O(1)$은 경로 길이이며, 총 계산량이나 메모리가 일정하다는 뜻이 아니다. 일반적인 attention 점수표는 n개 위치의 모든 쌍을 담으므로 $n\times n$ 크기다. E01·E02는 각각 scaling·위치 정보 관찰이며, 이 경로 길이 비교의 직접 근거는 §4와 Table 1이다.

---

<a id="a4"></a>
## 4) Attention layer만 여러 층 쌓는 대신, FFN을 함께 사용하는 이유는 무엇인가?  `[A4]`

> 허브: [R08](transformer_paper_guide.md#r08) · [R03](transformer_paper_guide.md#r03)
> 근거: [CS§5](A.ing_Transformer_Cheat_sheet.md#cs5) · [C13](../Week2/A.ing_Transformer_Cookbook.md#c13) · [C14](../Week2/A.ing_Transformer_Cookbook.md#c14) · N-14–N-15

### (1) Attention 뒤에 position-wise FFN을 두는 이유

> 허브: [R08](transformer_paper_guide.md#r08)

Attention은 다른 위치에서 필요한 정보를 모으고, FFN은 그렇게 얻은 **각 위치의 표현을 비선형적으로 변환**한다. 논문 §3.3의 FFN은 다음과 같다.

$$FFN(x)=\max(0,xW_1+b_1)W_2+b_2$$

- 첫 선형변환은 토큰 벡터의 특징 차원들을 결합한다.
- ReLU는 그 결과에 비선형성을 추가한다.
- 두 번째 선형변환은 결과를 모델의 표현 차원으로 돌려놓는다.

Position-wise는 **서로 다른 토큰을 FFN 안에서 직접 섞지 않는다**는 뜻이다. 같은 층의 모든 위치는 동일한 가중치와 편향을 공유한다. 토큰마다 별도의 FFN을 학습하거나, 벡터의 각 성분을 서로 독립적으로 처리한다는 뜻이 아니다.

### (2) FFN이 추가하는 표현 능력

> 허브: [R08](transformer_paper_guide.md#r08) · [R03](transformer_paper_guide.md#r03)

논문 base의 FFN은 `512 → 2048 → 512` 구조다. 더 큰 중간 공간에서 특징을 조합하고 ReLU를 적용한 뒤, 결과를 다시 512차원으로 만든다. Attention의 위치 간 정보 결합에 더해 **각 토큰의 특징을 변환하는 학습 가능한 비선형 경로**를 제공한다.

C14의 두 Linear와 ReLU가 이 역할을 한다. 마지막 차원이 E로 돌아오므로 C13의 residual 덧셈에서 입력과 출력의 shape이 모두 `(N, L, E)`가 된다.

“Attention은 선형이고 FFN만 비선형이다”라는 설명은 정확하지 않다. Attention 비율을 고정하면 V에 대한 가중합은 선형이지만, 실제 attention 비율은 입력에 따라 Q·K와 softmax로 계산된다. 또한 §3.3은 FFN 구조를 설명하며, FFN을 제거한 모든 대안보다 항상 좋은 성능을 낸다는 직접 비교 실험을 제시하지는 않는다.

### (3) 심화: ReLU를 제거한 FFN과 Transformer 전체의 차이

> 허브: [R08](transformer_paper_guide.md#r08) · [R03](transformer_paper_guide.md#r03)

ReLU를 제거한 식을 전개하면 다음과 같다.

$$FFN(x)=(xW_1+b_1)W_2+b_2=x(W_1W_2)+(b_1W_2+b_2)$$

$$W_{eff}=W_1W_2,\qquad b_{eff}=b_1W_2+b_2$$

따라서 FFN은 **하나의 선형변환과 편향**, 즉 affine 변환 $xW_{eff}+b_{eff}$로 합쳐진다. 중간 차원을 아무리 늘려도 두 변환 사이에 비선형 연산이 없다면 비선형 함수를 만들 수 없다. 중간 차원에 따라 행렬의 rank 제약이나 학습 과정은 달라질 수 있지만, affine 변환이라는 사실은 같다.

그러나 **Transformer 전체가 선형 모델이 되는 것은 아니다.**

- Attention은 입력에서 만든 Q·K의 내적과 softmax로 비율을 계산한다. 이 비율도 입력에 따라 달라진다.
- LayerNorm은 현재 입력에서 평균과 분산을 계산해 정규화한다. 고정된 하나의 가중치 행렬과 편향으로 합칠 수 없다.
- 출력 확률을 만들 때 사용하는 softmax도 비선형 연산이다.

즉, 제거되는 것은 **FFN 내부의 ReLU 비선형성**이다. Attention과 LayerNorm 등에 남아 있는 비선형성까지 없어지는 것은 아니다. 이 설명은 §3.1~§3.3의 연산을 바탕으로 한 추론이다.

---

<a id="a5"></a>
## 5) Decoder의 self-attention에는 look-ahead mask가 필요한 이유는 무엇인가?  `[A5]`

> 허브: [R02](transformer_paper_guide.md#r02) · [R07](transformer_paper_guide.md#r07) · [R08](transformer_paper_guide.md#r08)
> 근거: [CS§4](A.ing_Transformer_Cheat_sheet.md#cs4) · [C3](../Week2/A.ing_Transformer_Cookbook.md#c3) · [C16](../Week2/A.ing_Transformer_Cookbook.md#c16) · [C19](../Week2/A.ing_Transformer_Cookbook.md#c19) · N-20/N-28–N-36

### (1) Auto-regressive 조건

> 허브: [R02](transformer_paper_guide.md#r02)

출력 문장의 확률을 다음과 같이 분해하는 생성 방식이다.

$$p(y\mid x)=\prod_{t=1}^{m}p(y_t\mid y_{<t},x)$$

$t$번째 토큰을 예측할 때는 **원문 x와 앞서 나온 출력 토큰들**만 사용한다. 아직 예측하지 않은 현재 정답 $y_t$나 이후 정답을 입력 정보로 사용해서는 안 된다. §3 첫 문단은 다음 토큰을 생성할 때 이전에 생성한 토큰을 추가 입력으로 사용한다고 설명한다.

### (2) Look-ahead mask가 없으면 생기는 정답 유출

> 허브: [R02](transformer_paper_guide.md#r02) · [R07](transformer_paper_guide.md#r07)

학습할 때 정답 번역문을 한 칸 이동해 decoder 입력으로 준다. 다음 표에서 열 번호는 0부터 센다.

| 위치 | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Decoder 입력 | BOS | I | eat | apples |
| 예측할 정답 | I | eat | apples | EOS |

위치 1은 입력 `I`로 정답 `eat`을 예측한다. Mask가 없으면 입력 위치 2의 `eat`을 볼 수 있어 **지금 맞혀야 할 정답을 미리 참고**하게 된다. 생성할 때는 그 정답이 아직 없으므로 학습 때와 사용할 수 있는 정보가 달라진다.

§3.2.3은 허용되지 않은 attention 점수를 softmax 전에 $-\infty$로 바꾸어 해당 비율을 0으로 만든다고 설명한다. 실습의 C9는 충분히 작은 음수를 사용한다. C3의 causal mask는 현재 입력 위치까지 허용하고 미래 입력 위치를 가린다.

§3.1의 **입력 한 칸 이동과 masking을 함께 사용**해야 예측할 정답보다 앞선 토큰만 참고할 수 있다. PAD를 참고하지 않게 하는 padding mask와 PAD 위치를 손실에서 제외하는 처리도 서로 다른 역할이다.

### (3) 심화: 입력 이동 없이 현재 위치까지 가리면 충분한가?

> 허브: [R02](transformer_paper_guide.md#r02) · [R07](transformer_paper_guide.md#r07) · [R08](transformer_paper_guide.md#r08)

**충분하지 않다. Attention 연결을 가려도 현재 정답의 embedding이 residual 경로로 전달된다.**

문제의 설정에서 위치 1의 입력과 정답은 모두 `eat`이다. 이 위치의 입력 표현을 $x_1$이라 하면, $x_1$에는 이미 `eat`의 embedding이 포함되어 있다.

Fig.1의 첫 decoder 서브레이어는 다음과 같은 residual 연결을 갖는다. 식에서는 dropout을 생략했다.

$$z_1=LayerNorm\left(x_1+MaskedSelfAttention(X)_1\right)$$

Mask는 attention이 현재·미래 위치의 K·V를 참고하지 못하게 할 뿐, **덧셈의 $x_1$을 제거하지 않는다.** 따라서 다음 경로는 여전히 열려 있다.

`정답 eat의 embedding → residual 덧셈 → LayerNorm → 이후 decoder 층 → 출력 점수`

실습에서도 N-21의 `masked_self_attention_output + x`가 이 연결이다. LayerNorm이 있다고 해서 정답 토큰 정보가 반드시 지워지는 것은 아니다. 현재 위치의 Q 역시 현재 입력에서 만들어지므로, attention 비율을 계산하는 경로에도 정답 입력의 영향을 받을 여지가 있다.

해결 방법은 입력을 `[BOS, I, eat, apples]`, 정답을 `[I, eat, apples, EOS]`로 나누고 causal mask를 함께 사용하는 것이다. 그러면 residual 경로로 전달되는 현재 입력도 **예측할 정답보다 앞선 토큰**이 된다. 첫 위치의 빈 attention 처리 여부와 별개로, 정답 유출의 핵심은 입력 이동을 생략했다는 데 있다.

---

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin. *Attention Is All You Need.* NIPS 2017.
