# CLAUDE.md

## 📌 目的（Purpose）

このアプリケーションは、ユーザーが Datalog 風のリスト形式で与えた結合クエリ（Conjunctive Query）に対して、以下の特徴量を計算するためのシンプルなツールです。

- Fractional Edge Cover (`ρ*`)
- Fractional Edge Packing (`τ*`)
- AGM Bound（各リレーションサイズが1と仮定）

研究や教育の場において、クエリ構造の理論的性質をすばやく評価することを目的とします。

---

## 📥 入力（Input）

- **形式**：Datalog風のリスト形式（1行1リレーション）

- **例**：
R(a, b)
S(b, c)
T(a, c)

- 各リレーションは名前と引数（属性）を持ちます。

---

## 📤 出力（Output）

以下の情報をテーブル形式でStreamlit上に表示します：

- 頂点数（|V|）
- エッジ数（|E|）
- ハイパーグラフの rank（最大エッジサイズ）
- Fractional Edge Cover（ρ*）
- Fractional Edge Packing（τ*）
- AGM Bound（全リレーションサイズ = 1 の仮定）
- `ρ* × τ*` の積（|V| に近いかのチェック）

---

## ⚙️ 機能要件（Functional Requirements

| ID  | 機能内容                                                                |
|-----|-------------------------------------------------------------------------|
| F-1 | 入力クエリ（Datalog風テキスト）をパースし、ハイパーグラフ構造を構築する |
| F-2 | 線形計画問題を解き、fractional edge cover（ρ*）と packing（τ*）を求める |
| F-3 | AGM Bound を計算（全リレーションサイズ = 1 を仮定）                     |
| F-4 | 結果を Streamlit 上にテーブルで表示する                                 |

---
