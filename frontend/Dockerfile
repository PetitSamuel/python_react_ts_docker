FROM node:12.6.0
ADD . /frontend
WORKDIR /frontend
COPY package.json /frontend
COPY package-lock.json /frontend
RUN npm install
COPY . /frontend
CMD npm start