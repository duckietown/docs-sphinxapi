
AIDO_REGISTRY ?= docker.io
PIP_INDEX_URL ?= https://pypi.org/simple

build_options=\
 	--build-arg AIDO_REGISTRY=$(AIDO_REGISTRY)\
 	--build-arg PIP_INDEX_URL=$(PIP_INDEX_URL)


all:

tag=$(AIDO_REGISTRY)/duckietown/docs-sphinxapi:daffy
outdir=output-dir

build:
	docker build -t $(tag) $(build_options) .

push: build
	docker push $(tag)

run: build
	rm -rf $(outdir)
	mkdir -p $(outdir)
	docker run -it --rm -v "$(PWD)/$(outdir):/output" $(tag)
