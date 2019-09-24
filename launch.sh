#!/bin/bash

set -e

mkdir -p "${CATKIN_WS_DIR}/src"

while read p; do
  repo=$(python -c "print '${p}'.split(':')[0]")
  branch_name=$(python -c "print '${p}'.split(':')[1]")
  repo_name=$(python -c "print '${repo}'.split('/')[1]")
  git clone --depth 1 -b ${branch_name} "https://github.com/${repo}" "${CATKIN_WS_DIR}/src/${repo_name}"
done < /repositories.txt

# build packages
source /opt/ros/${ROS_DISTRO}/setup.sh && \
  catkin_make -C ${CATKIN_WS_DIR}/

while read p; do
  repo=$(python -c "print '${p}'.split(':')[0]")
  branch_name=$(python -c "print '${p}'.split(':')[1]")
  repo_name=$(python -c "print '${repo}'.split('/')[1]")
  # clone source into sphynx (try with symlink)
  git clone --depth 1 -b ${branch_name} "https://github.com/${repo}" "${CATKIN_WS_DIR}/src/docs/source/repositories/${repo_name}"
done < /repositories.txt

source "${CATKIN_WS_DIR}/devel/setup.bash"

# build docs
cd "${CATKIN_WS_DIR}/src/docs"
make html
