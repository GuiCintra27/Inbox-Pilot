import {
  ArrowRight,
  BadgeCheck,
  CircleGauge,
  FileText,
  MailQuestion,
  Sparkles,
  Workflow
} from "lucide-react";

import { EmailAnalysisDemo } from "@/components/forms/email-analysis-demo";
import { ProductSnapshot } from "@/components/marketing/product-snapshot";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

const principles = [
  {
    icon: MailQuestion,
    title: "Entrada sem fricção",
    description: "Texto livre e arquivo convivem no mesmo fluxo sem aumentar a complexidade."
  },
  {
    icon: CircleGauge,
    title: "Leitura imediata",
    description: "Categoria, confiança e justificativa aparecem com hierarquia visual forte."
  },
  {
    icon: Workflow,
    title: "Pronto para operação",
    description: "A resposta sugerida já entra na jornada como próximo passo acionável."
  }
];

const productSignals = [
  "Fluxo único entre entrada, análise e saída",
  "Estados claros de loading, erro e sucesso",
  "Upload e texto livre no mesmo contrato",
  "Demo pronta para uso em desktop e mobile"
];

const trustNotes = [
  "O backend aceita `email_text`, `email_file` ou ambos no mesmo envio.",
  "A resposta traz categoria, confiança, justificativa, keywords e sugestão de resposta.",
  "A experiência visual foi pensada para parecer produto, não dashboard genérico."
];

export default function HomePage() {
  return (
    <main className="relative isolate min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-amber-300/25 blur-3xl" />
        <div className="absolute right-0 top-24 h-80 w-80 rounded-full bg-slate-400/20 blur-3xl" />
        <div className="absolute bottom-10 left-1/3 h-64 w-64 rounded-full bg-stone-300/40 blur-3xl" />
      </div>

      <div className="relative mx-auto flex w-full max-w-7xl flex-col px-4 py-5 sm:px-6 lg:px-8 lg:py-6">
        <header className="flex items-center justify-between gap-4 border-b border-border/60 pb-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-border/70 bg-background/85 shadow-sm">
              <FileText className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.26em] text-muted-foreground">Inbox Pilot</p>
              <p className="font-display text-lg tracking-tight">triagem de emails operacionais</p>
            </div>
          </div>
          <div className="hidden items-center gap-2 md:flex">
            <Badge
              variant="outline"
              className="rounded-full px-3 py-1 text-[11px] uppercase tracking-[0.2em]"
            >
              Product demo
            </Badge>
            <Badge
              variant="secondary"
              className="rounded-full px-3 py-1 text-[11px] uppercase tracking-[0.2em]"
            >
              Frontend live
            </Badge>
          </div>
        </header>

        <section className="grid gap-8 pb-8 pt-10 lg:grid-cols-[1.02fr_0.98fr] lg:items-start lg:gap-10 lg:pt-12">
          <div className="space-y-8">
            <div className="space-y-6">
              <Badge
                variant="outline"
                className="w-fit rounded-full border-border/70 bg-background/80 px-4 py-1.5 text-[10px] uppercase tracking-[0.3em] text-muted-foreground"
              >
                Product demo
              </Badge>
              <div className="space-y-4">
                <h1 className="max-w-3xl font-display text-5xl leading-[0.92] tracking-tight text-balance sm:text-6xl lg:text-7xl">
                  A triagem de email pode parecer produto desde a primeira tela.
                </h1>
                <p className="max-w-2xl text-lg leading-8 text-muted-foreground sm:text-xl">
                  Inbox Pilot mostra a jornada completa em uma interface única: entrada simples,
                  leitura imediata do resultado e uma resposta sugerida pronta para acelerar a
                  operação.
                </p>
              </div>
              <div className="flex flex-wrap gap-3">
                <Button asChild className="rounded-full px-6">
                  <a href="#demo">
                    Explorar a experiência
                    <ArrowRight className="h-4 w-4" />
                  </a>
                </Button>
                <Button asChild variant="outline" className="rounded-full px-6">
                  <a href="#panorama">Ver o panorama do produto</a>
                </Button>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {principles.map(({ icon: Icon, title, description }) => (
                <Card key={title} className="border-border/70 bg-card/85 backdrop-blur">
                  <CardContent className="space-y-4 p-5">
                    <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-foreground text-background">
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="space-y-2">
                      <h2 className="font-display text-lg tracking-tight">{title}</h2>
                      <p className="text-sm leading-6 text-muted-foreground">{description}</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          <div id="panorama" className="lg:pt-2">
            <ProductSnapshot />
          </div>
        </section>

        <section id="demo" className="pb-8">
          <EmailAnalysisDemo />
        </section>

        <section className="grid gap-6 pb-10 lg:grid-cols-[1.1fr_0.9fr]">
          <Card className="border-border/70 bg-card/85 backdrop-blur">
            <CardHeader className="gap-3">
              <CardTitle className="font-display text-2xl tracking-tight sm:text-3xl">
                O que esta interface já comunica
              </CardTitle>
              <CardDescription className="max-w-2xl text-base leading-7">
                O fluxo está organizado para mostrar valor em poucos segundos, sem depender de
                documentação externa ou de leitura técnica do backend.
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 sm:grid-cols-2">
              {productSignals.map((signal) => (
                <div
                  key={signal}
                  className="flex items-center gap-3 rounded-2xl border border-border/70 bg-background/80 p-4"
                >
                  <BadgeCheck className="h-5 w-5 text-foreground/80" />
                  <span className="text-sm leading-6 text-foreground">{signal}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="border-border/70 bg-card/85 backdrop-blur">
            <CardHeader className="gap-3">
              <CardTitle className="font-display text-2xl tracking-tight sm:text-3xl">
                Leitura rápida para a demo
              </CardTitle>
              <CardDescription className="text-base leading-7">
                A tela foi desenhada para fazer a transição entre problema, demonstração e
                resultado sem quebrar ritmo.
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3">
              {trustNotes.map((note) => (
                <div
                  key={note}
                  className="flex items-start gap-3 rounded-2xl border border-border/70 bg-background/80 p-4"
                >
                  <Sparkles className="mt-0.5 h-5 w-5 text-foreground/75" />
                  <span className="text-sm leading-6 text-foreground">{note}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </section>

        <section className="pb-6">
          <Card className="border-border/70 bg-card/85 backdrop-blur">
            <CardHeader className="gap-3">
              <CardTitle className="font-display text-2xl tracking-tight sm:text-3xl">
                Jornada do produto
              </CardTitle>
              <CardDescription className="max-w-3xl text-base leading-7">
                Entrada, processamento e resultado continuam legíveis mesmo em telas menores, sem
                virar uma sequência de blocos genéricos.
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4 sm:grid-cols-[1fr_auto_1fr_auto_1fr] sm:items-center">
              <div className="rounded-3xl border border-border/70 bg-background/80 p-5">
                <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Entrada</p>
                <p className="mt-2 text-sm leading-6 text-foreground">
                  Texto livre, upload e exemplos prontos na mesma interface.
                </p>
              </div>
              <Separator orientation="vertical" className="hidden h-16 sm:block" />
              <div className="rounded-3xl border border-border/70 bg-background/80 p-5">
                <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">
                  Processamento
                </p>
                <p className="mt-2 text-sm leading-6 text-foreground">
                  O backend responde com contrato estável e tratamento claro de falhas.
                </p>
              </div>
              <Separator orientation="vertical" className="hidden h-16 sm:block" />
              <div className="rounded-3xl border border-border/70 bg-background/80 p-5">
                <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Resultado</p>
                <p className="mt-2 text-sm leading-6 text-foreground">
                  Categoria, confiança, justificativa, keywords e resposta sugerida.
                </p>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </main>
  );
}
