# Quantum RSA Lab

RSA × 量子アルゴリズム実験のための専用リポジトリです。Shor アルゴリズムの理論整理から小規模実装、AWS Braket での実機検証、成果公開までを一気通貫で扱えるように構成しています。

## リポジトリ構成

```
quantum-rsa-lab/
├ docs/                # ロードマップ、調査メモ、設計資料
├ notebooks/           # Jupyter 実験ノート（Qiskit/Braket）
├ src/
│ └ quantum_rsa/
│   ├ __init__.py
│   └ shor_demo.py     # 小規模 Shor 実装（N=15 から開始）
├ pyproject.toml       # 依存管理 (Qiskit, Matplotlib, etc.)
├ requirements.txt     # シンプルに `pip install -r` したい場合用
└ README.md
```

## セットアップ

1. Python 3.11+ を用意（pyenv など）
2. このリポジトリをクローン
3. 仮想環境を作成して依存をインストール

```bash
python -m venv .venv
source .venv/bin/activate  # Windows は .venv\\Scripts\\activate
pip install -r requirements.txt
```

> Poetry/uv など他のツールを使いたい場合は `pyproject.toml` を参照してインストールしてください。

## 進め方 (ハイレベル)

1. **理論フェーズ**: RSA / Shor / 既存研究の整理 → `docs/roadmap.md`
2. **ローカルフェーズ**: Qiskit で N=15,21,33… の Shor 実験 → `notebooks/`
3. **AWS フェーズ**: AWS Braket (SV1→QPU) で挙動とコスト測定
4. **改良フェーズ**: mod-exp 最適化、誤り緩和の検証
5. **公開フェーズ**: 記事化、GitHub 公開、比較表整備
6. **発展フェーズ**: VQF/QAOA など他手法、PQC 実装連携

## 現状

- ✅ リポジトリ雛形、依存、Shor (N=15) デモコードを配置
- ⏳ ノートブック、Braket 用サンプル、統計可視化はこれから

## ライセンス

TBD（デフォルトでは MIT を想定）。
