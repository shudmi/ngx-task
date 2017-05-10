from setuptools import find_packages, setup

setup(
    name='ngx-task',
    version='0.2',
    description='Testimonial for candidates to show up their code-foo',
    author='Dmitry Shulyak',
    author_email='dmitri.shulyak@gmail.com',
    url='https://github.com/shudmi/ngx-task',
    classifiers=[
        'License :: Apache License 2.0',
        'Programming Language :: Python',
        'Programming Language :: Python 3',
        'Programming Language :: Python 3.4',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    tests_require=[
        "pytest==3.0.7",
    ],
    entry_points="""
        [console_scripts]
        ngx_generate=ngx_task.cli:generate_data
        ngx_process=ngx_task.cli:process_data
    """
)
