import setuptools

# Long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# Requirements
def get_requirements():
    return [
        "numpy>=1.17",
        "opencv-python>=4",
        "requests>=2.22"
    ]

setuptools.setup(
    name="video-kf",
    version="0.0.1",
    author="Antonio Verdone",
    author_email="averdones@gmail.com",
    description="A keyframes and ffmpeg iframes extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/averdones/video-kf",
    packages=setuptools.find_packages(),
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": ["video-kf=videokf.cli_scripts:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="keyframes iframes video extractor",
    python_requires=">=3.6"
)
