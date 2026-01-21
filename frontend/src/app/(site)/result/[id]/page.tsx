"use client";

import { useState, useEffect, use, useRef } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, Share2 } from "lucide-react";
import { toast } from "sonner";
import { apiClient } from "@/lib/api";
import { TryOnRequest } from "@/types";

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(
  /\/$/,
  ""
);

const resolveMediaUrl = (url?: string) => {
  if (!url) return "";
  if (url.startsWith("http://") || url.startsWith("https://")) return url;
  if (url.startsWith("/")) return `${API_BASE_URL}${url}`;
  return `${API_BASE_URL}/${url}`;
};

interface ResultPageProps {
  params: Promise<{ id: string }>;
}

export default function ResultPage({ params }: ResultPageProps) {
  const router = useRouter();
  const { id } = use(params);
  const [result, setResult] = useState<TryOnRequest | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const hasShownVideoErrorToast = useRef(false);

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout> | null = null;
    let isActive = true;

    const fetchResult = async () => {
      try {
        const data = await apiClient.getResult(id);
        if (!isActive) return;
        setResult(data);

        const isVideoError =
          !data.video_url &&
          Boolean(data.error_message) &&
          data.error_message.startsWith("Video generation failed");

        if (isVideoError && !hasShownVideoErrorToast.current) {
          hasShownVideoErrorToast.current = true;
          toast.error("영상 생성 실패", {
            description: data.error_message,
          });
        }

        const shouldPoll =
          (!data.video_url && (data.status === "processing" || data.status === "pending")) ||
          (data.status === "completed" && !data.video_url && !isVideoError);

        if (shouldPoll) {
          timeoutId = setTimeout(fetchResult, 2000);
        }
      } catch {
        if (!isActive) return;
        setError("결과를 불러오는데 실패했습니다.");
      } finally {
        if (!isActive) return;
        setIsLoading(false);
      }
    };

    fetchResult();

    return () => {
      isActive = false;
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [id]);

  const handleRetry = () => {
    router.push("/fitting");
  };

  const handleShare = async () => {
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
      <div className="min-h-[90vh] bg-white text-black flex">
        <div className="mx-auto flex w-full max-w-md flex-1 flex-col min-h-0 border-x border-neutral-200">
          <div className="flex flex-1 flex-col min-h-0 pt-[50px]">
            <div className="flex items-center justify-center px-2 py-1">
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
            <div className="p-2 text-center">
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
      <div className="min-h-[90vh] bg-white text-black flex">
        <div className="mx-auto flex w-full max-w-md flex-1 flex-col items-center justify-center px-4 min-h-0 border-x border-neutral-200">
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

  const isVideoError =
    !result.video_url &&
    Boolean(result.error_message) &&
    result.error_message.startsWith("Video generation failed");

  if (
    (!result.video_url && (result.status === "processing" || result.status === "pending")) ||
    (result.status === "completed" && !result.video_url && !isVideoError)
  ) {
    return (
      <div className="min-h-[90vh] bg-white text-black flex">
        <div className="mx-auto flex w-full max-w-md flex-1 flex-col min-h-0 border-x border-neutral-200">
          <div className="flex flex-1 flex-col min-h-0 pt-[50px]">
            <div className="flex items-center justify-center px-2 py-1">
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
            <div className="p-2 text-center">
              <p className="text-lg font-semibold uppercase tracking-wide text-black">
                CREATING YOUR LOOK...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (result.status === "failed" || isVideoError) {
    return (
      <div className="min-h-[90vh] bg-white text-black flex">
        <div className="mx-auto flex w-full max-w-md flex-1 flex-col items-center justify-center px-4 min-h-0 border-x border-neutral-200">
          <p className="text-lg text-center mb-4">
            {result.error_message || "결과 생성에 실패했습니다."}
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
    <div className="min-h-[90vh] bg-white text-black flex">
      <div className="mx-auto flex w-full max-w-md flex-1 flex-col min-h-0 border-x border-neutral-200">
        {/* 헤더 */}
        <div className="p-3 flex items-center justify-between border-b border-neutral-200">
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
        <div className="flex-1 min-h-0 px-3 pt-3 overflow-y-auto">
          {result.video_url && (
            <div className="relative w-full aspect-[3/4] bg-neutral-100 rounded-lg overflow-hidden">
              <video
                className="h-full w-full object-contain"
                src={resolveMediaUrl(result.video_url)}
                controls
                autoPlay
                muted
                loop
                playsInline
                preload="metadata"
              />
            </div>
          )}
        </div>

        {/* 하단 버튼 */}
        <div className="px-3 py-2 border-t border-neutral-200">
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
