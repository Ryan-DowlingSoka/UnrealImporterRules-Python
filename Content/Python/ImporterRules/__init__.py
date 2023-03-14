# MIT License

# Copyright (c) 2023 Ryan DowlingSoka

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Importer Rules is a simple, bare bones, python frame work for handling data transformations on imported assets on import. 
A user can define a "Rule" by ascribing "Queries" that the incoming asset must match before subsequent "Actions" are applied.
You can write your own rules, queries, and actions or use the existing generic ones to modify assets that need updating.
"""

from ImporterRules.Manager import importer_rules_manager
from ImporterRules.Actions import SetEditorProperties, SetAssetTags
from ImporterRules.Queries import SourcePath, DestinationPath
from ImporterRules.Rules import Rule