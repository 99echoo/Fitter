"use client";

import { useCallback, useState } from "react";
import Image from "next/image";

interface ImageUploaderProps {
  label: string;
  description: string;
  onImageSelect: (file: File) => void;
  acceptedFormats?: string;
  maxSizeMB?: number;
}

export function ImageUploader({
  label,
  description,
  onImageSelect,
  acceptedFormats = "image/jpeg,image/png,image/webp",
  maxSizeMB = 10,
}: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const inputId = `upload-${label}`;

  const handleFile = useCallback(
    (file: File) => {
      setError(null);

      if (!file.type.match(/^image\/(jpeg|png|webp)$/)) {
        setError("JPG, PNG, WebP 형식만 지원됩니다.");
        return;
      }

      if (file.size > maxSizeMB * 1024 * 1024) {
        setError(`파일 크기는 ${maxSizeMB}MB 이하여야 합니다.`);
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);

      onImageSelect(file);
    },
    [maxSizeMB, onImageSelect]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const file = e.dataTransfer.files[0];
      if (file) {
        handleFile(file);
      }
    },
    [handleFile]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        handleFile(file);
      }
      e.target.value = "";
    },
    [handleFile]
  );

  return (
    <div className="w-full bg-neutral-100 rounded-lg p-4">
      <h3 className="font-semibold text-black mb-1">{label}</h3>
      <p className="text-sm text-gray-500 mb-4">{description}</p>

      <div
        className={`border-2 border-dashed rounded-lg p-3 transition-colors ${
          isDragging
            ? "border-black bg-neutral-200"
            : "border-neutral-300 hover:border-neutral-400"
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <div className="relative h-48 w-full">
          {preview ? (
            <>
              <Image
                src={preview}
                alt="Preview"
                fill
                sizes="100vw"
                className="object-contain rounded-lg"
                unoptimized
              />
            <label
              htmlFor={inputId}
              className="absolute bottom-3 right-3 px-3 py-1.5 text-xs border border-neutral-300 rounded text-black hover:bg-neutral-200 transition cursor-pointer bg-white/90"
            >
              다시 선택
            </label>
            </>
          ) : (
            <div className="flex h-full w-full flex-col items-center justify-center gap-3 text-center">
              <div className="text-3xl">📷</div>
              <p className="text-sm text-gray-500">
                이미지를 드래그하거나 클릭하여 업로드
              </p>
              <label
                htmlFor={inputId}
                className="inline-block px-4 py-2 text-sm border border-neutral-300 rounded text-black hover:bg-neutral-200 transition cursor-pointer"
              >
                파일 선택
              </label>
            </div>
          )}
          <input
            type="file"
            accept={acceptedFormats}
            onChange={handleInputChange}
            className="hidden"
            id={inputId}
          />
        </div>
      </div>

      {error && <p className="text-sm text-red-500 mt-2">{error}</p>}
    </div>
  );
}
