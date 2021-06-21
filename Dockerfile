ARG ARCH=amd64
ARG MAJOR=daffy
ARG ROS_DISTRO=kinetic
ARG BASE_TAG=${MAJOR}-${ARCH}
ARG VERSION="6.0.1"
# define base image
ARG DOCKER_REGISTRY=docker.io
FROM ${DOCKER_REGISTRY}/duckietown/dt-ros-${ROS_DISTRO}-base:${BASE_TAG}

ENV SOURCE_DIR /code
ENV CATKIN_WS_DIR "${SOURCE_DIR}/catkin_ws"

# copy dependencies files only
COPY ./dependencies-apt.txt "${REPO_PATH}/"
COPY ./dependencies-py.txt "${REPO_PATH}/"

# install apt dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    $(awk -F: '/^[^#]/ { print $1 }' /dependencies-apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
ARG PIP_INDEX_URL="https://pypi.org/simple"
ENV PIP_INDEX_URL=${PIP_INDEX_URL}
RUN echo PIP_INDEX_URL=${PIP_INDEX_URL}

RUN python3 -m pip install -r /dependencies-py.txt


# copy docs boilerplate
COPY docs ${CATKIN_WS_DIR}/src/docs

# install napoleon
RUN cd /; git clone https://github.com/AleksandarPetrov/napoleon; cd /napoleon; python setup.py install -f

# build the docs
COPY launch.sh /launch.sh
#RUN /launch.sh
CMD []
ENTRYPOINT /launch.sh
