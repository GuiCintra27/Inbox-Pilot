"use client";

import { useEffect, useId, useRef, useState, type FormEvent } from "react";
import { FileUp, Loader2, Paperclip, X } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import {
  AnalyzeEmailError,
  type AnalyzeEmailResponse
} from "@/lib/email-analysis";
import { useEmailAnalysis } from "@/hooks/use-email-analysis";

export interface EmailAnalysisFormProps {
  className?: string;
  apiBaseUrl?: string;
  initialEmailText?: string;
  onResult?: (result: AnalyzeEmailResponse) => void;
  onError?: (error: AnalyzeEmailError) => void;
  onSubmittingChange?: (isSubmitting: boolean) => void;
}

export function EmailAnalysisForm({
  className,
  apiBaseUrl,
  initialEmailText = "",
  onResult,
  onError,
  onSubmittingChange
}: EmailAnalysisFormProps) {
  const fileInputId = useId();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [emailText, setEmailText] = useState(initialEmailText);
  const [emailFile, setEmailFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

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

  const handleFileChange = (file: File | null) => {
    clearError();
    clearResult();
    setIsSuccess(false);
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

    const trimmedText = emailText.trim();
    const resolvedFile = emailFile && emailFile.size > 0 ? emailFile : null;

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
      <CardHeader className="gap-3">
        <Badge variant="outline" className="w-fit border-border/70 bg-background/80 text-[11px] uppercase tracking-[0.24em] text-muted-foreground">
          Demo input
        </Badge>
        <CardTitle className="text-2xl tracking-tight">Analisar email</CardTitle>
        <CardDescription>
          Cole o texto do email, envie um arquivo `.txt` ou `.pdf`, ou use os dois campos juntos.
          O backend mantém a precedência do arquivo e a interface mostra o resultado em seguida.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form className="grid gap-5" onSubmit={handleSubmit}>
          <div className="grid gap-3">
            <label className="text-sm font-medium text-foreground" htmlFor="email-text">
              Texto do email
            </label>
            <Textarea
              id="email-text"
              value={emailText}
              onChange={(event) => {
                setEmailText(event.target.value);
                clearError();
                setIsSuccess(false);
              }}
              placeholder="Exemplo: confirme se a fatura pode ser aprovada hoje e envie o status ao fornecedor."
              className="min-h-[220px] resize-y rounded-3xl border-border/80 bg-background/90 p-4 text-base leading-7 shadow-sm focus-visible:ring-2"
            />
            <p className="text-xs leading-5 text-muted-foreground">
              Aceita texto livre, inclusive junto de um arquivo anexado.
            </p>
          </div>

          <div className="grid gap-3">
            <div className="flex items-center justify-between gap-3">
              <label className="text-sm font-medium text-foreground" htmlFor={fileInputId}>
                Arquivo do email
              </label>
              <span className="text-xs text-muted-foreground">TXT ou PDF</span>
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
              className={`group flex min-h-36 w-full flex-col items-center justify-center rounded-3xl border border-dashed px-5 py-6 text-left transition-colors ${
                isDragging
                  ? "border-foreground bg-foreground/5"
                  : "border-border bg-muted/20 hover:border-foreground/40 hover:bg-muted/40"
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
              <div className="flex items-center gap-3 text-sm font-medium text-foreground">
                <FileUp className="h-4 w-4" />
                <span>Arraste o arquivo para cá ou clique para selecionar</span>
              </div>
              <p id={`${fileInputId}-help`} className="mt-2 max-w-md text-center text-xs leading-5 text-muted-foreground">
                O upload pode ser combinado com o texto colado. Se ambos forem enviados, o backend usa o arquivo como fonte principal.
              </p>
            </button>

            {selectedFileName ? (
              <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-border/70 bg-background px-4 py-3 text-sm">
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

          <Separator />

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="grid gap-1 text-sm text-muted-foreground">
              <span>O backend decide a precedência entre texto e arquivo.</span>
              <span>O resultado completo volta em seguida para a camada de apresentação.</span>
            </div>
            <Button type="submit" className="w-full sm:w-auto" disabled={isSubmitting}>
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

          <div aria-live="polite" className="grid gap-3">
            {error ? (
              <div className="rounded-2xl border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm leading-6 text-destructive">
                {error.message}
              </div>
            ) : null}
            {isSuccess ? (
              <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/8 px-4 py-3 text-sm leading-6 text-emerald-800">
                Análise enviada com sucesso. O painel ao lado já exibe a categoria, a confiança e a resposta sugerida.
              </div>
            ) : null}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
