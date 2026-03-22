import {
  AlertTriangle,
  Layers3,
  Sparkles,
  Target
} from "lucide-react";

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

function getCategoryBadgeClass(category: AnalysisResult["category"]) {
  return category === "Produtivo"
    ? "bg-[#12213b] text-white"
    : "bg-[#3c2413] text-white";
}

function describeProvider(provider: string) {
  const [channel, ...rest] = provider.split(":");
  const model = rest.join(":") || "desconhecido";

  if (channel === "gemini") {
    return { title: "Provider & Modelo", label: model, tag: "provider principal" };
  }

  if (channel === "openrouter") {
    return { title: "Provider & Modelo", label: model, tag: "fallback externo" };
  }

  return { title: "Provider & Modelo", label: "Fallback local", tag: model };
}

function EmptyState() {
  return (
    <Card className="overflow-hidden rounded-[16px] bg-[#07091d] text-white">
      <div className="h-1 w-full bg-[linear-gradient(90deg,#16c8f2_0%,#8b5cf6_55%,#d49b58_100%)]" />
      <CardHeader className="px-5 pb-4 pt-5">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-[12px] font-semibold text-white">Produtivo</p>
          </div>
          <div className="text-right">
            <p className="font-display text-[42px] font-semibold leading-none">98%</p>
            <p className="mt-1 text-[9px] uppercase tracking-[0.25em] text-white/55">
              Confiança da IA
            </p>
          </div>
        </div>
        <div className="mt-5 h-[4px] rounded-full bg-[#12c8f2]" />
        <div className="mt-2 flex justify-between text-[8px] uppercase tracking-[0.22em] text-white/35">
          <span>Incerteza</span>
          <span>Análise concluída</span>
        </div>
      </CardHeader>
      <CardContent className="space-y-4 px-5 pb-5">
        <div className="grid gap-4">
          {[
            {
              icon: Target,
              title: "Categoria",
              description: "Classificação imediata da mensagem."
            },
            {
              icon: Sparkles,
              title: "Resposta sugerida",
              description: "Uma versão pronta para adaptação."
            },
            {
              icon: Layers3,
              title: "Detalhe útil",
              description: "Justificativa, confiança e palavras-chave em um só lugar."
            }
          ].map(({ icon: Icon, title, description }) => (
            <div
              key={title}
              className="rounded-[14px] border border-white/12 bg-white/[0.04] px-4 py-5"
            >
              <div className="flex h-11 w-11 items-center justify-center rounded-[14px] bg-white/10 text-white">
                <Icon className="h-5 w-5" />
              </div>
              <h3 className="mt-5 font-display text-[16px] font-medium text-white">{title}</h3>
              <p className="mt-3 text-[12px] leading-7 text-white/62">{description}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export function AnalysisResultPanel({
  result,
  isLoading = false,
  errorMessage = null,
  className
}: AnalysisResultPanelProps) {
  if (errorMessage) {
    return (
      <Card
        className={cn(
          "overflow-hidden rounded-[16px] bg-[#120e1d] text-white",
          className
        )}
      >
          <CardHeader className="px-5 pb-4 pt-5">
            <CardTitle className="flex items-center gap-2 font-display text-[28px] text-red-200">
              <AlertTriangle className="h-5 w-5" />
              Não foi possível analisar
            </CardTitle>
            <CardDescription className="mt-3 text-[13px] leading-7 text-white/65">
              {errorMessage}
            </CardDescription>
            <p className="text-[12px] leading-6 text-white/45">
              Revise o conteúdo, o tipo do arquivo ou aguarde alguns instantes antes de tentar de
              novo.
            </p>
          </CardHeader>
        </Card>
      );
  }

  if (isLoading) {
    return (
      <Card className={cn("overflow-hidden rounded-[16px] bg-[#07091d] text-white", className)}>
        <div className="h-1 w-full bg-[linear-gradient(90deg,#16c8f2_0%,#8b5cf6_55%,#d49b58_100%)]" />
        <CardHeader className="px-5 pb-4 pt-5">
          <div className="flex items-start justify-between">
            <div className="h-4 w-16 animate-pulse rounded-full bg-white/10" />
            <div className="space-y-2">
              <div className="ml-auto h-8 w-16 animate-pulse rounded-xl bg-white/10" />
              <div className="h-2 w-20 animate-pulse rounded-full bg-white/10" />
            </div>
          </div>
          <div className="mt-5 h-[4px] rounded-full bg-white/10" />
        </CardHeader>
        <CardContent className="space-y-4 px-5 pb-5">
          <div className="h-[46px] animate-pulse rounded-[14px] bg-white/10" />
          <div className="h-[120px] animate-pulse rounded-[14px] bg-white/10" />
          <div className="h-[110px] animate-pulse rounded-[14px] bg-white/10" />
          <div className="h-[78px] animate-pulse rounded-[14px] bg-white/10" />
        </CardContent>
      </Card>
    );
  }

  if (!result) {
    return <EmptyState />;
  }

  const confidencePercent = Math.round(result.confidence * 100);
  const provider = describeProvider(result.provider);

  return (
    <Card className={cn("overflow-hidden rounded-[16px] bg-[#07091d] text-white", className)}>
      <div className="h-1 w-full bg-[linear-gradient(90deg,#16c8f2_0%,#8b5cf6_55%,#d49b58_100%)]" />
      <CardHeader className="px-5 pb-4 pt-5">
        <div className="flex items-start justify-between">
          <div>
            <Badge
              className={cn(
                "rounded-full border-0 px-3 py-1 text-[11px] font-semibold",
                getCategoryBadgeClass(result.category)
              )}
            >
              {result.category}
            </Badge>
          </div>
          <div className="text-right">
            <p className="font-display text-[42px] font-semibold leading-none">{confidencePercent}%</p>
            <p className="mt-1 text-[9px] uppercase tracking-[0.25em] text-white/55">
              Confiança da IA
            </p>
          </div>
        </div>
        <div className="mt-5 h-[4px] rounded-full bg-[#12c8f2]" />
        <div className="mt-2 flex justify-between text-[8px] uppercase tracking-[0.22em] text-white/35">
          <span>Incerteza</span>
          <span>Análise concluída</span>
        </div>
      </CardHeader>

      <CardContent className="space-y-4 px-5 pb-5">
        <section className="rounded-[14px] border border-white/10 bg-white/[0.04] px-4 py-3.5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#e8d4b7] text-[#6a4a24]">
              <Sparkles className="h-4 w-4" />
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-[0.16em] text-white/48">{provider.title}</p>
              <p className="mt-1 text-[12px] font-medium text-white">{provider.label}</p>
              <p className="mt-1 text-[9px] text-white/45">{provider.tag}</p>
            </div>
          </div>
        </section>

        <section>
          <div className="mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[#16c8f2]" />
            <p className="text-[10px] uppercase tracking-[0.22em] text-white/45">Justificativa</p>
          </div>
          <div className="rounded-[14px] border border-[#b789f6]/70 bg-transparent px-4 py-3 text-[12px] leading-6 text-white/80">
            {result.rationale}
          </div>
        </section>

        <section>
          <div className="mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[#8b5cf6]" />
            <p className="text-[10px] uppercase tracking-[0.22em] text-white/45">Resposta sugerida</p>
          </div>
          <div className="rounded-[14px] border border-white/10 bg-white/[0.04] px-4 py-3 text-[12px] italic leading-7 text-white/82">
            “{result.suggestedReply}”
          </div>
        </section>

        <section>
          <p className="mb-3 text-[10px] uppercase tracking-[0.22em] text-white/45">
            Palavras-chave extraídas
          </p>
          <div className="flex flex-wrap gap-2">
            {result.keywords.map((keyword) => (
              <span
                key={keyword}
                className="rounded-full border border-white/10 bg-white/[0.05] px-3 py-1 text-[10px] text-white/78"
              >
                {keyword}
              </span>
            ))}
          </div>
        </section>

        <Separator className="bg-white/10" />

        <div className="flex items-center justify-between gap-4">
          <button
            type="button"
            className="rounded-full bg-white px-5 py-2 text-[12px] font-medium text-slate-950 transition-colors hover:bg-white/90"
          >
            Ver leitura completa
          </button>
          <div className="flex items-center gap-3">
            <CopyReplyButton
              text={result.suggestedReply}
              label=""
              copiedLabel=""
              className="gap-0"
              buttonClassName="h-8 w-8 rounded-md border-white/10 bg-transparent px-0 text-white hover:bg-white/10"
              hintClassName="hidden"
            />
            <button type="button" className="text-[10px] text-white/35">
              Baixar JSON
            </button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
