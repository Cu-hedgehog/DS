FROM node:lts as dependencies
WORKDIR /front-end
COPY package.json package-lock.json ./
RUN npm install && npm cache clean --force

FROM node:lts as builder
WORKDIR /front-end
COPY . .
COPY --from=dependencies /front-end/node_modules ./node_modules
RUN npm run build

FROM node:lts as runner
WORKDIR /front-end
COPY --from=builder /front-end/public ./public
COPY --from=builder /front-end/package.json ./package.json
COPY --from=builder /front-end/.next ./.next
COPY --from=builder /front-end/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "start"]
