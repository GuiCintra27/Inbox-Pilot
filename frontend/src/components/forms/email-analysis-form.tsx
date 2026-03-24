"use client";

import { useEffect, useId, useRef, useState, type FormEvent, type ReactNode } from "react";
import { FileText, FileUp, Loader2, Paperclip, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import {
  AnalyzeEmailError,
  ACCEPTED_FILE_EXTENSIONS,
  MAX_EMAIL_TEXT_CHARS,
  formatUploadLimit,
  validateSelectedEmailFile,
  type AnalyzeEmailResponse
} from "@/lib/email-analysis";
import { useEmailAnalysis } from "@/hooks/use-email-analysis";

export interface EmailAnalysisFormProps {
  className?: string;
  apiBaseUrl?: string;
  initialEmailText?: string;
  examplesSlot?: ReactNode;
  onResult?: (result: AnalyzeEmailResponse) => void;
  onError?: (error: AnalyzeEmailError) => void;
  onSubmittingChange?: (isSubmitting: boolean) => void;
  onInteractionReset?: () => void;
}

export function EmailAnalysisForm({
  className,
  apiBaseUrl,
  initialEmailText = "",
  examplesSlot,
  onResult,
  onError,
  onSubmittingChange,
  onInteractionReset
}: EmailAnalysisFormProps) {
  const fileInputId = useId();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [emailText, setEmailText] = useState(initialEmailText);
  const [emailFile, setEmailFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const { analyze, clearError, clearResult, error, isSubmitting } = useEmailAnalysis({
    baseUrl: apiBaseUrl,
    onSuccess: (result) => {
      setIsSuccess(true);
      onResult?.(result);
    },
    onError
  });

  const selectedFileName = emailFile?.name ?? null;

  useEffect(() => {
    setEmailText(initialEmailText);
  }, [initialEmailText]);

  useEffect(() => {
    onSubmittingChange?.(isSubmitting);
  }, [isSubmitting, onSubmittingChange]);

  const emitLocalError = (message: string, status: number) => {
    setLocalError(message);
    onError?.(new AnalyzeEmailError(message, status));
  };

  const handleFileChange = (file: File | null) => {
    clearError();
    clearResult();
    setIsSuccess(false);
    setLocalError(null);
    onInteractionReset?.();

    const validationError = validateSelectedEmailFile(file);
    if (validationError) {
      setEmailFile(null);
      emitLocalError(validationError.message, validationError.status);
      return;
    }

    setEmailFile(file);
  };

  const handleDrop = (files: FileList | null) => {
    if (!files || files.length === 0) {
      return;
    }

    handleFileChange(files[0]);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    clearError();
    clearResult();
    setIsSuccess(false);
    setLocalError(null);

    const trimmedText = emailText.trim();
    const resolvedFile = emailFile && emailFile.size > 0 ? emailFile : null;

    const fileValidationError = validateSelectedEmailFile(resolvedFile);
    if (fileValidationError) {
      emitLocalError(fileValidationError.message, fileValidationError.status);
      return;
    }

    if (!resolvedFile && trimmedText.length > MAX_EMAIL_TEXT_CHARS) {
      emitLocalError(
        `O texto excede o limite de ${MAX_EMAIL_TEXT_CHARS.toLocaleString("pt-BR")} caracteres. Reduza o conteúdo antes de enviar.`,
        413
      );
      return;
    }

    try {
      await analyze({
        emailText: trimmedText || undefined,
        emailFile: resolvedFile
      });
    } catch {
      // State is already tracked by the hook.
    }
  };

  return (
    <Card className={className}>
      <CardHeader className="gap-3 px-5 pt-5 sm:px-6">
        <div className="flex items-center gap-2 text-[12px] font-medium text-slate-900">
          <FileText className="h-3.5 w-3.5 text-[#19c8f2]" />
          <span>Conteúdo do Email</span>
        </div>
        <CardTitle className="sr-only">Analisar email</CardTitle>
        <CardDescription>
          Cole o conteúdo do email ou faça o upload de um arquivo.
        </CardDescription>
      </CardHeader>
      <CardContent className="px-5 pb-5 sm:px-6">
        <form className="grid gap-5" onSubmit={handleSubmit}>
          <div className="grid gap-3">
            <Textarea
              id="email-text"
              value={emailText}
              onChange={(event) => {
                setEmailText(event.target.value);
                clearError();
                setLocalError(null);
                setIsSuccess(false);
                onInteractionReset?.();
              }}
              placeholder="Bom dia, equipe. A reunião de hoje foi excelente para alinhar os próximos passos do projeto Alpha. Gostaria de confirmar se todos receberam a ata e se as tarefas designadas para sexta-feira estão claras. Aguardo confirmação."
              className="min-h-[158px] resize-y rounded-[14px] border-[#edeae4] bg-white p-4 text-[13px] leading-7 text-slate-700 shadow-none focus-visible:ring-1 focus-visible:ring-[#19c8f2]"
            />
            <div className="flex items-center justify-between gap-3 text-[11px] text-slate-400">
              <span>Texto livre continua aceito mesmo quando você usa upload.</span>
              <span
                className={
                  emailText.trim().length > MAX_EMAIL_TEXT_CHARS
                    ? "font-medium text-amber-600"
                    : ""
                }
              >
                {emailText.trim().length.toLocaleString("pt-BR")} /{" "}
                {MAX_EMAIL_TEXT_CHARS.toLocaleString("pt-BR")}
              </span>
            </div>
          </div>

          <div className="grid gap-3">
            <div className="flex items-center gap-2 text-[12px] font-medium text-slate-900">
              <Paperclip className="h-3.5 w-3.5 text-[#19c8f2]" />
              <label htmlFor={fileInputId}>Anexo (opcional)</label>
            </div>

            <input
              ref={fileInputRef}
              id={fileInputId}
              type="file"
              accept=".txt,.pdf,application/pdf,text/plain"
              className="sr-only"
              onChange={(event) => handleFileChange(event.target.files?.[0] ?? null)}
            />

            <button
              type="button"
              aria-describedby={`${fileInputId}-help`}
              className={`group flex min-h-[104px] w-full flex-col items-center justify-center rounded-[14px] border border-dashed px-5 py-6 text-left transition-colors ${
                isDragging
                  ? "border-[#19c8f2] bg-[#f3fcff]"
                  : "border-[#efece6] bg-[#fdfdfc] hover:border-[#7fe2fb] hover:bg-[#f7fdff]"
              }`}
              onClick={() => fileInputRef.current?.click()}
              onDragEnter={(event) => {
                event.preventDefault();
                event.stopPropagation();
                setIsDragging(true);
              }}
              onDragOver={(event) => {
                event.preventDefault();
                event.stopPropagation();
                setIsDragging(true);
              }}
              onDragLeave={(event) => {
                event.preventDefault();
                event.stopPropagation();
                setIsDragging(false);
              }}
              onDrop={(event) => {
                event.preventDefault();
                event.stopPropagation();
                setIsDragging(false);
                handleDrop(event.dataTransfer.files);
              }}
              >
              <div className="flex items-center gap-3 text-[13px] font-medium text-slate-700">
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#effcff] text-[#19c8f2]">
                  <FileUp className="h-4 w-4" />
                </div>
                <span>Arraste um .txt ou .pdf ou clique para selecionar</span>
              </div>
              <p id={`${fileInputId}-help`} className="mt-2 max-w-md text-center text-[10px] leading-5 text-slate-400">
                Tipos aceitos: {ACCEPTED_FILE_EXTENSIONS.join(", ")}. Limite de{" "}
                {formatUploadLimit()} por arquivo.
              </p>
            </button>

            {selectedFileName ? (
              <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[#edeae4] bg-[#fafaf8] px-4 py-3 text-sm">
                <div className="flex items-center gap-2 text-foreground">
                  <Paperclip className="h-4 w-4 text-muted-foreground" />
                  <span className="max-w-[18rem] truncate">{selectedFileName}</span>
                </div>
                <button
                  type="button"
                  className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground transition-colors hover:text-foreground"
                  onClick={() => {
                    handleFileChange(null);
                    if (fileInputRef.current) {
                      fileInputRef.current.value = "";
                    }
                  }}
                >
                  <X className="h-3.5 w-3.5" />
                  Remover
                </button>
              </div>
            ) : null}
          </div>

          {examplesSlot ? (
            <div className="grid gap-3">
              <p className="text-[12px] font-medium text-slate-900">Exemplos Prontos</p>
              {examplesSlot}
            </div>
          ) : null}

          <Separator className="bg-[#efede8]" />

          <div className="grid gap-4">
            <div className="rounded-2xl border border-amber-300/80 bg-amber-50 px-4 py-3 text-[12px] leading-6 text-amber-800">
              <span className="font-medium">Atenção:</span> a primeira análise pode levar até 30s,
              porque o backend em produção ativa sob demanda no Render.
            </div>

            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="grid gap-1 text-[11px] text-slate-500">
                <span>Arquivo tem prioridade quando texto e upload são enviados juntos.</span>
                <span>O provider real aparece no resultado para facilitar a leitura.</span>
              </div>
              <div className="flex items-center gap-5">
                <button
                  type="button"
                  className="text-[12px] font-medium text-slate-600 transition-colors hover:text-slate-900"
                  onClick={() => {
                    setEmailText("");
                    handleFileChange(null);
                    clearError();
                    clearResult();
                    setLocalError(null);
                    setIsSuccess(false);
                    onInteractionReset?.();
                    if (fileInputRef.current) {
                      fileInputRef.current.value = "";
                    }
                  }}
                >
                  Limpar
                </button>
                <Button
                  type="submit"
                  className="h-[36px] rounded-full border-0 bg-[#19c8f2] px-5 text-[12px] font-medium text-white shadow-none hover:bg-[#17bce4]"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Analisando
                    </>
                  ) : (
                    "Analisar email"
                  )}
                </Button>
              </div>
            </div>
          </div>

          <div aria-live="polite" className="grid gap-3">
            {localError || error ? (
              <div className="rounded-2xl border border-destructive/20 bg-destructive/5 px-4 py-3 text-sm leading-6 text-destructive">
                {localError ?? error?.message}
              </div>
            ) : null}
            {isSuccess ? (
              <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/8 px-4 py-3 text-sm leading-6 text-emerald-800">
                Análise enviada com sucesso. O painel ao lado já exibe a categoria, a confiança e a resposta sugerida.
              </div>
            ) : null}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
