import os
import subprocess

def generate_sphinx_docs(package_name, source_dir="docs/source", build_dir="docs/build"):
    """
    Automatically generate Sphinx documentation for a Python package.

    :param package_name: The name or path of the package to document.
    :param source_dir: The directory to store the .rst files (default: docs/source).
    :param build_dir: The directory to store the built HTML files (default: docs/build).
    """    
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    conf_py_path = os.path.join(source_dir, "conf.py")
    if not os.path.exists(conf_py_path):
        print("Creating conf.py...")
        with open(conf_py_path, "w") as f:
            f.write(f"""
import os
import sys
sys.path.insert(0, os.path.abspath('../../')) 

# Configuration file for the Sphinx documentation builder.
project = '{package_name}'
author = 'Your_author_name'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]
templates_path = ['_templates']
exclude_patterns = []

# HTML output theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['./docs/build/_static']
""")

    # Generates .rst files
    print(f"Running sphinx-apidoc for {package_name}...")
    sphinx_apidoc_cmd = [
        "sphinx-apidoc", 
        "-o", source_dir,  
        "-f", 
        "-e", 
        package_name   
    ]
    subprocess.run(sphinx_apidoc_cmd, check=True)

    # Generates index.rst
    index_rst = os.path.join(source_dir, "index.rst")

    print("Creating index.rst...")
    with open(index_rst, "w") as f:
        f.write(f"""
{package_name} Documentation
============================

.. toctree::
   :maxdepth: 30
   :caption: Contents:

   {package_name}
""")
            
    # Generates and overwrites my_package.rst dynamically
    my_package_rst_path = os.path.join(source_dir, f"{package_name}.rst")
    print(f"Creating {package_name}.rst...")
    with open(my_package_rst_path, "w") as f:
        f.write(f"""
{package_name} Package
===================

Submodules
----------

.. toctree::
   :maxdepth: 30

""")
            
        package_dir = os.path.join(os.path.dirname(__file__), package_name) 
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_rel_path = os.path.relpath(root, package_dir)
                    if module_rel_path == ".":
                        module_name = f"{package_name}.{file[:-3]}"
                    else:
                        module_name = f"{package_name}.{module_rel_path.replace(os.sep, '.')}.{file[:-3]}"
                    f.write(f"   {module_name}\n")

    # Generates HTML documentation
    print("Building HTML documentation with sphinx-build...")
    sphinx_build_cmd = [
        "sphinx-build",
        "-b", "html",       
        source_dir,         
        build_dir       
    ]
    subprocess.run(sphinx_build_cmd, check=True)

    print(f"Documentation built successfully in {build_dir}")


if __name__ == "__main__":
    generate_sphinx_docs("my_package")