"""Small-scale Shor experiment harness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:
    from qiskit.algorithms import Shor
    from qiskit.primitives import Sampler
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise RuntimeError(
        "Qiskit がインストールされていません。`pip install -r requirements.txt` を先に実行してください。"
    ) from exc


@dataclass
class ShorDemoResult:
    number: int
    base: int
    factors: tuple[int, int]
    shots: int
    raw_result: object


def run_shor_demo(number: int = 15, base: Optional[int] = None, shots: int = 4000) -> ShorDemoResult:
    """Factor ``number`` using Qiskit's Shor implementation.

    Parameters
    ----------
    number:
        合成数 N。既定は 15。
    base:
        生成する a (1 < a < N)。None の場合はアルゴリズムに任せる。
    shots:
        サンプラーのショット数。成功率ログ用。
    """

    if number % 2 == 0:
        raise ValueError("偶数は Shor の対象になりません。別の N を指定してください。")

    sampler = Sampler()  # デフォルトで状態ベクトルシミュレータ
    shor = Shor(sampler=sampler, seed=42, shots=shots)

    result = shor.factor(N=number, a=base)
    factors = tuple(result.factors[0]) if result.factors else (1, number)

    return ShorDemoResult(
        number=number,
        base=base or result.a,
        factors=factors,
        shots=shots,
        raw_result=result,
    )


if __name__ == "__main__":
    demo = run_shor_demo()
    print(f"N={demo.number} を a={demo.base} で実行 → 因数 {demo.factors}")
