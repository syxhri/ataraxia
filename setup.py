from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as ldf:
	long_desc = ldf.read()

setup(
	name="ataraxia",
	version="1.0.3",
	packages=find_packages(),
	
	install_requires=[
		'requests==2.32.2'
	],
	
	author="syxhri",
	author_email="syxhri.id@gmail.com",
	description="Unofficial Python wrapper of Blackbox AI",
	long_description=long_desc,
	long_description_content_type="text/markdown",
	url="https://github.com/syxhri/ataraxia",
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
	],
	python_requires='>=3.7'
)