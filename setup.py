from setuptools import setup

setup(name='pymarkoff',
      author='Christopher Chen',
      author_email='christopher.chen1995@gmail.com',
      version='0.1.0',
      description="""A simple Markov chain modeller and generator aimed for word and sentence generation.""",
      long_description="Originally a proof of concept, I've used this in enough projects that I've decided to publish it tomake it easier to import.\n"
      "",
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Operating System :: OS Independent",
          "Intended Audience :: End Users/Desktop",
          "License :: Public Domain"

      ],
      keywords="math calculator utility command line reverse polish notation",
      url='https://bitbucket.org/TheCDC/pyrpn',
      license='Public Domain',
      packages=['pyrpncalc'],
      download_url="https://bitbucket.org/TheCDC/pyrpn/get/HEAD.zip",
      install_requires=[],
      scripts=["bin/pyrpncalc"],
      zip_safe=True)
