# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

######################### IMPORTANT ##########################################################
##
##   DO NOT EDIT THIS FILE UNLESS REALLY NECESSARY
##   IF YOU WISH TO DO SO, CONTACT ALEKSANDAR PETROV FIRST
##
######################### IMPORTANT ##########################################################

############################# NODE MODULE SETUP ##############################################
#
# STRONGLY RECOMMENDED NOT TO EDIT THIS
#
# This part creates a temporary module in a temporary folder that contains all
# node classes in the repo. This is necessary for the autodocs functionality as it
# works well only with Python modules. These node classes can then be used as `nodes.SomeNode`.
#
###############################################################################################

import tempfile
from shutil import copyfile

module_name = 'nodes'

# Create the temporary module dir
dirpath = tempfile.mkdtemp()
module_dir = os.path.join(dirpath, module_name)
os.makedirs(module_dir)

# Get the list of repositories
with open('repositories.txt') as f:
    repositories = f.readlines()
repositories = [repo.split('/')[1].split(':')[0] for repo in repositories]
print("REPOSITORIES: ", repositories)


print("LOOKING FOR NODE SOURCE FILES")
# Find all the nodes and move them to the temp module folder
node_source_files = []
for repo in repositories:
    for pkg in os.listdir(os.path.abspath('repositories/%s/packages/'%repo)):
        # Add the include paths such that all the include modules can also be used with autodocs
        sys.path.insert(0, os.path.abspath('repositories/%s/packages/%s/include' % (repo,pkg)))
        if os.path.isdir(os.path.abspath('repositories/%s/packages/%s/src' % (repo,pkg))):
            for node_source_file in os.listdir(os.path.abspath('repositories/%s/packages/%s/src' % (repo,pkg))):
                if node_source_file[-3:] == '.py' and node_source_file != '__init__.py':
                    node_source_files.append('repositories/%s/packages/%s/src/%s' % (repo, pkg, node_source_file))
                    copyfile('repositories/%s/packages/%s/src/%s' % (repo, pkg, node_source_file),
                             os.path.join(module_dir, node_source_file))

# Create an __init__.py file for the temporary module
with open(os.path.join(module_dir, '__init__.py'), 'w') as init_file:
    for node_source_file in node_source_files:
        init_file.write('from .%s import *\n' % (node_source_file.split('/')[-1][:-3]))

# Add the temporary module to the paths
sys.path.insert(0, dirpath)

############################# END OF NODE MODULE SETUP #########################################

print("Final system path directories:")
print(sys.path)
sys.setrecursionlimit(1500)


# -- Project information -----------------------------------------------------

project = 'Duckietown API'
copyright = 'Duckietown'
author = 'Duck Quackermann'

# The full version, including alpha/beta/rc tags
version = 'daffy'
release = version


# -- General configuration ---------------------------------------------------


# Napoleon (for Google-style docstrings)
extensions = ['sphinxcontrib.napoleon']

# Autodocs
extensions += ['sphinx.ext.autodoc']


# Load all the necesary mock imports
with open('mock_imports') as f:
    autodoc_mock_imports = f.readlines()
for idx in range(len(autodoc_mock_imports)):
    autodoc_mock_imports[idx] = autodoc_mock_imports[idx].strip(' ').strip('\n')

# Appearance settings (PLEASE REFRAIN FROM EDITING THESE)
autodoc_default_flags = {'members': True,
                         'member-order': 'alphabetical',
                         'undoc-members': True,
                         'inherited-members': True,
                         'show-inheritance': True}
add_module_names = False

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = [('Configuration', 'Parameters'),
                            ('Subscribers', 'Parameters'),
                            ('Subscriber', 'Parameters'),
                            ('Publishers', 'Parameters'),
                            ('Publisher', 'Parameters'),
                            ('Services', 'Parameters'),
                            ('Service', 'Parameters'),
                            ('Fields', 'Parameters'),
                            ('Attribute', 'Parameters'),
                            ('Attributes', 'Parameters'),
                            ('inputs', 'Parameters'),
                            ('input', 'Parameters'),
                            ('outputs', 'Parameters'),
                            ('output', 'Parameters'),
                            ]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Set the index page
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    # 'canonical_url': '',
    # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    # 'logo_only': False,
    # 'display_version': True,
    'prev_next_buttons_location': 'bottom',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    'style_nav_header_background': '#fbc10b',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': False,
    'titles_only': False,
    # 'github_url': True
}

html_logo = "logo_textonly.png"
html_favicon = "favicon.png"
# html_style = 'dt_style.css'



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
