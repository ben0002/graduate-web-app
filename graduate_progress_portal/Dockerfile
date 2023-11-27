# Use an official Node.js runtime as the base image
FROM node:18

# Set the working directory within the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the React app source code to the container
COPY . .

# Build the React app (replace 'build' with your actual build script)
#RUN npm run build

# Expose a port (e.g., 80) for the React app to run
EXPOSE 80

# Specify the command to start your React app
CMD ["npm", "start"]