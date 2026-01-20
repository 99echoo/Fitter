import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero Banner */}
      <section className="relative bg-gradient-to-r from-zinc-900 to-zinc-800 text-white">
        <div className="container mx-auto px-4 py-24 md:py-32">
          <div className="max-w-2xl">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              AI로 미리 입어보세요
            </h1>
            <p className="text-lg md:text-xl text-zinc-300 mb-8">
              사진 한 장으로 원하는 옷을 가상으로 착용해보고
              <br />
              나에게 어울리는 스타일을 찾아보세요.
            </p>
            <Button asChild size="lg" className="text-lg px-8 py-6">
              <Link href="/fitting">AI 피팅룸 입장</Link>
            </Button>
          </div>
        </div>
        <div className="absolute inset-0 bg-[url('/images/hero-pattern.svg')] opacity-10" />
      </section>

      {/* Features */}
      <section className="py-16 md:py-24 bg-zinc-50">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl md:text-3xl font-bold text-center mb-12">
            어떻게 사용하나요?
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-xl shadow-sm text-center">
              <div className="text-4xl mb-4">1</div>
              <h3 className="font-semibold mb-2">사진 업로드</h3>
              <p className="text-muted-foreground">
                얼굴 사진과 전신 사진을 업로드해주세요
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm text-center">
              <div className="text-4xl mb-4">2</div>
              <h3 className="font-semibold mb-2">의상 선택</h3>
              <p className="text-muted-foreground">
                입어보고 싶은 옷을 선택해주세요
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm text-center">
              <div className="text-4xl mb-4">3</div>
              <h3 className="font-semibold mb-2">결과 확인</h3>
              <p className="text-muted-foreground">
                AI가 생성한 피팅 이미지를 확인하세요
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 md:py-24">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-4">
            지금 바로 체험해보세요
          </h2>
          <p className="text-muted-foreground mb-8 max-w-md mx-auto">
            AI 가상 피팅으로 온라인 쇼핑의 새로운 경험을 만나보세요.
          </p>
          <Button asChild size="lg">
            <Link href="/fitting">시작하기</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
