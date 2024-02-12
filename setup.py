from setuptools import setup, find_packages



f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='godaddy_ddns',
    description='godaddy dynamic dynamic dns client',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='PanosRCng',
    author_email='panosrcng@gmail.com',
    url='https://cloud.panosrcng.com/gogs/godaddy_ddns',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup']),
    entry_points="""
        [console_scripts]
        godaddy_ddns = godaddy_ddns.godaddy_ddns:main
    """,
)
