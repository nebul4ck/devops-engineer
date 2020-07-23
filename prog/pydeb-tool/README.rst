*****
PyDeb
*****

Python to Debian package converter.

Usage
#####

1. Make a requirements file with your project dependencies.

2. Make a directory to save .deb packages.

3. Use our tool:

.. code:: console

    cd /path/to/pydeb/
    ./pydeb_main.py -r requirements.txt -p /usr/bin/python3 -d /path/to/download_dir/


.. note::

    To execute pydeb like a script, you need python3.5 installed in your system. Alternatively, you can use traditional invocation: python3 pydeb_main ...


    
