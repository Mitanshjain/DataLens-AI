import type { Metadata, Viewport } from "next";
import { Fraunces, Geist, Geist_Mono, Instrument_Sans } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

// Display serif used for headings (font-serif)
const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
  style: ["normal", "italic"],
  display: "swap",
});

// Body sans used across the app (font-sans)
const instrumentSans = Instrument_Sans({
  variable: "--font-instrument",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "DataLens AI | Data into decisions",
    template: "%s | DataLens AI",
  },
  description:
    "Upload a CSV and DataLens AI profiles it, trains and explains a model, and writes a business briefing grounded in your data.",
  applicationName: "DataLens AI",
  keywords: [
    "data analysis",
    "machine learning",
    "explainability",
    "business intelligence",
    "CSV analytics",
  ],
  openGraph: {
    title: "DataLens AI | Data into decisions",
    description:
      "Profiling, modelling, explainability and a business briefing, generated from one CSV.",
    siteName: "DataLens AI",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "DataLens AI | Data into decisions",
    description:
      "Upload a CSV and get profiling, a trained model, explainability and a business briefing.",
  },
};

export const viewport: Viewport = {
  // Matches the dark hero so the mobile browser bar blends into the page
  themeColor: "#060a13",
  colorScheme: "light",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      // Dark html background keeps overscroll at the top (hero) and bottom (footer) seamless
      className={`${fraunces.variable} ${instrumentSans.variable} ${geistSans.variable} ${geistMono.variable} h-full scroll-smooth bg-[#060a13] antialiased [text-rendering:optimizeLegibility]`}
    >
      <body className="flex min-h-full flex-col bg-[#f5f4ef] text-[#0c1424] selection:bg-[#4d5b9e]/20 [-webkit-tap-highlight-color:transparent]">
        {children}
      </body>
    </html>
  );
}