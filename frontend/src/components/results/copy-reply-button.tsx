"use client";

import * as React from "react";
import { Check, Copy } from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface CopyReplyButtonProps {
  text: string;
  className?: string;
  buttonClassName?: string;
  hintClassName?: string;
  label?: string;
  copiedLabel?: string;
}

export function CopyReplyButton({
  text,
  className,
  buttonClassName,
  hintClassName,
  label = "Copiar resposta",
  copiedLabel = "Copiada"
}: CopyReplyButtonProps) {
  const [copied, setCopied] = React.useState(false);
  const timeoutRef = React.useRef<number | null>(null);

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current !== null) {
        window.clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      if (timeoutRef.current !== null) {
        window.clearTimeout(timeoutRef.current);
      }
      timeoutRef.current = window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <Button
        type="button"
        variant="outline"
        onClick={handleCopy}
        className={cn("rounded-full", buttonClassName)}
      >
        {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
        {label || copiedLabel ? <span>{copied ? copiedLabel : label}</span> : null}
      </Button>
      <span className={cn("text-xs font-medium text-muted-foreground", hintClassName)} aria-live="polite">
        {copied ? "Texto copiado para a área de transferência." : "Pronto para compartilhar a resposta."}
      </span>
    </div>
  );
}
