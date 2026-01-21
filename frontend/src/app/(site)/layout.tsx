import { MusinsaHeader } from "@/components/musinsa/MusinsaHeader";
import { Toaster } from "@/components/ui/sonner";

export default function SiteLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <MusinsaHeader />
      <main className="flex-1">{children}</main>
      <Toaster />
    </>
  );
}
