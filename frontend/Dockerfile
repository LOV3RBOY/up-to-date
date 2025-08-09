FROM node:18-alpine

# Set working directory
WORKDIR /app

COPY package.json ./
RUN npm install --silent

COPY . .

# Build the Next.js app for production
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
