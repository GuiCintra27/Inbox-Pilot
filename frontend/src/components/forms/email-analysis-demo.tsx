"use client";

import { useState } from "react";

import { SampleEmails, type SampleEmailExample } from "@/components/examples";
import { AnalysisResultPanel, type AnalysisResult } from "@/components/results";
import type { AnalyzeEmailError, AnalyzeEmailResponse } from "@/lib/email-analysis";

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
    <section>
      <div className="max-w-[720px]">
        <h2 className="font-display text-[clamp(2.5rem,3.4vw,3rem)] font-semibold leading-[1.02] tracking-[-0.05em] text-slate-950">
            Analisar email
        </h2>
        <p className="mt-3 text-[14px] leading-7 text-slate-500">
          Insira o conteúdo do email ou faça o upload de um arquivo.
          <span className="ml-1 text-[#19c8f2]">Prioridade: arquivo &gt; texto ⓘ</span>
        </p>
      </div>

      <div className="mt-10 grid items-start gap-10 xl:grid-cols-[minmax(760px,1fr)_460px] 2xl:grid-cols-[minmax(860px,1fr)_500px] 2xl:gap-14">
        <div className="min-w-0">
          <EmailAnalysisForm
            key={formInstanceKey}
            initialEmailText={prefillText}
            examplesSlot={<SampleEmails onSelectExample={handleExampleSelect} />}
            onResult={handleSuccess}
            onError={handleError}
            onSubmittingChange={setIsSubmitting}
            onInteractionReset={() => setErrorMessage(null)}
            className="border-[#ece9e3] bg-white shadow-none"
          />
        </div>

        <AnalysisResultPanel
          result={analysisResult}
          isLoading={isSubmitting}
          errorMessage={errorMessage}
          className="w-full max-w-[500px] border-0 shadow-[0_40px_80px_-40px_rgba(15,23,42,0.62)] xl:sticky xl:top-6"
        />
      </div>
    </section>
  );
}
