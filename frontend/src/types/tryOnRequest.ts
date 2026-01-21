import { ClothingCategory } from "./clothing";

export type TryOnStatus = "pending" | "processing" | "completed" | "failed";

export interface ClothingItemReference {
  id: string;
  category: ClothingCategory;
  name?: string;
}

export interface TryOnRequest {
  id: string;
  clothing_id: string;
  clothing_items?: ClothingItemReference[];
  face_image_path: string;
  body_image_path: string;
  status: TryOnStatus;
  result_image_url?: string;
  video_url?: string;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

export interface TryOnResponse {
  request_id: string;
  status: TryOnStatus;
  result_image_url?: string;
  clothing_items?: ClothingItemReference[];
  created_at: string;
}

export interface VideoGenerateResponse {
  video_id: string;
  status: TryOnStatus;
  video_url?: string;
  duration: number;
  resolution: string;
}
