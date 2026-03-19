"use client";

import { useState } from "react";

import {
  AnalyzeEmailError,
  analyzeEmail,
  type AnalyzeEmailRequest,
  type AnalyzeEmailResponse
} from "@/lib/email-analysis";

export interface UseEmailAnalysisOptions {
  baseUrl?: string;
  onSuccess?: (result: AnalyzeEmailResponse) => void;
  onError?: (error: AnalyzeEmailError) => void;
}

export function useEmailAnalysis(options: UseEmailAnalysisOptions = {}) {
  const [result, setResult] = useState<AnalyzeEmailResponse | null>(null);
  const [error, setError] = useState<AnalyzeEmailError | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const reset = () => {
    setResult(null);
    setError(null);
  };

  const clearError = () => setError(null);
  const clearResult = () => setResult(null);

  const submit = async (input: AnalyzeEmailRequest) => {
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await analyzeEmail(input, { baseUrl: options.baseUrl });
      setResult(response);
      options.onSuccess?.(response);
      return response;
    } catch (cause) {
      const normalized =
        cause instanceof AnalyzeEmailError
          ? cause
          : new AnalyzeEmailError("Falha inesperada ao analisar o email.", 500);

      setError(normalized);
      options.onError?.(normalized);
      throw normalized;
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    analyze: submit,
    clearError,
    clearResult,
    error,
    isSubmitting,
    reset,
    result
  };
}
