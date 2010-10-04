from setuptools import setup, find_packages
import sys, os

version = '0.1'

long_description = open('README.markdown').read()

setup(name='PylonsTemplates',
      version=version,
      description="Extra paster templates for Pylons including repoze.what implementation",
      long_description=long_description,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Framework :: Pylons",
          "Framework :: Paste",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Utilities",
      ],
      keywords='',
      author='Jason Stitt, Andrey Petrov',
      author_email='jason@countergram.com, andrey.petrov@shazow.net',
      url='http://countergram.com/software/PylonsTemplates',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "Pylons>=0.9.7",
          "PasteScript>=1.6.3",
      ],
      entry_points="""
      [paste.paster_create_template]
      pylons_repoze_what = PylonsTemplates:PylonsRepozeWhat
      pylons_cleaner_default = PylonsTemplates:PylonsCleanerDefault
      pylons_dotcloud = PylonsTemplates:PylonsDotCloud
      """,
      )
