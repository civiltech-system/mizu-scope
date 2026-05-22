export type WaterType = "soft" | "medium" | "hard" | "very_hard";

export function getWaterType(hardness: number | null | undefined): WaterType | null {
  if (hardness == null) return null;
  if (hardness <= 60) return "soft";
  if (hardness <= 120) return "medium";
  if (hardness <= 180) return "hard";
  return "very_hard";
}

export const waterTypeLabel: Record<WaterType, string> = {
  soft: "軟水",
  medium: "中硬水",
  hard: "硬水",
  very_hard: "超硬水",
};

export const waterTypeColor: Record<WaterType, string> = {
  soft: "#3B82F6",
  medium: "#22C55E",
  hard: "#EAB308",
  very_hard: "#EF4444",
};
