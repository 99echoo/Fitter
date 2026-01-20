"use client";

import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";

interface LoadingProps {
  message?: string;
  progress?: number;
  showCancel?: boolean;
  onCancel?: () => void;
}

export function Loading({
  message = "처리 중입니다...",
  progress,
  showCancel,
  onCancel,
}: LoadingProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin" />
      <p className="text-lg font-medium">{message}</p>
      {progress !== undefined && (
        <div className="w-full max-w-xs">
          <Progress value={progress} className="h-2" />
          <p className="text-sm text-muted-foreground text-center mt-2">
            {progress}%
          </p>
        </div>
      )}
      {showCancel && onCancel && (
        <button
          onClick={onCancel}
          className="text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          취소
        </button>
      )}
    </div>
  );
}

export function ImageSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="aspect-square w-full rounded-lg" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
    </div>
  );
}
