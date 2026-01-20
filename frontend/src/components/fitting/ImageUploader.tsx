"use client";

import { useCallback, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
    },
    [handleFile]
  );

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <h3 className="font-semibold mb-2">{label}</h3>
        <p className="text-sm text-muted-foreground mb-4">{description}</p>

        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            isDragging
              ? "border-primary bg-primary/5"
              : "border-muted-foreground/25 hover:border-primary/50"
          }`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          {preview ? (
            <div className="space-y-4">
              <img
                src={preview}
                alt="Preview"
                className="max-h-48 mx-auto rounded-lg object-contain"
              />
              <Button
                variant="outline"
                onClick={() => {
                  setPreview(null);
                }}
              >
                다시 선택
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="text-4xl">📷</div>
              <p className="text-sm text-muted-foreground">
                이미지를 드래그하거나 클릭하여 업로드하세요
              </p>
              <input
                type="file"
                accept={acceptedFormats}
                onChange={handleInputChange}
                className="hidden"
                id={`upload-${label}`}
              />
              <Button asChild variant="outline">
                <label htmlFor={`upload-${label}`} className="cursor-pointer">
                  파일 선택
                </label>
              </Button>
            </div>
          )}
        </div>

        {error && <p className="text-sm text-destructive mt-2">{error}</p>}
      </CardContent>
    </Card>
  );
}
