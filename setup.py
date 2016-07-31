from setuptools import setup

setup(name='pymarkoff',
      author='Christopher Chen',
      author_email='christopher.chen1995@gmail.com',
      version='0.1.0',
      description="""A simple Markov chain modeller and generator aimed for word and sentence generation.""",
      long_description=open("README.md").read(),
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Operating System :: OS Independent",
      ],
      keywords="markov chain model generator",
      url='https://bitbucket.org/TheCDC/pymarkoff',
      license='Public Domain',
      packages=['pymarkoff'],
      download_url="https://bitbucket.org/TheCDC/pymarkoff/get/HEAD.zip",
      install_requires=[],
      zip_safe=True)
