def get_water_type(hardness: float | None) -> str | None:
    if hardness is None:
        return None
    if hardness <= 60:
        return "soft"
    elif hardness <= 120:
        return "medium"
    elif hardness <= 180:
        return "hard"
    else:
        return "very_hard"
