export function getProxiedImageUrl(originalUrl: string): string {
  return `/api/proxy-image?url=${encodeURIComponent(originalUrl)}`;
}
