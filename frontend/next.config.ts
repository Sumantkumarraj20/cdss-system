import type { NextConfig } from "next";
import withSerwistInit from "@serwist/next";

const withSerwist = withSerwistInit({
  // Path to your service worker source file
  swSrc: "app/sw.ts",
  // Where the compiled service worker will be placed
  swDest: "public/sw.js",
  // Corresponds to your old 'disable' logic
  disable: process.env.NODE_ENV === "development",
  // Equivalent to 'cacheOnFrontEndNav'
  cacheOnNavigation: true,
});

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
};

export default withSerwist(nextConfig);
