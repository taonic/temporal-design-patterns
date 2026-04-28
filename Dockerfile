# syntax=docker/dockerfile:1.7

# Stage 1: build the VitePress static site at base "/" so it can be served
# from the fly app's root (the GitHub Pages build uses "/temporal-design-patterns/").
FROM node:20-bookworm-slim AS docs-builder
WORKDIR /repo
COPY package.json package-lock.json ./
RUN npm ci
COPY docs ./docs
ENV VITEPRESS_BASE=/
RUN npm run docs:build

# Stage 2: install sandbox-runner deps (tsx is a devDep but is the runtime entrypoint).
FROM node:20-bookworm-slim AS runner-deps
WORKDIR /app
COPY sandbox-runner/package.json sandbox-runner/package-lock.json ./
RUN npm ci

# Stage 3: runtime image. Hosts the Express API and serves the built docs from
# the same origin, so DaytonaRunner.vue's relative /api/* calls keep working.
FROM node:20-bookworm-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=8080 \
    DOCS_DIST_DIR=/app/docs-dist
COPY --from=runner-deps /app/node_modules ./node_modules
COPY sandbox-runner/package.json sandbox-runner/tsconfig.json ./
COPY sandbox-runner/src ./src
COPY sandbox-runner/patterns ./patterns
COPY sandbox-runner/runtime ./runtime
COPY --from=docs-builder /repo/docs/.vitepress/dist /app/docs-dist
EXPOSE 8080
CMD ["npm", "start"]
