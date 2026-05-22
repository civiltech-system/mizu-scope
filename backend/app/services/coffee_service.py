def calc_coffee_score(
    hardness: float | None,
    ph: float | None,
    magnesium: float | None,
) -> int:
    """
    ハンドドリップ向き基準でコーヒー適性スコアを1〜5で算出。
    硬度 50〜150 mg/L、pH 6.5〜7.5、Mg 10〜30 mg/L が最適。
    """
    if hardness is None:
        return 3

    score = 3.0

    if 50 <= hardness <= 150:
        score += 1
    elif hardness < 20 or hardness > 300:
        score -= 1

    if ph is not None:
        if 6.5 <= ph <= 7.5:
            score += 0.5
        elif ph < 6.0 or ph > 8.0:
            score -= 0.5

    if magnesium is not None:
        if 10 <= magnesium <= 30:
            score += 0.5

    return max(1, min(5, round(score)))
