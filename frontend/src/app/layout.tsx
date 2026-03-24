import type { ReactNode } from "react";
import type { Metadata } from "next";
import { Roboto_Flex } from "next/font/google";

import "./globals.css";

const robotoFlexSans = Roboto_Flex({
  subsets: ["latin"],
  variable: "--font-sans"
});

const robotoFlexDisplay = Roboto_Flex({
  subsets: ["latin"],
  variable: "--font-display"
});

export const metadata: Metadata = {
  title: "Inbox Pilot",
  description: "Operational email triage with structured analysis and suggested replies."
};

export default function RootLayout({
  children
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html
      lang="pt-BR"
      className={`${robotoFlexSans.variable} ${robotoFlexDisplay.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
