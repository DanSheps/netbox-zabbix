from setuptools import find_packages, setup

setup(
    name='netbox_zabbix',
    version='1.0.0',
    description='NetBox Zabbix Sync',
    long_description='Plugin to Sync to Zabbix',
    url='https://github.com/dansheps/netbox-zabbix/',
    download_url='https://github.com/dansheps/netbox-zabbix/',
    author='Daniel Sheppard',
    author_email='dans@dansheps.com',
    maintainer='Daniel Sheppard',
    maintainer_email='dans@dansheps.com',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPL v3',
    zip_safe=False,
    keywords=['netbox', 'netbox-plugin'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ]
)