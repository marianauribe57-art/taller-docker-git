FROM node:18-alpine

WORKDIR /app

COPY src/package*.json ./
RUN npm install --omit=dev

COPY src/ ./

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "server.js"]