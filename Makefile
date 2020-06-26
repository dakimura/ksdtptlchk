
build:
	docker build . -t ksdtptlchk

run:
	docker run --log-driver json-file --log-opt max-size=10m --log-opt max-file=10 ksdtptlchk:latest python