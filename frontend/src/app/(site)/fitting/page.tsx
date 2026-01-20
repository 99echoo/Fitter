"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { ImageUploader } from "@/components/fitting/ImageUploader";
import { ClothingSelector } from "@/components/fitting/ClothingSelector";
import { Loading } from "@/components/common/Loading";
import { apiClient } from "@/lib/api";
import { Clothing } from "@/types";

type Step = 1 | 2 | 3;

export default function FittingPage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>(1);
  const [faceImage, setFaceImage] = useState<File | null>(null);
  const [bodyImage, setBodyImage] = useState<File | null>(null);
  const [selectedClothing, setSelectedClothing] = useState<Clothing | null>(null);
  const [clothingItems, setClothingItems] = useState<Clothing[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClothing = async () => {
      setIsLoading(true);
      try {
        const items = await apiClient.getClothingList();
        setClothingItems(items);
      } catch {
        setError("의상 목록을 불러오는데 실패했습니다.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchClothing();
  }, []);

  const handleSubmit = async () => {
    if (!faceImage || !bodyImage || !selectedClothing) {
      setError("모든 항목을 선택해주세요.");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await apiClient.createTryOn(
        faceImage,
        bodyImage,
        selectedClothing.id
      );
      router.push(`/result/${response.request_id}`);
    } catch {
      setError("피팅 요청에 실패했습니다. 다시 시도해주세요.");
      setIsSubmitting(false);
    }
  };

  const canProceed = () => {
    switch (step) {
      case 1:
        return faceImage !== null;
      case 2:
        return bodyImage !== null;
      case 3:
        return selectedClothing !== null;
      default:
        return false;
    }
  };

  const progressValue = ((step - 1) / 2) * 100;

  if (isSubmitting) {
    return (
      <div className="container max-w-4xl mx-auto py-12">
        <Loading message="AI가 피팅 이미지를 생성하고 있습니다..." />
      </div>
    );
  }

  return (
    <div className="container max-w-4xl mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-4">AI 피팅룸</h1>
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Step {step} / 3</span>
            <span>
              {step === 1 && "얼굴 사진 업로드"}
              {step === 2 && "전신 사진 업로드"}
              {step === 3 && "의상 선택"}
            </span>
          </div>
          <Progress value={progressValue} className="h-2" />
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 text-destructive rounded-lg">
          {error}
        </div>
      )}

      {step === 1 && (
        <ImageUploader
          label="얼굴 사진"
          description="정면을 바라보는 밝은 조명의 얼굴 사진을 업로드해주세요."
          onImageSelect={setFaceImage}
        />
      )}

      {step === 2 && (
        <ImageUploader
          label="전신 사진"
          description="정면 자세의 전신이 보이는 사진을 업로드해주세요."
          onImageSelect={setBodyImage}
        />
      )}

      {step === 3 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">의상을 선택해주세요</h2>
          {isLoading ? (
            <Loading message="의상 목록을 불러오는 중..." />
          ) : (
            <ClothingSelector
              items={clothingItems}
              onSelect={setSelectedClothing}
              selectedId={selectedClothing?.id}
            />
          )}
        </div>
      )}

      <div className="flex justify-between mt-8">
        <Button
          variant="outline"
          onClick={() => setStep((prev) => (prev > 1 ? ((prev - 1) as Step) : prev))}
          disabled={step === 1}
        >
          이전
        </Button>

        {step < 3 ? (
          <Button
            onClick={() => setStep((prev) => ((prev + 1) as Step))}
            disabled={!canProceed()}
          >
            다음
          </Button>
        ) : (
          <Button onClick={handleSubmit} disabled={!canProceed()}>
            피팅하기
          </Button>
        )}
      </div>
    </div>
  );
}
