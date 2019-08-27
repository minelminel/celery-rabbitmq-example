FROM alpine:latest

# pip3 python3
RUN apk add python3

# copy source into location
ADD ./src /opt/artifice
WORKDIR /opt/artifice
# install requirements
RUN pip3 install -e .

# set up system resources


# housekeeping


# run the app
