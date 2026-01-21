"use client";

import { useState } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface ResultViewerProps {
  originalImageUrl?: string;
  resultImageUrl: string;
  videoUrl?: string;
  onRetry?: () => void;
  onGenerateVideo?: () => void;
  isVideoLoading?: boolean;
}

export function ResultViewer({
  originalImageUrl,
  resultImageUrl,
  videoUrl,
  onRetry,
  onGenerateVideo,
  isVideoLoading,
}: ResultViewerProps) {
  const [showComparison, setShowComparison] = useState(false);
  const [showVideo, setShowVideo] = useState(false);

  const handleDownload = async (url: string, filename: string) => {
    const response = await fetch(url);
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="p-6">
          {showVideo && videoUrl ? (
            <div className="aspect-square relative bg-black rounded-lg overflow-hidden">
              <video
                src={videoUrl}
                controls
                autoPlay
                loop
                className="w-full h-full object-contain"
              />
            </div>
          ) : showComparison && originalImageUrl ? (
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <p className="text-sm font-medium text-center">Before</p>
                <div className="aspect-square relative bg-muted rounded-lg overflow-hidden">
                  <Image
                    src={originalImageUrl}
                    alt="Original"
                    fill
                    sizes="50vw"
                    className="object-contain"
                    unoptimized
                  />
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-sm font-medium text-center">After</p>
                <div className="aspect-square relative bg-muted rounded-lg overflow-hidden">
                  <Image
                    src={resultImageUrl}
                    alt="Result"
                    fill
                    sizes="50vw"
                    className="object-contain"
                    unoptimized
                  />
                </div>
              </div>
            </div>
          ) : (
            <div className="aspect-square relative bg-muted rounded-lg overflow-hidden max-w-lg mx-auto">
              <Image
                src={resultImageUrl}
                alt="Result"
                fill
                sizes="(min-width: 1024px) 32rem, 100vw"
                className="object-contain"
                unoptimized
              />
            </div>
          )}
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-3 justify-center">
        {originalImageUrl && (
          <Button
            variant="outline"
            onClick={() => {
              setShowComparison(!showComparison);
              setShowVideo(false);
            }}
          >
            {showComparison ? "결과만 보기" : "Before/After 비교"}
          </Button>
        )}

        {videoUrl ? (
          <Button
            variant="outline"
            onClick={() => {
              setShowVideo(!showVideo);
              setShowComparison(false);
            }}
          >
            {showVideo ? "이미지 보기" : "360도 영상 보기"}
          </Button>
        ) : onGenerateVideo ? (
          <Button
            variant="outline"
            onClick={onGenerateVideo}
            disabled={isVideoLoading}
          >
            {isVideoLoading ? "영상 생성 중..." : "360도 영상 생성"}
          </Button>
        ) : null}

        <Button onClick={() => handleDownload(resultImageUrl, "fitter-result.png")}>
          이미지 다운로드
        </Button>

        {videoUrl && (
          <Button
            variant="outline"
            onClick={() => handleDownload(videoUrl, "fitter-video.mp4")}
          >
            영상 다운로드
          </Button>
        )}

        {onRetry && (
          <Button variant="secondary" onClick={onRetry}>
            다른 옷 입어보기
          </Button>
        )}
      </div>
    </div>
  );
}
