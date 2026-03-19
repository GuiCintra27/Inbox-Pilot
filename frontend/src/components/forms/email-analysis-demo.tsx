"use client";

import { useState } from "react";

import { SampleEmails, type SampleEmailExample } from "@/components/examples";
import {
  AnalysisResultPanel,
  type AnalysisResult
} from "@/components/results";
import type {
  AnalyzeEmailError,
  AnalyzeEmailResponse
} from "@/lib/email-analysis";

import { EmailAnalysisForm } from "./email-analysis-form";

function toResultModel(result: AnalyzeEmailResponse): AnalysisResult {
  return {
    category: result.category,
    confidence: result.confidence,
    rationale: result.rationale,
    suggestedReply: result.suggested_reply,
    keywords: result.keywords,
    provider: result.provider
  };
}

export function EmailAnalysisDemo() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [prefillText, setPrefillText] = useState("");
  const [formInstanceKey, setFormInstanceKey] = useState(0);

  function handleExampleSelect(example: SampleEmailExample) {
    const nextText = `Subject: ${example.subject}\n\n${example.body}`;

    setPrefillText(nextText);
    setAnalysisResult(null);
    setErrorMessage(null);
    setFormInstanceKey((current) => current + 1);
  }

  function handleSuccess(result: AnalyzeEmailResponse) {
    setAnalysisResult(toResultModel(result));
    setErrorMessage(null);
  }

  function handleError(error: AnalyzeEmailError) {
    setAnalysisResult(null);
    setErrorMessage(error.message);
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[1.02fr_0.98fr]">
      <div className="grid gap-6">
        <EmailAnalysisForm
          key={formInstanceKey}
          initialEmailText={prefillText}
          onResult={handleSuccess}
          onError={handleError}
          onSubmittingChange={setIsSubmitting}
          className="border-white/70 bg-white/75 shadow-[0_35px_90px_-48px_rgba(15,23,42,0.28)] backdrop-blur"
        />
        <SampleEmails
          onSelectExample={handleExampleSelect}
          className="border-white/70 bg-white/75 shadow-[0_35px_90px_-48px_rgba(15,23,42,0.28)] backdrop-blur"
        />
      </div>

      <AnalysisResultPanel
        result={analysisResult}
        isLoading={isSubmitting}
        errorMessage={errorMessage}
        className="border-slate-900/15 bg-white/72 shadow-[0_35px_90px_-48px_rgba(15,23,42,0.3)] backdrop-blur"
      />
    </div>
  );
}
