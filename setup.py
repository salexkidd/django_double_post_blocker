from distutils.core import setup
from django_double_post_blocker import get_version

setup(
    name='django_double_post_blocker',
    version=get_version(),
    description='Prevents double POSTs when submitting forms.',
    long_description=open('README.rst').read(),
    author='salexkidd',
    author_email='salexkidd@gmail.com',
    url='https://github.com/salexkidd/django_double_post_blocker',
    packages=[
        'django_double_post_blocker',
        'django_double_post_blocker.middleware',
        'django_double_post_blocker.templatetags',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
