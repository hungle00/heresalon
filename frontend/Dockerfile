FROM node:20-alpine

# The default working directory for the image
WORKDIR /app

# Copy package.json and yarn.lock into the image
COPY package.json yarn.lock ./

# Install yarn globally (if not already available)
# RUN npm install -g yarn

# Install node dependencies using yarn
RUN yarn install --frozen-lockfile

# Copies everything over to Docker environment
COPY . .

# The default command to use when running this image
CMD ["yarn", "start"]
