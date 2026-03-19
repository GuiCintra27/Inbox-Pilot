import { CircleCheckBig, FileText, Layers3, Sparkles, Zap } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

const pillars = [
  {
    icon: FileText,
    title: "Entrada simples",
    description: "A fundação já prepara texto livre e upload de arquivo para o fluxo principal."
  },
  {
    icon: Layers3,
    title: "Arquitetura separada",
    description: "Frontend e backend ficam desacoplados desde o começo para facilitar evolução e deploy."
  },
  {
    icon: Sparkles,
    title: "Base pronta para demo",
    description: "A interface nasce com espaço para uma apresentação forte sem comprometer a clareza."
  }
];

const checklist = [
  "Next.js App Router com TypeScript",
  "Tailwind configurado com tokens de design",
  "Componentes base em estilo shadcn/ui",
  "Estrutura pronta para expansão da Fase 2"
];

export default function HomePage() {
  return (
    <main className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
      <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr] lg:gap-8">
        <Card className="relative overflow-hidden border-border/70 bg-card/80 backdrop-blur">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(99,102,241,0.12),transparent_24%),radial-gradient(circle_at_top_right,rgba(245,158,11,0.12),transparent_24%)]" />
          <CardHeader className="relative gap-4 pb-0 pt-8 sm:pt-10">
            <Badge variant="outline" className="w-fit rounded-full border-border/70 bg-background/80 px-3 py-1 text-[11px] uppercase tracking-[0.24em] text-muted-foreground">
              Foundation
            </Badge>
            <CardTitle className="max-w-3xl font-display text-4xl leading-[0.95] tracking-tight sm:text-5xl lg:text-6xl">
              Email Bot Automation
            </CardTitle>
            <CardDescription className="max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
              Base de frontend para o case de triagem de emails, preparada para texto livre, upload de arquivo e a
              demo visual da solução.
            </CardDescription>
          </CardHeader>
          <CardContent className="relative mt-8 grid gap-4 sm:grid-cols-3">
            {pillars.map(({ icon: Icon, title, description }) => (
              <div key={title} className="rounded-3xl border border-border/70 bg-background/70 p-5 shadow-sm">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-2xl bg-foreground text-background">
                  <Icon className="h-5 w-5" />
                </div>
                <h2 className="mb-2 font-display text-lg tracking-tight">{title}</h2>
                <p className="text-sm leading-6 text-muted-foreground">{description}</p>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="border-border/70 bg-card/80 backdrop-blur">
          <CardHeader>
            <CardTitle className="font-display text-2xl tracking-tight">Estado desta fase</CardTitle>
            <CardDescription>
              Layout neutro, base de design e estrutura do projeto, sem a UI final da demo.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            {checklist.map((item) => (
              <div key={item} className="flex items-start gap-3 rounded-2xl border border-border/70 bg-background/70 p-4">
                <CircleCheckBig className="mt-0.5 h-5 w-5 text-foreground/80" />
                <span className="text-sm leading-6 text-foreground">{item}</span>
              </div>
            ))}
            <Separator className="my-2" />
            <div className="grid gap-3">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Zap className="h-4 w-4" />
                <span>Pronto para conectar ao backend na próxima fase.</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="inline-flex h-2 w-2 rounded-full bg-foreground" />
                <span>Sem POST /analyze, sem parsing e sem dependências de AI ainda.</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      <section className="mt-6 grid gap-6 lg:grid-cols-3">
        <Card className="border-border/70 bg-card/80 backdrop-blur lg:col-span-2">
          <CardHeader>
            <CardTitle className="font-display text-2xl tracking-tight">Conexão do projeto</CardTitle>
            <CardDescription>
              A base do frontend já conversa com a arquitetura documentada e deixa a próxima fase sem ambiguidade.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-3xl border border-border/70 bg-background/80 p-5">
              <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Stack-alvo</p>
              <p className="mt-2 text-sm leading-6 text-foreground">
                Next.js App Router, TypeScript, Tailwind e componentes em estilo shadcn/ui.
              </p>
            </div>
            <div className="rounded-3xl border border-border/70 bg-background/80 p-5">
              <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Próxima integração</p>
              <p className="mt-2 text-sm leading-6 text-foreground">
                Upload e texto livre vão consumir a API FastAPI na Fase 2 e Fase 3.
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/70 bg-card/80 backdrop-blur">
          <CardHeader>
            <CardTitle className="font-display text-2xl tracking-tight">Navegação</CardTitle>
            <CardDescription>Documentação e estrutura do case.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <Button className="rounded-full" type="button">
              Base pronta para a Fase 2
            </Button>
            <p className="text-sm leading-6 text-muted-foreground">
              Esta fase deixa a fundação criada sem antecipar a experiência final da demo.
            </p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}
