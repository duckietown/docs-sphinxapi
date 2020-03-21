all:

tag=duckietown/docs-sphinxapi:daffy
outdir=output-dir

build:
	docker build -t $(tag) .

push: build
	docker push $(tag)

run: build
	rm -rf $(outdir)
	mkdir -p $(outdir)
	docker run -it --rm -v "$(PWD)/$(outdir):/output" $(tag)
