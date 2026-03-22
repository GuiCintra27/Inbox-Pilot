import Image from "next/image";
import {
  ArrowRight,
  Layers3,
  Mail,
  Shield,
  Sparkles,
  SquareMousePointer,
  Zap
} from "lucide-react";

import { EmailAnalysisDemo } from "@/components/forms/email-analysis-demo";
import { ProductSnapshot } from "@/components/marketing/product-snapshot";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const heroHighlights = [
  {
    icon: SquareMousePointer,
    title: "Entrada sem fricção"
  },
  {
    icon: Layers3,
    title: "Leitura imediata de IA"
  },
  {
    icon: Zap,
    title: "Pronto para operação"
  }
];

const workflowSteps = [
  {
    icon: Mail,
    step: "Passo 01",
    title: "Recebemos o email",
    description:
      "Nossa engine captura o conteúdo bruto do email ou extrai o texto de documentos anexados com OCR avançado."
  },
  {
    icon: Sparkles,
    step: "Passo 02",
    title: "Interpretamos e classificamos",
    description:
      "Usando a camada de IA, identificamos a intenção, o tom de voz e a prioridade operacional de cada mensagem."
  },
  {
    icon: ArrowRight,
    step: "Passo 03",
    title: "Sugerimos próxima ação",
    description:
      "Você recebe uma classificação imediata e uma sugestão de resposta pronta para ser enviada."
  }
];

const trustTechnologies = [
  {
    icon: Shield,
    label: "Enterprise Grade"
  },
  {
    icon: Layers3,
    label: "Multi-LLM Support"
  },
  {
    icon: Zap,
    label: "Ultra-Fast Response"
  }
];

const footerLinks = ["Termos", "Privacidade", "Suporte"];

export default function HomePage() {
  return (
    <main className="bg-[#f7f7f5] text-slate-950">
      <div className="mx-auto max-w-[1440px] px-3 pb-10 pt-3 sm:px-4">
        <div className="overflow-hidden rounded-[6px] border border-[#e7e6e1] bg-white shadow-[0_30px_100px_-60px_rgba(15,23,42,0.18)]">
          <div className="relative overflow-hidden">
            <div className="pointer-events-none absolute inset-0">
              <div className="absolute left-[-140px] top-10 h-[520px] w-[520px] rounded-full bg-[radial-gradient(circle,rgba(125,241,255,0.42)_0%,rgba(125,241,255,0)_68%)]" />
              <div className="absolute right-[-140px] top-6 h-[620px] w-[620px] rounded-full bg-[radial-gradient(circle,rgba(241,189,255,0.34)_0%,rgba(241,189,255,0)_66%)]" />
              <div className="absolute left-1/2 top-0 h-[540px] w-[540px] -translate-x-1/2 rounded-full bg-[radial-gradient(circle,rgba(233,241,255,0.9)_0%,rgba(233,241,255,0)_70%)]" />
            </div>

            <div className="relative mx-auto max-w-[1220px] px-8 pb-12 pt-5">
              <header className="flex items-center justify-between border-b border-[#f0efea] pb-4">
                <a href="#" className="inline-flex items-center gap-3">
                  <Image
                    src="/logo.webp"
                    alt="Inbox Pilot"
                    width={132}
                    height={32}
                    className="h-8 w-auto"
                    priority
                  />
                </a>
                <nav className="hidden items-center gap-8 text-[11px] font-medium text-slate-700 md:flex">
                  <a href="#how-it-works" className="transition-colors hover:text-slate-950">
                    Como funciona
                  </a>
                  <a href="#pricing" className="transition-colors hover:text-slate-950">
                    Preços
                  </a>
                  <a href="#enterprise" className="transition-colors hover:text-slate-950">
                    Enterprise
                  </a>
                  <a
                    href="#signin"
                    className="rounded-full border border-[#e5e2dc] px-4 py-2 text-slate-900 transition-colors hover:bg-slate-50"
                  >
                    Entrar
                  </a>
                  <a
                    href="#demo"
                    className="rounded-full bg-[#19c8f2] px-4 py-2 text-white shadow-[0_12px_24px_-14px_rgba(25,200,242,0.9)] transition-opacity hover:opacity-95"
                  >
                    Testar Agora
                  </a>
                </nav>
              </header>

              <section className="grid items-center gap-16 pb-11 pt-16 lg:grid-cols-[1.05fr_0.95fr]">
                <div className="max-w-[530px]">
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#bfeffc] bg-white/72 px-4 py-2 text-[10px] font-medium uppercase tracking-[0.22em] text-[#00aee6]">
                    <Sparkles className="h-3 w-3" />
                    Nova Versão 2.5 disponível
                  </div>

                  <h1 className="mt-8 font-display text-[68px] font-semibold leading-[0.93] tracking-[-0.06em] text-slate-950">
                    Analisar emails
                    <br />
                    operacionais
                    <br />
                    <span className="bg-[linear-gradient(90deg,#18c6f2_0%,#36c1e7_18%,#8a7ce4_52%,#d38f49_100%)] bg-clip-text text-transparent">
                      rápido e confiável
                    </span>
                  </h1>

                  <p className="mt-8 max-w-[520px] text-[15px] leading-8 text-slate-600">
                    Cole, envie ou teste um exemplo. Resultado imediato com categoria, confiança e
                    resposta sugerida baseada em inteligência contextual.
                  </p>

                  <div className="mt-8 flex items-center gap-4">
                    <Button
                      asChild
                      className="h-[44px] rounded-full border-0 bg-[#19c8f2] px-7 text-[14px] font-medium text-white shadow-[0_20px_35px_-18px_rgba(25,200,242,0.95)] hover:bg-[#17bce4]"
                    >
                      <a href="#demo">
                        Analisar email
                        <ArrowRight className="h-4 w-4" />
                      </a>
                    </Button>
                    <Button
                      asChild
                      variant="outline"
                      className="h-[44px] rounded-full border border-[#e1ddd6] bg-white px-7 text-[14px] font-medium text-slate-900 hover:bg-[#fafaf8]"
                    >
                      <a href="#how-it-works">Ver como funciona</a>
                    </Button>
                  </div>
                </div>

                <div className="justify-self-end">
                  <ProductSnapshot />
                </div>
              </section>
            </div>
          </div>

          <section className="border-y border-[#f0efea] bg-[#fcfcfb]">
            <div className="mx-auto grid max-w-[1220px] gap-4 px-8 py-7 md:grid-cols-3">
              {heroHighlights.map(({ icon: Icon, title }) => (
                <div
                  key={title}
                  className="flex items-center gap-3 rounded-[16px] border border-[#f1efea] bg-white px-6 py-5 text-[12px] font-medium text-slate-700 shadow-[0_20px_40px_-35px_rgba(15,23,42,0.16)]"
                >
                  <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#edfaff] text-[#19c8f2]">
                    <Icon className="h-3.5 w-3.5" />
                  </span>
                  <span>{title}</span>
                </div>
              ))}
            </div>
          </section>

          <section id="demo" className="mx-auto max-w-[1220px] px-8 pb-24 pt-16">
            <EmailAnalysisDemo />
          </section>

          <section id="how-it-works" className="bg-[#fafaf9] px-8 pb-20 pt-16">
            <div className="mx-auto max-w-[1220px]">
              <div className="mx-auto max-w-[720px] text-center">
                <h2 className="font-display text-[58px] font-semibold leading-[1.05] tracking-[-0.05em] text-slate-950">
                  Como o Inbox Pilot funciona?
                </h2>
                <p className="mx-auto mt-4 max-w-[620px] text-[15px] leading-7 text-slate-600">
                  Nossa tecnologia processa cada mensagem através de camadas de análise semântica
                  para entregar precisão absoluta.
                </p>
              </div>

              <div className="mt-14 grid gap-5 md:grid-cols-3">
                {workflowSteps.map(({ icon: Icon, step, title, description }) => (
                  <Card
                    key={title}
                    className="rounded-[18px] border border-[#eceae4] bg-white shadow-[0_24px_50px_-42px_rgba(15,23,42,0.16)]"
                  >
                    <CardContent className="flex flex-col items-center px-8 py-9 text-center">
                      <span className="flex h-[56px] w-[56px] items-center justify-center rounded-full bg-[#eafcff] text-[#19c8f2]">
                        <Icon className="h-6 w-6" />
                      </span>
                      <p className="mt-5 text-[10px] font-semibold uppercase tracking-[0.24em] text-[#19c8f2]">
                        {step}
                      </p>
                      <h3 className="mt-3 font-display text-[28px] font-semibold leading-[1.12] tracking-[-0.04em] text-slate-950">
                        {title}
                      </h3>
                      <p className="mt-4 text-[13px] leading-6 text-slate-500">{description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </section>

          <section className="px-8 py-14">
            <div className="mx-auto max-w-[1220px]">
              <p className="text-center text-[10px] font-semibold uppercase tracking-[0.35em] text-slate-500">
                Tecnologias de confiança
              </p>
              <div className="mt-8 flex flex-wrap items-center justify-center gap-x-14 gap-y-5 text-[16px] font-medium text-slate-500">
                {trustTechnologies.map(({ icon: Icon, label }) => (
                  <div key={label} className="inline-flex items-center gap-3">
                    <Icon className="h-5 w-5 text-[#19c8f2]" />
                    <span>{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="px-8 pb-14 pt-4">
            <div className="mx-auto max-w-[1220px]">
              <div className="rounded-[32px] bg-[radial-gradient(circle_at_top_right,rgba(14,192,241,0.18),transparent_28%),linear-gradient(135deg,#050520_0%,#07133d_42%,#082538_100%)] px-10 py-16 text-center shadow-[0_50px_110px_-60px_rgba(15,23,42,0.65)]">
                <h2 className="font-display text-[58px] font-semibold leading-[1.02] tracking-[-0.055em] text-white">
                  Pronto para testar em escala?
                </h2>
                <p className="mx-auto mt-6 max-w-[620px] text-[15px] leading-8 text-white/70">
                  Junte-se a centenas de gestores que transformaram suas caixas de entrada
                  operacionais em centros de produtividade.
                </p>
                <div className="mt-10">
                  <Button
                    asChild
                    className="h-[52px] rounded-full border-0 bg-white px-10 text-[15px] font-semibold text-slate-950 shadow-[0_20px_35px_-20px_rgba(255,255,255,0.5)] hover:bg-white/95"
                  >
                    <a href="#demo">Analisar seu primeiro email</a>
                  </Button>
                </div>
                <div className="mt-8 flex flex-wrap items-center justify-center gap-6 text-[12px] text-white/45">
                  <span>◌ Gemini Pro</span>
                  <span>◌ OpenRouter</span>
                  <span>◌ Fallback Local</span>
                </div>
              </div>
            </div>
          </section>

          <footer className="border-t border-[#efede8] px-8 py-7">
            <div className="mx-auto flex max-w-[1220px] flex-col items-center justify-between gap-4 text-[11px] text-slate-500 md:flex-row">
              <div className="flex items-center gap-2 font-medium text-slate-600">
                <span className="rounded bg-slate-500 px-1.5 py-0.5 text-[10px] text-white">⚡</span>
                <span>Inbox Pilot</span>
              </div>
              <p className="text-center">
                © 2024 Inbox Pilot AI. Todos os direitos reservados. Feito com foco em performance operacional.
              </p>
              <div className="flex items-center gap-5">
                {footerLinks.map((link) => (
                  <a key={link} href="#" className="transition-colors hover:text-slate-800">
                    {link}
                  </a>
                ))}
              </div>
            </div>
          </footer>
        </div>
      </div>
    </main>
  );
}
