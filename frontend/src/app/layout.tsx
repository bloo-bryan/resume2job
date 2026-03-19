import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { NavBar } from "@/components/nav-bar";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Resume2Job",
  description: "Multi-signal resume-to-job matching engine",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} font-sans antialiased bg-[#09090B] text-zinc-100`}
      >
        <a href="#main-content" className="skip-nav">
          Skip to main content
        </a>
        <NavBar />
        <main
          id="main-content"
          className="max-w-[1200px] mx-auto px-4 pt-20 pb-12"
        >
          {children}
        </main>
      </body>
    </html>
  );
}
