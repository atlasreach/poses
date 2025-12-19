'use client';

import { useState } from 'react';
import { getProxiedImageUrl } from '@/lib/utils';

interface InstagramPost {
  id: string;
  type: string;
  caption: string;
  url: string;
  likesCount: number;
  commentsCount: number;
  images: string[];
  displayUrl: string;
  ownerUsername: string;
  ownerId: string;
}

interface PostModalProps {
  post: InstagramPost;
  onClose: () => void;
}

export default function PostModal({ post, onClose }: PostModalProps) {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [copiedUrl, setCopiedUrl] = useState<string | null>(null);

  // Use images array if available, otherwise use displayUrl
  const allImages = post.images && post.images.length > 0 ? post.images : [post.displayUrl];

  const handleCopyUrl = (url: string) => {
    navigator.clipboard.writeText(url);
    setCopiedUrl(url);
    setTimeout(() => setCopiedUrl(null), 2000);
  };

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % allImages.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + allImages.length) % allImages.length);
  };

  return (
    <div
      className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col lg:flex-row"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Image Section */}
        <div className="lg:w-2/3 bg-black flex items-center justify-center relative">
          <img
            src={getProxiedImageUrl(allImages[currentImageIndex])}
            alt={`Image ${currentImageIndex + 1}`}
            className="max-h-[70vh] lg:max-h-[90vh] w-auto object-contain"
          />

          {allImages.length > 1 && (
            <>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  prevImage();
                }}
                className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/90 hover:bg-white rounded-full p-3 shadow-lg z-10"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  nextImage();
                }}
                className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/90 hover:bg-white rounded-full p-3 shadow-lg z-10"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>

              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/70 text-white px-3 py-1 rounded-full text-sm">
                {currentImageIndex + 1} / {allImages.length}
              </div>
            </>
          )}
        </div>

        {/* Details Section */}
        <div className="lg:w-1/3 flex flex-col max-h-[90vh]">
          {/* Header */}
          <div className="p-4 border-b flex items-center justify-between">
            <div className="font-semibold">@{post.ownerUsername}</div>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Caption */}
          <div className="p-4 border-b flex-1 overflow-y-auto">
            <div className="mb-4">
              <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                <span>❤️ {post.likesCount.toLocaleString()}</span>
                <span>💬 {post.commentsCount.toLocaleString()}</span>
              </div>
              <p className="text-sm whitespace-pre-wrap">{post.caption}</p>
            </div>

            <div className="mt-4">
              <a
                href={post.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline text-sm"
              >
                View on Instagram →
              </a>
            </div>
          </div>

          {/* Copy URL Section */}
          <div className="p-4 border-t bg-gray-50">
            <div className="mb-3">
              <div className="text-sm font-medium text-gray-700 mb-2">Current Image URL:</div>
              <button
                onClick={() => handleCopyUrl(allImages[currentImageIndex])}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                {copiedUrl === allImages[currentImageIndex] ? '✓ Copied!' : 'Copy Current Image URL'}
              </button>
            </div>

            {allImages.length > 1 && (
              <div>
                <div className="text-sm font-medium text-gray-700 mb-2">All Images:</div>
                <div className="space-y-1 max-h-40 overflow-y-auto">
                  {allImages.map((url, index) => (
                    <button
                      key={index}
                      onClick={() => handleCopyUrl(url)}
                      className={`w-full text-left text-xs py-2 px-3 rounded transition-colors ${
                        copiedUrl === url
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                      }`}
                    >
                      {copiedUrl === url ? '✓ Copied' : `Image ${index + 1}`}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
