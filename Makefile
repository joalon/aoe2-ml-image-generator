
.PHONY: rpm clean test

test:
	python3 -m aoe2_image_gen multi_label -n 5 --visible

rpm:
	python3 setup.py bdist_rpm

clean:
	rm -rf build dist aoe2_image_gen.egg-info results
