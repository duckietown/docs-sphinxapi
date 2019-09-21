# parameters
ARG REPO_NAME="dt-duckiebot-interface"

# ==================================================>
# ==> Do not change this code
ARG ARCH=arm32v7
ARG MAJOR=daffy
ARG BASE_TAG=${MAJOR}-${ARCH}
ARG BASE_IMAGE=dt-ros-commons

# define base image
FROM duckietown/${BASE_IMAGE}:${BASE_TAG}

# define repository path
ARG REPO_NAME
ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"
WORKDIR "${REPO_PATH}"

# create repo directory
RUN mkdir -p "${REPO_PATH}"

# copy dependencies files only
COPY dt-duckiebot-interface/dependencies-apt.txt "${REPO_PATH}/"
COPY dt-duckiebot-interface/dependencies-py.txt "${REPO_PATH}/"

# install apt dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    $(awk -F: '/^[^#]/ { print $1 }' dependencies-apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install -r ${REPO_PATH}/dependencies-py.txt

# copy the source code
COPY dt-duckiebot-interface "${REPO_PATH}/"

############################################
## ADD CAR INTERFACE

# parameters
ARG REPO_NAME="dt-car-interface"

# ==================================================>
# ==> Do not change this code

# define repository path
ARG REPO_NAME=dt-car-interface
ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"
WORKDIR "${REPO_PATH}"

# create repo directory and copy the source code
RUN mkdir -p "${REPO_PATH}"


# copy dependencies files only
COPY dt-car-interface/dependencies-apt.txt "${REPO_PATH}/"
COPY dt-car-interface/dependencies-py.txt "${REPO_PATH}/"

COPY dt-car-interface "${REPO_PATH}/"

# install apt dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    $(awk -F: '/^[^#]/ { print $1 }' dependencies-apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install -r ${REPO_PATH}/dependencies-py.txt

# build packages
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
  catkin build \
    --workspace ${CATKIN_WS_DIR}/

# define launch script
ENV LAUNCHFILE "${REPO_PATH}/launch.sh"

# define command
CMD ["bash", "-c", "${LAUNCHFILE}"]
# <== Do not change this code
# <==================================================

### ADDD DOCS STUFF

RUN apt-get update; apt-get install -y git

RUN python -m pip install sphinx==1.7.0 sphinx-rtd-theme sphinx-autobuild mock

RUN cd /; git clone https://github.com/AleksandarPetrov/napoleon; cd /napoleon; python setup.py install -f

COPY docs ${CATKIN_WS_DIR}/src/docs

CMD "/ros_entrypoint.sh"

RUN ls "${CATKIN_WS_DIR}/src/"
RUN cp -r "${CATKIN_WS_DIR}/src/dt-ros-commons" "${CATKIN_WS_DIR}/src/docs/source/repositories/"
RUN cp -r "${CATKIN_WS_DIR}/src/dt-car-interface" "${CATKIN_WS_DIR}/src/docs/source/repositories/"
RUN cp -r "${CATKIN_WS_DIR}/src/dt-duckiebot-interface" "${CATKIN_WS_DIR}/src/docs/source/repositories/"

# maintainer
LABEL maintainer="Liam Paull (<YOUR_EMAIL_ADDRESS>)"
