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
    id: "confirm-meeting",
    title: "Confirmar Reunião",
    subject: "Confirm meeting follow-up",
    body:
      "Bom dia, equipe. A reunião de hoje foi excelente para alinhar os próximos passos do projeto Alpha. Gostaria de confirmar se todos receberam a ata e se as tarefas designadas para sexta-feira estão claras. Aguardo confirmação.",
    category: "Produtivo",
    hint: "Bom para demonstrar um follow-up operacional claro."
  },
  {
    id: "checkout-error",
    title: "Erro de Checkout",
    subject: "Checkout flow issue",
    body:
      "Olá time, identificamos uma falha intermitente no checkout após a atualização de ontem. Conseguem validar a causa e responder com uma previsão de correção ainda hoje?",
    category: "Produtivo",
    hint: "Mostra urgência operacional e necessidade de resposta."
  },
  {
    id: "sales-followup",
    title: "Follow-up Vendas",
    subject: "Sales pipeline update",
    body:
      "Poderiam me enviar um status dos leads qualificados desta semana e confirmar se a cadência de resposta está dentro do SLA acordado?",
    category: "Produtivo",
    hint: "Útil para um caso de acompanhamento comercial."
  }
];

interface SampleEmailsProps {
  onSelectExample?: (example: SampleEmailExample) => void;
  className?: string;
}

export function SampleEmails({ onSelectExample, className }: SampleEmailsProps) {
  return (
    <div className={cn("flex flex-wrap gap-2", className)}>
      {sampleEmailExamples.map((example) => (
        <button
          key={example.id}
          type="button"
          onClick={() => onSelectExample?.(example)}
          disabled={!onSelectExample}
          className="rounded-full border border-[#edeae4] bg-[#fbfaf8] px-4 py-2 text-[11px] font-medium text-slate-600 transition-colors hover:border-[#d9f5fd] hover:bg-[#f1fcff] hover:text-slate-900 disabled:cursor-default"
        >
          {example.title}
        </button>
      ))}
    </div>
  );
}
