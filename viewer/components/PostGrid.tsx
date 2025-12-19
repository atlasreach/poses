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

interface PostGridProps {
  posts: InstagramPost[];
  onPostClick: (post: InstagramPost) => void;
}

export default function PostGrid({ posts, onPostClick }: PostGridProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {posts.map((post, index) => {
        const engagement = post.likesCount + post.commentsCount;
        return (
          <div
            key={post.id}
            onClick={() => onPostClick(post)}
            className="relative aspect-square bg-gray-200 rounded-lg overflow-hidden cursor-pointer group hover:opacity-90 transition-opacity"
          >
            <img
              src={getProxiedImageUrl(post.displayUrl)}
              alt={post.caption?.slice(0, 100) || 'Instagram post'}
              className="w-full h-full object-cover"
            />

            <div className="absolute top-3 left-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-2 py-1 rounded-full text-xs font-bold">
              #{index + 1}
            </div>

            {post.images.length > 1 && (
              <div className="absolute top-3 right-3 bg-black/70 text-white px-2 py-1 rounded-full text-xs font-medium">
                1/{post.images.length}
              </div>
            )}

            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex flex-col items-center justify-center opacity-0 group-hover:opacity-100">
              <div className="text-white font-medium flex gap-4 mb-1">
                <span>❤️ {post.likesCount.toLocaleString()}</span>
                <span>💬 {post.commentsCount.toLocaleString()}</span>
              </div>
              <div className="text-white text-sm font-semibold">
                {engagement.toLocaleString()} total engagement
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
