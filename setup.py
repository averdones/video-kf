import setuptools


setuptools.setup(
    name="keyframes-extractor",
    version="0.0.1",
    author="Antonio Verdone",
    author_email="averdones@gmail.com",
    description="A keyframes and ffmpeg iframes extractor.",
    long_description="Long description",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["extract_keyframes=keyframes_extractor.cli_scripts:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)