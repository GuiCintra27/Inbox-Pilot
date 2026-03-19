import { ArrowRight, Mail } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

import type { AnalysisCategory } from "../results";

export interface SampleEmailExample {
  id: string;
  title: string;
  subject: string;
  body: string;
  category: AnalysisCategory;
  hint: string;
}

export const sampleEmailExamples: SampleEmailExample[] = [
  {
    id: "invoice-review",
    title: "Aprovação operacional",
    subject: "Invoice pending approval",
    body:
      "Hello team, please confirm whether the invoice can be approved today. The supplier needs a status update.",
    category: "Produtivo",
    hint: "Bom para testar o fluxo de triagem operacional."
  },
  {
    id: "holiday-note",
    title: "Mensagem social",
    subject: "Seasonal greetings",
    body:
      "Thanks for everything this quarter. Wishing you and the team a great holiday season and a happy new year.",
    category: "Improdutivo",
    hint: "Mostra um caso sem necessidade de ação imediata."
  },
  {
    id: "status-request",
    title: "Status de suporte",
    subject: "Need an update on the ticket",
    body:
      "Olá, poderia me enviar uma atualização sobre o ticket aberto? Precisamos confirmar o prazo hoje.",
    category: "Produtivo",
    hint: "Útil para demonstrar texto em português e inglês no mesmo produto."
  }
];

interface SampleEmailsProps {
  onSelectExample?: (example: SampleEmailExample) => void;
  className?: string;
}

function getCategoryTone(category: AnalysisCategory) {
  return category === "Produtivo"
    ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-700"
    : "border-amber-500/30 bg-amber-500/10 text-amber-700";
}

export function SampleEmails({ onSelectExample, className }: SampleEmailsProps) {
  return (
    <Card className={cn("border-border/70 bg-card/80 backdrop-blur", className)}>
      <CardHeader>
        <CardTitle className="font-display text-2xl tracking-tight">Exemplos prontos</CardTitle>
        <CardDescription>
          Use um dos exemplos abaixo para mostrar a triagem sem precisar preparar um email do zero.
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        {sampleEmailExamples.map((example) => (
          <article key={example.id} className="rounded-3xl border border-border/70 bg-background/80 p-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Mail className="h-4 w-4" />
                  <span>{example.subject}</span>
                </div>
                <h3 className="font-display text-lg tracking-tight">{example.title}</h3>
              </div>
              <Badge variant="outline" className={cn("rounded-full border px-3 py-1 text-[11px] uppercase tracking-[0.22em]", getCategoryTone(example.category))}>
                {example.category}
              </Badge>
            </div>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">{example.hint}</p>
            <p className="mt-4 text-sm leading-6 text-foreground">{example.body}</p>
            <div className="mt-4 flex items-center justify-between gap-3">
              <span className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Pronto para testar</span>
              <Button
                type="button"
                variant="outline"
                className="rounded-full"
                onClick={() => onSelectExample?.(example)}
                disabled={!onSelectExample}
              >
                <span>Usar exemplo</span>
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </article>
        ))}
      </CardContent>
    </Card>
  );
}
