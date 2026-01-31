# 実機実行ガイド

> **注意**: 本ガイドのデバイス名・価格・無料枠条件は執筆時点（2026年1月）のものです。最新情報は各クラウドベンダーの公式ページを参照してください。

> **免責**: 本リポジトリのShor実装は教育・実証目的のcompiled circuitを含み、大規模Nに対する汎用RSA破りを目的とするものではありません。

## 概要

AWS BraketまたはIBM Quantumを使用して、Shorのアルゴリズムを実際の量子ハードウェアで実行する方法。

## 方法1: AWS Braket

### セットアップ

```bash
# AWS Braket SDKをインストール
pip install amazon-braket-sdk

# またはプロジェクトと一緒にインストール
pip install -e ".[aws]"
```

### AWS認証情報の設定

```bash
# 方法A: AWS CLI
aws configure

# 方法B: 環境変数
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 利用可能なデバイス

| デバイス | タイプ | 量子ビット | 忠実度 | コスト |
|---------|--------|-----------|--------|--------|
| **IonQ Aria** | イオントラップ | 25 | 99.4% 2Q | $0.03/shot + $0.01/gate |
| **IonQ Forte** | イオントラップ | 32 | 高 | $0.03/shot + $0.01/gate |
| **Rigetti Ankaa-3** | 超伝導 | 84 | 99.5% 2Q | $0.00035/shot + $0.00035/gate |
| **IQM Garnet** | 超伝導 | 20 | 良好 | $0.00145/shot |

### 使用方法

```python
from quantum_rsa.backends import AWSBraketBackend
from quantum_rsa.algorithms import QuantumShor
from quantum_rsa.modexp import get_config

# バックエンドを初期化
backend = AWSBraketBackend(device="ionq_aria")

# 回路を構築
shor = QuantumShor()
config = get_config(15)
circuit = shor._construct_circuit(7, 15, config)

# 実機で実行
counts = backend.run(circuit, shots=100)
print(counts)
```

### 推奨アプローチ

```python
# 1. まずAWSシミュレータでテスト（安価）
backend_sim = AWSBraketBackend(device="sv1")
counts = backend_sim.run(circuit, shots=1000)

# 2. その後、少ないショット数で実機実行
backend_real = AWSBraketBackend(device="ionq_aria")
counts = backend_real.run(circuit, shots=100)
```

---

## 方法2: IBM Quantum

### セットアップ

```bash
# IBM Quantum Runtimeをインストール
pip install qiskit-ibm-runtime

# またはプロジェクトと一緒にインストール
pip install -e ".[ibm]"
```

### APIトークンの取得

1. https://quantum.ibm.com/ でアカウント作成
2. Dashboard → API Token へ移動
3. トークンをコピー

### 認証情報の保存

```python
from quantum_rsa.backends import IBMQuantumBackend

# トークンを保存（一度だけ必要）
IBMQuantumBackend.save_account("YOUR_API_TOKEN_HERE")
```

### 利用可能なデバイス（無料枠）

| デバイス | 量子ビット | 場所 | 備考 |
|---------|-----------|------|------|
| **ibm_kyoto** | 127 | 日本 | 可用性良好 |
| **ibm_osaka** | 127 | 日本 | 可用性良好 |
| **ibm_sherbrooke** | 127 | カナダ | 混雑しがち |
| **ibm_brisbane** | 127 | オーストラリア | 可用性良好 |

### 使用方法

```python
from quantum_rsa.backends import IBMQuantumBackend
from quantum_rsa.algorithms import QuantumShor
from quantum_rsa.modexp import get_config

# 利用可能なバックエンドを一覧表示
backends = IBMQuantumBackend.list_backends()
for b in backends:
    print(f"{b['name']}: {b['num_qubits']} qubits, {b['pending_jobs']} jobs queued")

# 初期化（最も空いているものを自動選択）
backend = IBMQuantumBackend()

# またはバックエンドを指定
backend = IBMQuantumBackend(backend_name="ibm_kyoto")

# 実行
shor = QuantumShor()
config = get_config(15)
circuit = shor._construct_circuit(7, 15, config)

counts = backend.run(circuit, shots=1000)
print(counts)
```

---

## 重要な注意点

### 1. 回路最適化

ユニタリ行列実装はトランスパイル後に多くのゲートを生成する傾向がある:

```python
from qiskit import transpile

# トランスパイル前
print(f"Original: {circuit.depth()} depth")

# 実機用にトランスパイル後
qc_transpiled = transpile(circuit, backend, optimization_level=3)
print(f"Transpiled: {qc_transpiled.depth()} depth")
```

### 2. N=15から始める

実機はノイズが多い。最小のケースから始めるのが良い:

```python
# 推奨: 小さい数から始める
result = run_shor(15, method='quantum', shots=1000)

# 大きなNには最適化回路が必要な場合がある
result = run_shor(77, method='quantum', shots=1000)
```

### 3. ノイズを想定する

実機の結果には通常ノイズが含まれる:

```
シミュレータ: {'0000': 256, '0100': 256, '1000': 256, '1100': 256}
実機:        {'0000': 180, '0100': 210, '1000': 195, '1100': 220, '0001': 45, ...}
```

エラー緩和の使用:
```python
# 今後対応予定: エラー緩和サポート
```

### 4. コストに注意

**AWS Braket:**
- IonQ: 1回あたり約$3-10（100 shots）
- Rigetti: 1回あたり約$0.05（100 shots）

**IBM Quantum:**
- 無料枠: 月10分
- 従量課金も利用可能

---

## クイックスタートスクリプト

```python
#!/usr/bin/env python3
"""実機でShorのアルゴリズムを実行"""

from quantum_rsa.runner import run_shor

# 方法1: AWS Braket
# pip install amazon-braket-sdk
# aws configure

from quantum_rsa.backends import AWSBraketBackend
backend = AWSBraketBackend(device="sv1")  # まずシミュレータで

# 方法2: IBM Quantum
# pip install qiskit-ibm-runtime
# IBMQuantumBackend.save_account("YOUR_TOKEN")

# from quantum_rsa.backends import IBMQuantumBackend
# backend = IBMQuantumBackend()

# N=15で実行
from quantum_rsa.algorithms import QuantumShor
from quantum_rsa.modexp import get_config

shor = QuantumShor()
config = get_config(15)
circuit = shor._construct_circuit(7, 15, config)

counts = backend.run(circuit, shots=1000)
print("結果:", counts)
```

---

## トラブルシューティング

### "Custom unitary gates must be decomposed"

modexpはユニタリ行列を使用。先にトランスパイルが必要:

```python
from qiskit import transpile

# 基本ゲートに分解
basis_gates = ['h', 'cx', 'rz', 'rx', 'ry', 'x', 'y', 'z']
circuit_decomposed = transpile(circuit, basis_gates=basis_gates, optimization_level=3)
```

### "Job queue is long"

IBM Quantum無料枠はキューが長い。対処法:
- 別のバックエンドを試す（ibm_brisbaneは比較的空いていることが多い）
- AWS Braketを使用（従量課金、キューなし）
- オフピーク時間に実行

### "Results are too noisy"

現在のNISQデバイスはエラー率が高い。対処法:
- ショット数を増やす（平均化を増やす）
- エラー緩和技術を使用
- 回路を簡素化（深度を減らす）
