/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // Disable telemetry for production
  telemetry: {
    enabled: false,
  },
}

module.exports = nextConfig
