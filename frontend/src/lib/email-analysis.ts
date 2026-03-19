export type EmailAnalysisCategory = "Produtivo" | "Improdutivo";

export interface AnalyzeEmailRequest {
  emailText?: string;
  emailFile?: File | null;
}

export interface AnalyzeEmailResponse {
  category: EmailAnalysisCategory;
  confidence: number;
  rationale: string;
  suggested_reply: string;
  keywords: string[];
  provider: string;
}

export interface AnalyzeEmailErrorPayload {
  detail?: string | { msg?: string } | Array<{ msg?: string }>;
  message?: string;
  error?: string;
}

export class AnalyzeEmailError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AnalyzeEmailError";
    this.status = status;
  }
}

export function getApiBaseUrl(): string {
  const value = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  if (!value) {
    throw new AnalyzeEmailError(
      "NEXT_PUBLIC_API_BASE_URL não está configurada no frontend.",
      500
    );
  }

  return value.replace(/\/+$/, "");
}

export function buildAnalyzeUrl(baseUrl = getApiBaseUrl()): string {
  return `${baseUrl}/analyze`;
}

export function buildAnalyzeFormData(input: AnalyzeEmailRequest): FormData {
  const formData = new FormData();
  const text = input.emailText?.trim();

  if (text) {
    formData.append("email_text", text);
  }

  if (input.emailFile) {
    formData.append("email_file", input.emailFile);
  }

  if (!text && !input.emailFile) {
    throw new AnalyzeEmailError(
      "Informe um texto de email ou selecione um arquivo para análise.",
      400
    );
  }

  return formData;
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as AnalyzeEmailErrorPayload;
    const detail = payload.detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail) && detail.length > 0 && detail[0]?.msg) {
      return detail[0].msg;
    }

    if (detail && typeof detail === "object" && "msg" in detail && detail.msg) {
      return detail.msg;
    }

    return payload.message ?? payload.error ?? `Falha na análise (${response.status}).`;
  } catch {
    return `Falha na análise (${response.status}).`;
  }
}

export async function analyzeEmail(
  input: AnalyzeEmailRequest,
  options?: { baseUrl?: string; signal?: AbortSignal }
): Promise<AnalyzeEmailResponse> {
  const formData = buildAnalyzeFormData(input);
  const response = await fetch(buildAnalyzeUrl(options?.baseUrl), {
    method: "POST",
    body: formData,
    signal: options?.signal
  });

  if (!response.ok) {
    throw new AnalyzeEmailError(await readErrorMessage(response), response.status);
  }

  return (await response.json()) as AnalyzeEmailResponse;
}
