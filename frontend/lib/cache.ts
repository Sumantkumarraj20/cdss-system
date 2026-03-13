const DAY_MS = 1000 * 60 * 60 * 24;

const REDIS_REST_URL = process.env.NEXT_PUBLIC_REDIS_REST_URL;
const REDIS_REST_TOKEN = process.env.NEXT_PUBLIC_REDIS_REST_TOKEN;

const hasRedis = Boolean(REDIS_REST_URL && REDIS_REST_TOKEN);
const memoryFallback = new Map<string, { value: unknown; expiresAt: number }>();

async function redisGet<T>(key: string): Promise<T | null> {
  if (!hasRedis) return null;
  try {
    const res = await fetch(`${REDIS_REST_URL}/get/${encodeURIComponent(key)}`, {
      headers: { Authorization: `Bearer ${REDIS_REST_TOKEN}` },
      cache: "no-store",
    });
    if (!res.ok) return null;
    const data = (await res.json()) as { result?: T | null };
    return (data?.result as T | null) ?? null;
  } catch (error) {
    console.warn("redis get failed", error);
    return null;
  }
}

async function redisSet<T>(key: string, value: T, ttlMs = DAY_MS) {
  if (!hasRedis) return;
  try {
    const ttlSeconds = Math.max(60, Math.floor(ttlMs / 1000));
    await fetch(`${REDIS_REST_URL}/set/${encodeURIComponent(key)}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${REDIS_REST_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ value, ex: ttlSeconds }),
    });
  } catch (error) {
    console.warn("redis set failed", error);
  }
}

function storageGet<T>(key: string): T | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { value: T; expiresAt: number };
    if (Date.now() > parsed.expiresAt) {
      window.localStorage.removeItem(key);
      return null;
    }
    return parsed.value;
  } catch (error) {
    console.warn("localStorage get failed", error);
    return null;
  }
}

function storageSet<T>(key: string, value: T, ttlMs = DAY_MS) {
  if (typeof window === "undefined") return;
  try {
    const payload = { value, expiresAt: Date.now() + ttlMs };
    window.localStorage.setItem(key, JSON.stringify(payload));
  } catch (error) {
    console.warn("localStorage set failed", error);
  }
}

export async function getCachedValue<T>(key: string): Promise<T | null> {
  const memory = memoryFallback.get(key);
  if (memory && memory.expiresAt > Date.now()) return memory.value as T;

  const local = storageGet<T>(key);
  if (local) return local;

  const redis = await redisGet<T>(key);
  if (redis) return redis;

  return null;
}

export async function setCachedValue<T>(key: string, value: T, ttlMs = DAY_MS) {
  memoryFallback.set(key, { value, expiresAt: Date.now() + ttlMs });
  storageSet(key, value, ttlMs);
  await redisSet(key, value, ttlMs);
}

export async function fetchWithCache<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlMs = DAY_MS
): Promise<T> {
  const cached = await getCachedValue<T>(key);
  if (cached) return cached;

  const fresh = await fetcher();
  await setCachedValue(key, fresh, ttlMs);
  return fresh;
}

export const CACHE_KEYS = {
  presentation: (slug: string) => `presentations:${slug}`,
  diagnoses: (slug: string) => `diagnoses:${slug}`,
  drugs: (slug: string) => `drug-info:${slug}`,
};

export const CACHE_TTL_MS = DAY_MS;
