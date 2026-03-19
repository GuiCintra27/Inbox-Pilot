export type AnalysisCategory = "Produtivo" | "Improdutivo";

export interface AnalysisResult {
  category: AnalysisCategory;
  confidence: number;
  rationale: string;
  suggestedReply: string;
  keywords: string[];
  provider: string;
}
