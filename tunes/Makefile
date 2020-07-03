all:
	python3 -m sipy

serve:
	cd build/ && python3 -m sipy serve

watch:
	while true; do \
		make; \
		inotifywait -qre close_write .; \
	done
