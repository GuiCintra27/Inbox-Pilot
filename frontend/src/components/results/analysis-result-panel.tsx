import { AlertTriangle, Sparkles, Target, Wand2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

import { CopyReplyButton } from "./copy-reply-button";
import type { AnalysisResult } from "./analysis-types";

interface AnalysisResultPanelProps {
  result: AnalysisResult | null;
  isLoading?: boolean;
  errorMessage?: string | null;
  className?: string;
}

function getCategoryTone(category: AnalysisResult["category"]) {
  if (category === "Produtivo") {
    return {
      badge: "border-emerald-500/30 bg-emerald-500/10 text-emerald-700",
      shell: "from-emerald-500/12 via-transparent to-transparent",
      accent: "bg-emerald-500"
    };
  }

  return {
    badge: "border-amber-500/30 bg-amber-500/10 text-amber-700",
    shell: "from-amber-500/12 via-transparent to-transparent",
    accent: "bg-amber-500"
  };
}

function Keywords({ keywords }: { keywords: string[] }) {
  if (keywords.length === 0) {
    return <p className="text-sm text-muted-foreground">Sem palavras-chave identificadas.</p>;
  }

  return (
    <div className="flex flex-wrap gap-2" aria-label="Palavras-chave da análise">
      {keywords.map((keyword) => (
        <Badge key={keyword} variant="secondary" className="rounded-full bg-muted/80 px-3 py-1 text-xs">
          {keyword}
        </Badge>
      ))}
    </div>
  );
}

function EmptyState() {
  return (
    <Card className="border-border/70 bg-card/80 backdrop-blur">
      <CardHeader>
        <CardTitle className="font-display text-2xl tracking-tight">Resultado da análise</CardTitle>
        <CardDescription>
          Envie um email para ver categoria, confiança, justificativa e resposta sugerida em um painel único.
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 sm:grid-cols-3">
        {[
          {
            icon: Target,
            title: "Categoria clara",
            description: "Produtivo ou improdutivo, com leitura rápida do contexto."
          },
          {
            icon: Wand2,
            title: "Resposta sugerida",
            description: "Uma versão pronta para reutilizar ou adaptar."
          },
          {
            icon: Sparkles,
            title: "Detalhe útil",
            description: "Justificativa, confiança e palavras-chave em uma visão só."
          }
        ].map(({ icon: Icon, title, description }) => (
          <div key={title} className="rounded-3xl border border-border/70 bg-background/80 p-5">
            <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-2xl bg-foreground text-background">
              <Icon className="h-5 w-5" />
            </div>
            <h3 className="font-display text-lg tracking-tight">{title}</h3>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">{description}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export function AnalysisResultPanel({ result, isLoading = false, errorMessage = null, className }: AnalysisResultPanelProps) {
  if (errorMessage) {
    return (
      <Card className={cn("border-destructive/30 bg-card/80 backdrop-blur", className)}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 font-display text-2xl tracking-tight text-destructive">
            <AlertTriangle className="h-5 w-5" />
            Não foi possível concluir a análise
          </CardTitle>
          <CardDescription>{errorMessage}</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className={cn("border-border/70 bg-card/80 backdrop-blur", className)}>
        <CardHeader>
          <CardTitle className="font-display text-2xl tracking-tight">Analisando email</CardTitle>
          <CardDescription>Estamos preparando o retorno com categoria, confiança e resposta sugerida.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="h-40 animate-pulse rounded-3xl bg-muted/70" />
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="h-24 animate-pulse rounded-3xl bg-muted/70" />
            <div className="h-24 animate-pulse rounded-3xl bg-muted/70" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!result) {
    return <EmptyState />;
  }

  const tone = getCategoryTone(result.category);
  const confidencePercent = Math.round(result.confidence * 100);

  return (
    <Card className={cn("overflow-hidden border-border/70 bg-card/80 backdrop-blur", className)}>
      <div className={cn("h-1 bg-gradient-to-r", tone.accent)} aria-hidden="true" />
      <CardHeader className={cn("bg-gradient-to-br", tone.shell)}>
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-3">
            <Badge variant="outline" className={cn("w-fit rounded-full border px-3 py-1 text-[11px] uppercase tracking-[0.22em]", tone.badge)}>
              {result.category}
            </Badge>
            <CardTitle className="font-display text-2xl tracking-tight sm:text-3xl">
              O email foi classificado com {confidencePercent}% de confiança.
            </CardTitle>
            <CardDescription className="max-w-2xl text-base leading-7">
              O painel abaixo resume o motivo da decisão e já traz uma resposta sugerida para acelerar a próxima ação.
            </CardDescription>
          </div>
          <div className="min-w-[10rem] rounded-3xl border border-border/70 bg-background/80 p-4 shadow-sm">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Confiança</p>
            <p className="mt-2 font-display text-4xl tracking-tight">{confidencePercent}%</p>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-muted" aria-hidden="true">
              <div className={cn("h-full rounded-full", tone.accent)} style={{ width: `${confidencePercent}%` }} />
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="grid gap-6 pt-6">
        <section className="space-y-3 rounded-3xl border border-border/70 bg-background/80 p-5">
          <h3 className="font-display text-lg tracking-tight">Justificativa</h3>
          <p className="text-sm leading-7 text-muted-foreground">{result.rationale}</p>
        </section>

        <section className="space-y-4 rounded-3xl border border-border/70 bg-background/80 p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h3 className="font-display text-lg tracking-tight">Resposta sugerida</h3>
              <p className="text-sm text-muted-foreground">
                Use a resposta como ponto de partida para o próximo contato.
              </p>
            </div>
            <CopyReplyButton text={result.suggestedReply} />
          </div>
          <Separator />
          <p className="text-sm leading-7 text-foreground">{result.suggestedReply}</p>
        </section>

        <section className="space-y-3 rounded-3xl border border-border/70 bg-background/80 p-5">
          <h3 className="font-display text-lg tracking-tight">Palavras-chave</h3>
          <Keywords keywords={result.keywords} />
        </section>

        <div className="flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.22em] text-muted-foreground">
          <span>Provider</span>
          <span aria-hidden="true">•</span>
          <span>{result.provider}</span>
        </div>
      </CardContent>
    </Card>
  );
}
