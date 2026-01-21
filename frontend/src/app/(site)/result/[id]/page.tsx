"use client";

import { useState, useEffect, use } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { ChevronLeft, Share2 } from "lucide-react";
import { toast } from "sonner";
import { apiClient } from "@/lib/api";
import { TryOnRequest } from "@/types";

interface ResultPageProps {
  params: Promise<{ id: string }>;
}

export default function ResultPage({ params }: ResultPageProps) {
  const router = useRouter();
  const { id } = use(params);
  const [result, setResult] = useState<TryOnRequest | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isVideoLoading, setIsVideoLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const data = await apiClient.getResult(id);
        setResult(data);

        if (data.status === "processing" || data.status === "pending") {
          setTimeout(fetchResult, 2000);
        }
      } catch {
        setError("결과를 불러오는데 실패했습니다.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchResult();
  }, [id]);

  const handleGenerateVideo = async () => {
    setIsVideoLoading(true);
    try {
      await apiClient.generateVideo(id);

      const pollVideo = async () => {
        const data = await apiClient.getResult(id);
        setResult(data);

        if (!data.video_url && data.status !== "failed") {
          setTimeout(pollVideo, 2000);
        } else {
          setIsVideoLoading(false);
        }
      };

      pollVideo();
    } catch {
      setError("영상 생성에 실패했습니다.");
      setIsVideoLoading(false);
    }
  };

  const handleRetry = () => {
    router.push("/fitting");
  };

  const handleShare = async () => {
    if (!result?.result_image_url) return;

    try {
      if (navigator.share) {
        await navigator.share({
          title: "My Fitting Look",
          text: "AI 가상 피팅 결과를 확인해보세요!",
          url: window.location.href,
        });
      } else {
        // 폴백: 클립보드 복사
        await navigator.clipboard.writeText(window.location.href);
        toast.success("링크 복사됨", {
          description: "링크가 클립보드에 복사되었습니다.",
        });
      }
    } catch (error) {
      console.error("공유 실패:", error);
    }
  };

  const handleAddToCart = () => {
    // TODO: 실제 장바구니 추가 API 연동
    toast.success("장바구니 추가", {
      description: "선택한 룩이 장바구니에 추가되었습니다.",
    });

    // 임시: 무신사 페이지로 이동
    router.push("/musinsa");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white text-black">
        <div className="mx-auto max-w-md min-h-screen flex flex-col">
          <div className="flex flex-col min-h-screen">
            <div className="flex-1 flex items-center justify-center px-2 py-2">
              <div className="relative w-full max-h-[65vh] aspect-[269/482] rounded-lg overflow-hidden flex items-center justify-center">
                <video
                  className="h-full w-full object-contain"
                  src="/main.mp4"
                  autoPlay
                  muted
                  loop
                  playsInline
                  preload="auto"
                />
              </div>
            </div>
            <div className="p-4 text-center">
              <p className="text-lg font-semibold uppercase tracking-wide text-black">
                LOADING YOUR RESULT...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="min-h-screen bg-white text-black">
        <div className="mx-auto max-w-md min-h-screen flex flex-col items-center justify-center px-4">
          <p className="text-lg text-center mb-4">
            {error || "결과를 찾을 수 없습니다."}
          </p>
          <button
            onClick={handleRetry}
            className="px-6 py-2 border-2 border-black text-black hover:bg-black hover:text-white transition"
          >
            다시 시도하기
          </button>
        </div>
      </div>
    );
  }

  if (result.status === "processing" || result.status === "pending") {
    return (
      <div className="min-h-screen bg-white text-black">
        <div className="mx-auto max-w-md min-h-screen flex flex-col">
          <div className="flex flex-col min-h-screen">
            <div className="flex-1 flex items-center justify-center px-2 py-2">
              <div className="relative w-full max-h-[65vh] aspect-[269/482] rounded-lg overflow-hidden flex items-center justify-center">
                <video
                  className="h-full w-full object-contain"
                  src="/main.mp4"
                  autoPlay
                  muted
                  loop
                  playsInline
                  preload="auto"
                />
              </div>
            </div>
            <div className="p-4 text-center">
              <p className="text-lg font-semibold uppercase tracking-wide text-black">
                CREATING YOUR LOOK...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (result.status === "failed") {
    return (
      <div className="min-h-screen bg-white text-black">
        <div className="mx-auto max-w-md min-h-screen flex flex-col items-center justify-center px-4">
          <p className="text-lg text-center mb-4">
            {result.error_message || "이미지 생성에 실패했습니다."}
          </p>
          <button
            onClick={handleRetry}
            className="px-6 py-2 border-2 border-black text-black hover:bg-black hover:text-white transition"
          >
            다시 시도하기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white text-black">
      <div className="mx-auto max-w-md min-h-screen flex flex-col">
        {/* 헤더 */}
        <div className="p-4 flex items-center justify-between border-b border-neutral-200">
          <button
            onClick={() => router.back()}
            className="text-black hover:text-gray-600 transition"
            aria-label="뒤로"
          >
            <ChevronLeft className="h-6 w-6" />
          </button>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium uppercase tracking-wide">MY LOOKS</span>
            <button
              onClick={handleShare}
              className="text-black hover:text-gray-600 transition"
              aria-label="공유"
            >
              <Share2 className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* 콘텐츠 영역 */}
        <div className="flex-1 px-4 pt-4 overflow-y-auto">
          {result.result_image_url && (
            <div className="relative w-full aspect-[3/4] bg-neutral-100 rounded-lg overflow-hidden">
              <Image
                src={result.result_image_url}
                alt="피팅 결과"
                fill
                sizes="100vw"
                className="object-cover"
                unoptimized
              />
            </div>
          )}
        </div>

        {/* 하단 버튼 */}
        <div className="px-4 py-2 border-t border-neutral-200">
          <button
            onClick={handleAddToCart}
            className="w-full border-2 border-black text-black py-3 font-medium tracking-wider uppercase hover:bg-black hover:text-white transition"
          >
            ADD
          </button>
        </div>
      </div>
    </div>
  );
}
