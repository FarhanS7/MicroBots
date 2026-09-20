FROM node:20-alpine AS builder

WORKDIR /app

# Enable pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy root workspace files and package files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/protocol ./packages/protocol
COPY apps/web ./apps/web

# Install dependencies and build web frontend
RUN pnpm install --frozen-lockfile
RUN pnpm --filter @microbots/protocol build
RUN pnpm --filter @microbots/web build

FROM nginx:alpine AS runner

# Copy nginx static build artifact
COPY --from=builder /app/apps/web/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
