'use client';

import { useState, useEffect } from 'react';
import PostGrid from '@/components/PostGrid';
import PostModal from '@/components/PostModal';

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
  engagementScore?: number;
  rawEngagement?: number;
}

type SortOption = 'algorithm' | 'likes' | 'comments' | 'engagement' | 'original';

export default function Home() {
  const [allPosts, setAllPosts] = useState<InstagramPost[]>([]);
  const [posts, setPosts] = useState<InstagramPost[]>([]);
  const [selectedPost, setSelectedPost] = useState<InstagramPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<SortOption>('algorithm');

  useEffect(() => {
    fetch('/instagram_data.json')
      .then(res => res.json())
      .then(data => {
        // Calculate engagement scores
        const totalEngagement = data.reduce((sum: number, p: InstagramPost) =>
          sum + p.likesCount + p.commentsCount, 0
        );
        const avgEngagement = totalEngagement / data.length;

        // Add scores to each post
        const scoredPosts = data.map((post: InstagramPost, index: number) => {
          const rawEngagement = post.likesCount + (post.commentsCount * 2); // Comments worth 2x
          const performanceMultiplier = rawEngagement / avgEngagement;
          const engagementScore = rawEngagement * performanceMultiplier;

          return {
            ...post,
            rawEngagement,
            engagementScore,
            originalIndex: index
          };
        });

        setAllPosts(scoredPosts);

        // Default sort by algorithm
        const sorted = [...scoredPosts].sort((a, b) =>
          (b.engagementScore || 0) - (a.engagementScore || 0)
        );
        setPosts(sorted);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading data:', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (allPosts.length === 0) return;

    let sorted = [...allPosts];

    switch (sortBy) {
      case 'algorithm':
        sorted.sort((a, b) => (b.engagementScore || 0) - (a.engagementScore || 0));
        break;
      case 'likes':
        sorted.sort((a, b) => b.likesCount - a.likesCount);
        break;
      case 'comments':
        sorted.sort((a, b) => b.commentsCount - a.commentsCount);
        break;
      case 'engagement':
        sorted.sort((a, b) =>
          (b.likesCount + b.commentsCount) - (a.likesCount + a.commentsCount)
        );
        break;
      case 'original':
        sorted.sort((a, b) => (a as any).originalIndex - (b as any).originalIndex);
        break;
    }

    setPosts(sorted);
  }, [sortBy, allPosts]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading posts...</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Instagram Content Viewer</h1>
          <p className="text-gray-600">
            @{posts[0]?.ownerUsername} - {posts.length} posts, {posts.reduce((sum, p) => sum + p.images.length, 0)} images
          </p>
        </div>

        {/* Filter Dropdown */}
        <div className="mb-6 flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Sort by:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortOption)}
            className="px-4 py-2 border border-gray-300 rounded-lg bg-white text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="algorithm">🎯 Algorithm Score (Best)</option>
            <option value="engagement">💬 Total Engagement</option>
            <option value="likes">❤️ Most Likes</option>
            <option value="comments">💬 Most Comments</option>
            <option value="original">📅 Original Order</option>
          </select>

          <div className="ml-auto text-sm text-gray-500">
            Avg Engagement: {Math.round(allPosts.reduce((sum, p) => sum + p.likesCount + p.commentsCount, 0) / allPosts.length).toLocaleString()}
          </div>
        </div>

        <PostGrid posts={posts} onPostClick={setSelectedPost} />

        {selectedPost && (
          <PostModal
            post={selectedPost}
            onClose={() => setSelectedPost(null)}
          />
        )}
      </div>
    </main>
  );
}
