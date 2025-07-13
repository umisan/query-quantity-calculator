# Query Quantity Calculator

## 📌 概要

Query Quantity Calculatorは、Datalog風のリスト形式で与えられた結合クエリ（Conjunctive Query）に対して、以下の特徴量を計算するWebアプリケーションです：

- **Fractional Edge Cover** (`ρ*`)
- **Fractional Edge Packing** (`τ*`)
- **AGM Bound**（各リレーションサイズが1と仮定）

研究や教育の場において、クエリ構造の理論的性質をすばやく評価することを目的としています。

## ✨ 機能

- Datalog風クエリのパースとハイパーグラフ構造の構築
- 線形計画問題を解いてfractional edge coverとpackingを計算
- AGM Boundの計算
- インタラクティブなハイパーグラフの可視化
- 結果の詳細な分析と表示

## 📋 要件

- Python 3.8+
- Streamlit
- NumPy
- SciPy
- Plotly
- NetworkX
- Pandas

## 🚀 インストール

### 🐳 Dockerを使用する場合（推奨）

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/umisan/query-quantity-calculator.git
   cd query-quantity-calculator
   ```

2. **Dockerイメージのビルド**
   ```bash
   docker build -t query-quantity-calculator .
   ```

3. **コンテナの実行**
   ```bash
   docker run -p 8501:8501 query-quantity-calculator
   ```

### 🐍 ローカル環境での実行

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/umisan/query-quantity-calculator.git
   cd query-quantity-calculator
   ```

2. **依存関係のインストール**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 使用方法

### Webアプリの起動

**Dockerを使用する場合：**
```bash
docker run -p 8501:8501 query-quantity-calculator
```

**ローカル環境の場合：**
```bash
streamlit run run_app.py
```

どちらの方法でも、ブラウザで `http://localhost:8501` が自動的に開きます。

### クエリ入力例

アプリケーションでは、以下の形式でDatalog風クエリを入力します：

```
R(a, b)
S(b, c)
T(a, c)
```

### 出力結果

計算結果として以下の情報が表示されます：

- **頂点数 (|V|)**: ハイパーグラフの頂点数
- **エッジ数 (|E|)**: ハイパーグラフのエッジ数
- **ハイパーグラフのrank**: 最大エッジサイズ
- **Fractional Edge Cover (ρ*)**: 最小エッジカバー
- **Fractional Edge Packing (τ*)**: 最大エッジパッキング
- **AGM Bound**: 全リレーションサイズ=1での理論限界
- **ρ* × τ***: 積の値（|V|以下であることの確認）

### 可視化

ハイパーグラフの構造がインタラクティブなグラフとして表示され、クエリの構造を視覚的に理解できます。

## 📁 プロジェクト構造

```
query-quantity-calculator/
├── src/
│   └── query_quantity_calculator/
│       ├── __init__.py
│       ├── app.py                # Streamlitアプリケーション
│       ├── hypergraph.py          # ハイパーグラフ構造とその操作
│       ├── parser.py              # Datalogクエリパーサー
│       └── solver.py              # 線形計画ソルバー
├── tests/
│   └── __init__.py
├── run_app.py                     # アプリケーション起動スクリプト
├── requirements.txt               # 依存関係
├── CLAUDE.md                      # プロジェクト詳細仕様
├── README.md                      # このファイル
└── LICENSE
```

## 🧮 理論的背景

このツールは以下の理論に基づいています：

- **Fractional Edge Cover**: ハイパーグラフの各頂点を覆うのに必要な最小エッジ重み
- **Fractional Edge Packing**: 重複しないエッジの最大重み
- **AGM Bound**: 結合クエリの最適な実行時間の理論限界

## 📚 参考文献

- Atserias, A., Grohe, M., & Marx, D. (2008). "Size bounds and query plans for relational joins"
- 結合クエリとハイパーグラフ理論に関する研究

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 🤝 貢献

プロジェクトへの貢献を歓迎します。バグ報告、機能要求、プルリクエストなどお気軽にお寄せください。
