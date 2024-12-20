from setuptools import setup, find_packages

setup(
    name='nse_topic_segmentation',                     # Name of your package
    version='0.1',                         # Version number
    packages=find_packages(),             # Automatically find all packages

    # install_requires=[                    # List any external dependencies
    #     'numpy',                           # Example: replace with actual dependencies
    #     'requests',
    # ],

    # entry_points={                         # Optional: if your package has CLI commands
    #     'console_scripts': [
    #         'my-command=my_package.module1:main',  # command will call my_package.module1.main
    #     ],
    # },

    include_package_data=True,             # Include non-Python files (like README, etc.)
    long_description=open('README.md').read(),  # Add long description from README
    long_description_content_type='text/markdown',  # Specify markdown for README
    author='Anton Chernov',
    author_email='tony-pitchblack@yandex.ru',
    url='https://github.com/tony-pitchblack/NSE-TopicSegmentation',  # Link to your repo
    license='MIT',
)