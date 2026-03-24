import Image from "next/image";
import {
  ArrowRight,
  Layers3,
  Mail,
  Shield,
  Sparkles,
  SquareMousePointer,
  Zap,
} from "lucide-react";

import { EmailAnalysisDemo } from "@/components/forms/email-analysis-demo";
import { ProductSnapshot } from "@/components/marketing/product-snapshot";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const heroHighlights = [
  {
    icon: SquareMousePointer,
    title: "Entrada sem fricção",
  },
  {
    icon: Layers3,
    title: "Leitura imediata de IA",
  },
  {
    icon: Zap,
    title: "Pronto para operação",
  },
];

const workflowSteps = [
  {
    icon: Mail,
    step: "Passo 01",
    title: "Recebemos o email",
    description:
      "Nossa engine captura o conteúdo bruto do email ou extrai o texto de documentos anexados para iniciar a análise.",
  },
  {
    icon: Sparkles,
    step: "Passo 02",
    title: "Interpretamos e classificamos",
    description:
      "Usando a camada de IA, identificamos a intenção, o tom de voz e a prioridade operacional de cada mensagem.",
  },
  {
    icon: ArrowRight,
    step: "Passo 03",
    title: "Sugerimos próxima ação",
    description:
      "Você recebe uma classificação imediata e uma sugestão de resposta pronta para ser enviada.",
  },
];

const trustTechnologies = [
  {
    icon: Shield,
    label: "Enterprise Grade",
  },
  {
    icon: Layers3,
    label: "Multi-LLM Support",
  },
  {
    icon: Zap,
    label: "Ultra-Fast Response",
  },
];

const footerLinks = ["Termos", "Privacidade", "Suporte"];

export default function HomePage() {
  return (
    <main className="bg-white text-slate-950">
      <div className="w-full pb-10">
        <div className="overflow-hidden bg-white">
          <div className="relative overflow-hidden">
            <div className="relative mx-auto max-w-[1920px] px-6 pb-14 pt-5 md:px-8 xl:px-12 2xl:px-16">
              <header className="flex items-center justify-between border-b border-[#f0efea] pb-4 px-14">
                <a href="#" className="inline-flex items-center gap-3">
                  <Image
                    src="/logo.png"
                    alt="Inbox Pilot"
                    width={132}
                    height={32}
                    className="h-8 w-auto"
                    priority
                  />
                </a>
                <nav className="hidden items-center gap-8 text-[11px] font-medium text-slate-700 md:flex">
                  <a
                    href="#demo"
                    className="rounded-full bg-[#19c8f2] px-4 py-2 text-white shadow-[0_12px_24px_-14px_rgba(25,200,242,0.9)] transition-opacity hover:opacity-95"
                  >
                    Testar Agora
                  </a>
                </nav>
              </header>

              <section className="grid items-center gap-8 pb-12 pt-12 md:gap-10 md:pb-14 md:pt-16 xl:grid-cols-[minmax(0,60%)_minmax(560px,40%)] xl:gap-10 2xl:gap-14">
                <div className="min-w-0 max-w-[1200px]">
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#00aee6] bg-white/72 px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.1em] bg-[#e6f9fd] text-[#00aee6]">
                    <Sparkles className="h-3 w-3 text-yellow-400" />
                    Nova Versão disponível!
                  </div>

                  <h1 className="mt-7 max-w-[7.2ch] font-display text-[clamp(3.35rem,16vw,4.3rem)] font-semibold leading-[0.9] tracking-[-0.05em] text-slate-950 md:mt-8 md:max-w-full md:text-[clamp(4rem,4.95vw,5.35rem)] md:leading-[0.94] md:tracking-normal">
                    Analisar emails
                    <br />
                    operacionais
                    <br />
                    <span className="bg-[linear-gradient(90deg,#18c6f2_0%,#36c1e7_18%,#8a7ce4_52%,#d38f49_100%)] bg-clip-text text-transparent">
                      rápido e confiável
                    </span>
                  </h1>

                  <p className="mt-6 max-w-[360px] text-[15px] leading-8 text-slate-600 md:mt-7 md:max-w-[700px] md:text-[18px] md:leading-9">
                    Cole, envie ou teste um exemplo. Resultado imediato com
                    categoria, confiança e resposta sugerida baseada em
                    inteligência contextual.
                  </p>

                  <div className="mt-8 flex max-w-[280px] flex-col items-stretch gap-4 sm:max-w-none sm:flex-row sm:flex-wrap sm:items-center">
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

                <div className="w-full justify-self-center pt-2 xl:justify-self-end xl:max-w-[820px] xl:pt-0 2xl:max-w-[860px]">
                  <ProductSnapshot />
                </div>
              </section>
            </div>
          </div>

          <section className="border-y border-[#f0efea] bg-[#fcfcfb]">
            <div className="mx-auto grid max-w-[1920px] gap-5 px-6 py-7 md:grid-cols-3 md:px-8 xl:px-12 2xl:px-16">
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

          <section
            id="demo"
            className="mx-auto max-w-[1920px] px-6 pb-24 pt-16 md:px-8 xl:px-12 2xl:px-16"
          >
            <EmailAnalysisDemo />
          </section>

          <section
            id="how-it-works"
            className="bg-[#fafaf9] px-6 pb-20 pt-16 md:px-8 xl:px-12 2xl:px-16"
          >
            <div className="mx-auto max-w-[1920px]">
              <div className="mx-auto max-w-[760px] text-center">
                <h2 className="font-display text-[clamp(3rem,4.5vw,3.625rem)] font-semibold leading-[1.05] tracking-[-0.05em] text-slate-950">
                  Como o Inbox Pilot funciona?
                </h2>
                <p className="mx-auto mt-4 max-w-[620px] text-[15px] leading-7 text-slate-600">
                  Nossa tecnologia processa cada mensagem através de camadas de
                  análise semântica para entregar com uma maior precisão.
                </p>
              </div>

              <div className="mt-14 grid gap-6 lg:grid-cols-3">
                {workflowSteps.map(
                  ({ icon: Icon, step, title, description }) => (
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
                        <p className="mt-4 text-[13px] leading-6 text-slate-500">
                          {description}
                        </p>
                      </CardContent>
                    </Card>
                  ),
                )}
              </div>
            </div>
          </section>

          <section className="px-6 py-14 md:px-8 xl:px-12 2xl:px-16">
            <div className="mx-auto max-w-[1920px]">
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

          <section className="px-6 pb-14 pt-4 md:px-8 xl:px-12 2xl:px-16">
            <div className="mx-auto max-w-[1920px]">
              <div className="rounded-[32px] bg-[radial-gradient(circle_at_top_right,rgba(14,192,241,0.18),transparent_28%),linear-gradient(135deg,#050520_0%,#07133d_42%,#082538_100%)] px-10 py-16 text-center shadow-[0_50px_110px_-60px_rgba(15,23,42,0.65)]">
                <h2 className="font-display text-[clamp(3rem,4.6vw,3.625rem)] font-semibold leading-[1.02] tracking-[-0.055em] text-white">
                  Pronto para testar em escala?
                </h2>
                <p className="mx-auto mt-6 max-w-[620px] text-[15px] leading-8 text-white/70">
                  Junte-se a centenas de gestores que transformaram suas caixas
                  de entrada operacionais em centros de produtividade.
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
                  <span>◌ Gemini</span>
                  <span>◌ OpenRouter</span>
                  <span>◌ Fallback Local</span>
                </div>
              </div>
            </div>
          </section>

          <footer className="border-t border-[#efede8] px-6 py-7 md:px-8 xl:px-12 2xl:px-16">
            <div className="mx-auto flex max-w-[1920px] flex-col items-center justify-between gap-4 text-[11px] text-slate-500 md:flex-row">
              <div className="flex items-center gap-2 font-medium text-slate-600">
                <span className="rounded bg-slate-500 px-1.5 py-0.5 text-[10px] text-white">
                  ⚡
                </span>
                <span>Inbox Pilot</span>
              </div>
              <p className="text-center">
                © 2024 Inbox Pilot AI. Todos os direitos reservados. Feito com
                foco em performance operacional.
              </p>
              <div className="flex items-center gap-5">
                {footerLinks.map((link) => (
                  <a
                    key={link}
                    href="#"
                    className="transition-colors hover:text-slate-800"
                  >
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
