
.PHONY: rpm clean

rpm:
	python3 setup.py bdist_rpm

clean:
	rm -rf build dist aoe2_image_gen.egg-info
