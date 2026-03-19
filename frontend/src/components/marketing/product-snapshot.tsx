import { ArrowRight, Sparkles, Upload, Wand2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

const intakeSteps = [
  "Cole o email ou envie um arquivo",
  "O backend classifica o conteúdo",
  "A interface mostra contexto e resposta sugerida"
];

const signalRows = [
  { label: "Categoria", value: "Produtivo" },
  { label: "Confiança", value: "95%" },
  { label: "Provider", value: "gemini:gemini-2.5-flash" }
];

export function ProductSnapshot() {
  return (
    <Card className="relative overflow-hidden border-border/70 bg-card/85 shadow-[0_30px_80px_-40px_rgba(15,23,42,0.45)] backdrop-blur">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.5),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(245,158,11,0.12),transparent_32%)]" />
      <CardHeader className="relative gap-4 pb-0 pt-7 sm:pt-8">
        <div className="flex items-center justify-between gap-3">
          <Badge
            variant="outline"
            className="rounded-full border-border/70 bg-background/80 px-3 py-1 text-[10px] uppercase tracking-[0.28em] text-muted-foreground"
          >
            Produto
          </Badge>
          <span className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
            Inbox Pilot
          </span>
        </div>
        <CardTitle className="max-w-xl font-display text-3xl leading-[0.96] tracking-tight sm:text-4xl">
          Uma superfície clara para triagem de emails operacionais.
        </CardTitle>
        <CardDescription className="max-w-xl text-base leading-7 text-muted-foreground">
          O fluxo abaixo representa a experiência final da demo: entrada, processamento e
          leitura do resultado em um único espaço.
        </CardDescription>
      </CardHeader>
      <CardContent className="relative grid gap-4 pt-6 sm:grid-cols-[1.05fr_0.95fr]">
        <div className="rounded-[1.75rem] border border-dashed border-border/80 bg-background/70 p-5">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">
                Entrada do email
              </p>
              <p className="mt-1 text-sm font-medium text-foreground">
                Texto livre, upload e exemplos prontos no mesmo fluxo
              </p>
            </div>
            <Button variant="outline" size="sm" className="pointer-events-none gap-2">
              <Upload className="h-4 w-4" />
              Fluxo validado
            </Button>
          </div>
          <div className="grid gap-3">
            {intakeSteps.map((step, index) => (
              <div
                key={step}
                className="flex items-center gap-3 rounded-2xl border border-border/70 bg-background/85 p-4"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-foreground text-background">
                  <span className="text-xs font-semibold">{index + 1}</span>
                </div>
                <p className="text-sm leading-6 text-foreground">{step}</p>
              </div>
            ))}
          </div>
          <Separator className="my-5" />
          <div className="flex flex-wrap gap-2">
            <Badge variant="secondary" className="rounded-full px-3 py-1">
              texto livre
            </Badge>
            <Badge variant="secondary" className="rounded-full px-3 py-1">
              upload .txt
            </Badge>
            <Badge variant="secondary" className="rounded-full px-3 py-1">
              upload .pdf
            </Badge>
          </div>
        </div>

        <div className="rounded-[1.75rem] border border-border/70 bg-[linear-gradient(180deg,rgba(15,23,42,0.95),rgba(15,23,42,0.88))] p-5 text-background shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-background/60">
                Resultado
              </p>
              <p className="mt-1 text-sm font-medium text-background">
                Painel com categoria, confiança e resposta sugerida
              </p>
            </div>
            <div className="rounded-full border border-background/15 bg-background/10 p-2">
              <Wand2 className="h-4 w-4 text-amber-200" />
            </div>
          </div>
          <div className="mt-5 grid gap-3">
            {signalRows.map((row) => (
              <div key={row.label} className="rounded-2xl border border-background/10 bg-background/5 p-4">
                <p className="text-[11px] uppercase tracking-[0.22em] text-background/50">{row.label}</p>
                <p className="mt-1 text-sm font-medium text-background">{row.value}</p>
              </div>
            ))}
          </div>
          <div className="mt-5 rounded-3xl border border-background/10 bg-background/5 p-4">
            <div className="flex items-center gap-2 text-sm font-medium text-background">
              <Sparkles className="h-4 w-4 text-amber-200" />
              Pronto para a análise em tempo real
            </div>
            <p className="mt-2 text-sm leading-6 text-background/75">
              A leitura final combina justificativa, resposta sugerida e keywords em uma única
              superfície para acelerar a próxima ação.
            </p>
          </div>
          <Button className="mt-5 w-full rounded-full bg-background text-foreground hover:bg-background/90">
            Ver a leitura completa
            <ArrowRight className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
