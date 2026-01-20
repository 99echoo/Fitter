"use client";

import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import { Loading } from "@/components/common/Loading";
import { ResultViewer } from "@/components/fitting/ResultViewer";
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

  if (isLoading) {
    return (
      <div className="container max-w-4xl mx-auto py-12">
        <Loading message="결과를 불러오는 중..." />
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="container max-w-4xl mx-auto py-12 text-center">
        <p className="text-destructive mb-4">{error || "결과를 찾을 수 없습니다."}</p>
        <button
          onClick={handleRetry}
          className="text-primary underline"
        >
          다시 시도하기
        </button>
      </div>
    );
  }

  if (result.status === "processing" || result.status === "pending") {
    return (
      <div className="container max-w-4xl mx-auto py-12">
        <Loading message="AI가 이미지를 생성하고 있습니다..." />
      </div>
    );
  }

  if (result.status === "failed") {
    return (
      <div className="container max-w-4xl mx-auto py-12 text-center">
        <p className="text-destructive mb-4">
          {result.error_message || "이미지 생성에 실패했습니다."}
        </p>
        <button
          onClick={handleRetry}
          className="text-primary underline"
        >
          다시 시도하기
        </button>
      </div>
    );
  }

  return (
    <div className="container max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6 text-center">피팅 결과</h1>

      {result.result_image_url && (
        <ResultViewer
          resultImageUrl={result.result_image_url}
          videoUrl={result.video_url}
          onRetry={handleRetry}
          onGenerateVideo={handleGenerateVideo}
          isVideoLoading={isVideoLoading}
        />
      )}
    </div>
  );
}
