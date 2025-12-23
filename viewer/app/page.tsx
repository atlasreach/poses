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

interface Creation {
  id: string;
  source: string;
  sourceImageUrl: string;
  url: string;
  title: string;
  description: string;
  resolution: string;
  cost: string;
  generatedAt: string;
  metadata: Record<string, string>;
}

type SortOption = 'algorithm' | 'likes' | 'comments' | 'engagement' | 'original';
type Tab = 'posts' | 'creations';

export default function Home() {
  const [activeTab, setActiveTab] = useState<Tab>('posts');
  const [allPosts, setAllPosts] = useState<InstagramPost[]>([]);
  const [posts, setPosts] = useState<InstagramPost[]>([]);
  const [creations, setCreations] = useState<Creation[]>([]);
  const [selectedPost, setSelectedPost] = useState<InstagramPost | null>(null);
  const [selectedCreation, setSelectedCreation] = useState<Creation | null>(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<SortOption>('algorithm');

  useEffect(() => {
    // Load Instagram posts
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
        console.error('Error loading posts:', err);
        setLoading(false);
      });

    // Load creations
    fetch('/creations_data.json')
      .then(res => res.json())
      .then(data => {
        setCreations(data);
      })
      .catch(err => {
        console.error('Error loading creations:', err);
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
            @{posts[0]?.ownerUsername}
          </p>
        </div>

        {/* Tabs */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="flex gap-8">
            <button
              onClick={() => setActiveTab('posts')}
              className={`pb-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'posts'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📸 Instagram Posts
              <span className="ml-2 bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full text-xs">
                {posts.length}
              </span>
            </button>
            <button
              onClick={() => setActiveTab('creations')}
              className={`pb-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'creations'
                  ? 'border-purple-500 text-purple-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              ✨ Creations
              <span className="ml-2 bg-purple-100 text-purple-600 px-2 py-0.5 rounded-full text-xs">
                {creations.length}
              </span>
            </button>
          </nav>
        </div>

        {/* Posts Tab */}
        {activeTab === 'posts' && (
          <>
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
                {posts.length} posts, {posts.reduce((sum, p) => sum + p.images.length, 0)} images
              </div>
            </div>

            <PostGrid posts={posts} onPostClick={setSelectedPost} />
          </>
        )}

        {/* Creations Tab */}
        {activeTab === 'creations' && (
          <>
            <div className="mb-6 flex items-center justify-between">
              <div className="text-sm text-gray-600">
                {creations.length} AI-generated images • Total cost: ${(creations.length * 0.134).toFixed(2)}
              </div>
              <div className="text-sm text-gray-500">
                Source: NanaBanana API (Google Gemini)
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {creations.map((creation, index) => (
                <div
                  key={creation.id}
                  onClick={() => setSelectedCreation(creation)}
                  className="relative aspect-square bg-gray-200 rounded-lg overflow-hidden cursor-pointer group hover:opacity-90 transition-opacity"
                >
                  <img
                    src={creation.url}
                    alt={creation.title}
                    className="w-full h-full object-cover"
                  />

                  <div className="absolute top-3 left-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-2 py-1 rounded-full text-xs font-bold">
                    #{index + 1}
                  </div>

                  <div className="absolute top-3 right-3 bg-black/70 text-white px-2 py-1 rounded-full text-xs font-medium">
                    {creation.resolution}
                  </div>

                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/60 transition-colors flex flex-col items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="text-white font-bold text-center px-4 mb-2">
                      {creation.title}
                    </div>
                    <div className="text-white/80 text-sm text-center px-4">
                      {creation.metadata.location}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Post Modal */}
        {selectedPost && (
          <PostModal
            post={selectedPost}
            onClose={() => setSelectedPost(null)}
          />
        )}

        {/* Creation Modal */}
        {selectedCreation && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={() => setSelectedCreation(null)}>
            <div className="bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-auto" onClick={(e) => e.stopPropagation()}>
              <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">{selectedCreation.title}</h2>
                  <p className="text-sm text-gray-600">{selectedCreation.description}</p>
                </div>
                <button
                  onClick={() => setSelectedCreation(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
                >
                  ×
                </button>
              </div>

              <div className="p-6">
                <img
                  src={selectedCreation.url}
                  alt={selectedCreation.title}
                  className="w-full rounded-lg mb-6"
                />

                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Resolution</div>
                    <div className="text-base text-gray-900">{selectedCreation.resolution}</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Cost</div>
                    <div className="text-base text-gray-900">{selectedCreation.cost}</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Source</div>
                    <div className="text-base text-gray-900 capitalize">{selectedCreation.source.replace('_', ' ')}</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Generated</div>
                    <div className="text-base text-gray-900">{new Date(selectedCreation.generatedAt).toLocaleDateString()}</div>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h3 className="text-sm font-bold text-gray-900 mb-3">Generation Details</h3>
                  <div className="space-y-2">
                    {Object.entries(selectedCreation.metadata).map(([key, value]) => (
                      <div key={key} className="flex">
                        <div className="text-sm font-medium text-gray-500 w-40 capitalize">
                          {key.replace(/_/g, ' ')}:
                        </div>
                        <div className="text-sm text-gray-900 flex-1">{value}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border-t mt-6 pt-4">
                  <a
                    href={selectedCreation.sourceImageUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    View original Instagram image →
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
