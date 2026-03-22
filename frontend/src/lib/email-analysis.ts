export type EmailAnalysisCategory = "Produtivo" | "Improdutivo";

export const MAX_UPLOAD_BYTES = 1_048_576;
export const MAX_EMAIL_TEXT_CHARS = 12_000;
export const ACCEPTED_FILE_EXTENSIONS = [".txt", ".pdf"] as const;

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

export function formatUploadLimit(bytes = MAX_UPLOAD_BYTES): string {
  if (bytes >= 1024 * 1024) {
    return `${Math.round(bytes / (1024 * 1024))}MB`;
  }

  return `${Math.round(bytes / 1024)}KB`;
}

export function getApiBaseUrl(): string {
  const value = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();

  if (value) {
    return value.replace(/\/+$/, "");
  }

  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "http://127.0.0.1:8000";
    }
  }

  throw new AnalyzeEmailError(
    "NEXT_PUBLIC_API_BASE_URL não está configurada no frontend.",
    500
  );
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

export function isAcceptedEmailFile(file: File): boolean {
  const lowerName = file.name.toLowerCase();
  return ACCEPTED_FILE_EXTENSIONS.some((extension) => lowerName.endsWith(extension));
}

export function validateSelectedEmailFile(file: File | null): AnalyzeEmailError | null {
  if (!file) {
    return null;
  }

  if (!isAcceptedEmailFile(file)) {
    return new AnalyzeEmailError(
      "Envie apenas arquivos .txt ou .pdf para análise.",
      415
    );
  }

  if (file.size > MAX_UPLOAD_BYTES) {
    return new AnalyzeEmailError(
      `O arquivo excede o limite de ${formatUploadLimit()} por análise.`,
      413
    );
  }

  return null;
}

function normalizeErrorMessage(status: number, fallbackMessage: string): string {
  switch (status) {
    case 400:
      return "Envie um texto válido ou selecione um arquivo não vazio para continuar.";
    case 413:
      return `O conteúdo enviado excede o limite permitido. Reduza o texto ou use um arquivo de até ${formatUploadLimit()}.`;
    case 415:
      return "Formato inválido. Use apenas arquivos .txt ou .pdf.";
    case 429:
      return "Muitas análises em sequência. Aguarde alguns instantes e tente novamente.";
    case 500:
      return "A análise não pôde ser concluída agora. Tente novamente em instantes.";
    default:
      return fallbackMessage;
  }
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as AnalyzeEmailErrorPayload;
    const detail = payload.detail;

    if (typeof detail === "string") {
      return normalizeErrorMessage(response.status, detail);
    }

    if (Array.isArray(detail) && detail.length > 0 && detail[0]?.msg) {
      return normalizeErrorMessage(response.status, detail[0].msg);
    }

    if (detail && typeof detail === "object" && "msg" in detail && detail.msg) {
      return normalizeErrorMessage(response.status, detail.msg);
    }

    return normalizeErrorMessage(
      response.status,
      payload.message ?? payload.error ?? `Falha na análise (${response.status}).`
    );
  } catch {
    return normalizeErrorMessage(
      response.status,
      `Falha na análise (${response.status}).`
    );
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
