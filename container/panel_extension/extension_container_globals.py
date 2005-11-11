'''
extension_container_globals module
(c) 2005 travis f vachon

extension_container_globals provides functions and attributes that
are designed to be used by all of the modules in the panel_extension
package
'''
from os.path import expandvars

extension_dir = expandvars("$HOME/.panelextensions/")
