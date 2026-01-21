"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { X } from "lucide-react";
import { ImageUploader } from "@/components/fitting/ImageUploader";
import { ClothingSelector } from "@/components/fitting/ClothingSelector";
import { Loading } from "@/components/common/Loading";
import { apiClient } from "@/lib/api";
import { Clothing } from "@/types";

type Step = 0 | 1 | 2;

export default function FittingPage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>(0);
  const [faceImage, setFaceImage] = useState<File | null>(null);
  const [bodyImage, setBodyImage] = useState<File | null>(null);
  const [selectedClothings, setSelectedClothings] = useState<Clothing[]>([]);
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
    if (!faceImage || !bodyImage || selectedClothings.length === 0) {
      setError("모든 항목을 선택해주세요.");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // 첫 번째 선택된 의상으로 피팅 요청 (추후 다중 지원 시 수정)
      const response = await apiClient.createTryOn(
        faceImage,
        bodyImage,
        selectedClothings[0].id
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
        return selectedClothings.length > 0;
      case 2:
        return faceImage !== null && bodyImage !== null;
      default:
        return false;
    }
  };

  // 대기 화면
  if (isSubmitting) {
    return (
      <div className="min-h-screen bg-white text-black flex items-center justify-center">
        <div className="mx-auto max-w-sm px-4">
          <Loading message="AI가 피팅 이미지를 생성하고 있습니다..." />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white text-black">
      <div className="mx-auto max-w-md min-h-screen flex flex-col">
        {/* Step 0: 시작 화면 */}
        {step === 0 && (
          <div className="flex flex-col min-h-screen">
            {/* 헤더 - X 버튼 */}
            <div className="p-4">
              <button
                onClick={() => router.back()}
                className="text-black hover:text-gray-600 transition"
                aria-label="닫기"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* 시작 화면 비디오 */}
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

            {/* 하단 영역 */}
            <div className="p-4 space-y-3 text-center">
              <p className="text-sm uppercase tracking-wide leading-relaxed text-gray-600">
                사진이 밝고 선명한지, 혼자 찍은 사진인지 확인해주세요.
                <br />
                안경, 모자, 헤드폰은 벗어주세요.
              </p>
              <button
                onClick={() => setStep(1)}
                className="w-full bg-black text-white py-3 font-medium tracking-wider"
              >
                START
              </button>
              <p className="text-xs text-gray-400 leading-relaxed">
                AI 기술을 사용합니다. 계속 진행하면{" "}
                <span className="underline">이용약관</span>과{" "}
                <span className="underline">개인정보처리방침</span>에 동의하는
                것으로 간주합니다.
              </p>
            </div>
          </div>
        )}

        {/* Step 1: 의상 선택 */}
        {step === 1 && (
          <div className="flex flex-col min-h-screen">
            {/* 헤더 */}
            <div className="p-4 flex items-center justify-between">
              <button
                onClick={() => setStep(0)}
                className="text-black hover:text-gray-600 transition"
                aria-label="뒤로"
              >
                <X className="h-6 w-6" />
              </button>
              <span className="text-sm text-gray-500">1 / 2</span>
            </div>

            {/* 콘텐츠 */}
            <div className="flex-1 px-4 pb-4 overflow-y-auto">
              <h2 className="text-lg font-semibold mb-4 uppercase tracking-wide text-center text-gray-700">Select The Look</h2>
              {error && (
                <div className="mb-4 p-3 bg-red-100 text-red-600 rounded-lg text-sm">
                  {error}
                </div>
              )}
              {isLoading ? (
                <Loading message="의상 목록을 불러오는 중..." />
              ) : (
                <ClothingSelector
                  items={clothingItems}
                  onSelect={setSelectedClothings}
                  selectedIds={selectedClothings.map((c) => c.id)}
                />
              )}
            </div>

            {/* 하단 버튼 */}
            <div className="p-4 border-t border-neutral-200">
              <button
                onClick={() => setStep(2)}
                disabled={!canProceed()}
                className="w-full bg-black text-white py-3 font-medium tracking-wider uppercase disabled:bg-neutral-200 disabled:text-neutral-400 transition"
              >
                CREATE LOOK
              </button>
            </div>
          </div>
        )}

        {/* Step 2: 사진 업로드 */}
        {step === 2 && (
          <div className="flex flex-col min-h-screen">
            {/* 헤더 */}
            <div className="p-4 flex items-center justify-between">
              <button
                onClick={() => setStep(1)}
                className="text-black hover:text-gray-600 transition"
                aria-label="뒤로"
              >
                <X className="h-6 w-6" />
              </button>
              <span className="text-sm text-gray-500">2 / 2</span>
            </div>

            {/* 콘텐츠 */}
            <div className="flex-1 px-4 pb-4 overflow-y-auto">
              <div className="mb-4">
                <h2 className="text-lg font-semibold">사진을 업로드해주세요</h2>
                <p className="text-sm text-gray-500 mt-1">
                  얼굴 사진과 전신 사진을 모두 업로드해야 피팅이 가능합니다.
                </p>
              </div>
              {error && (
                <div className="mb-4 p-3 bg-red-100 text-red-600 rounded-lg text-sm">
                  {error}
                </div>
              )}
              <div className="space-y-4">
                <ImageUploader
                  label="얼굴 사진"
                  description="정면을 바라보는 밝은 조명의 얼굴 사진"
                  onImageSelect={setFaceImage}
                />
                <ImageUploader
                  label="전신 사진"
                  description="정면 자세의 전신이 보이는 사진"
                  onImageSelect={setBodyImage}
                />
              </div>
            </div>

            {/* 하단 버튼 */}
            <div className="p-4 border-t border-neutral-200">
              <button
                onClick={handleSubmit}
                disabled={!canProceed()}
                className="w-full bg-black text-white py-3 font-medium disabled:bg-neutral-200 disabled:text-neutral-400 transition"
              >
                피팅하기
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
