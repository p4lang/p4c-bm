#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# -*- coding: utf-8 -*-

import sys
import tenjin


def render_template(out, name, context, templates_dir, prefix=None):
    """
    Render a template using tenjin.
    out: a file-like object
    name: name of the template
    context: dictionary of variables to pass to the template
    prefix: optional prefix for embedding (for other languages than python)
    """

    # support "::" syntax
    pp = [tenjin.PrefixedLinePreprocessor(prefix=prefix)
          if prefix else tenjin.PrefixedLinePreprocessor()]
    # disable HTML escaping
    template_globals = {"to_str": str, "escape": str}
    engine = TemplateEngine(path=[templates_dir], pp=pp, cache=False)
    out.write(engine.render(name, context, template_globals))


# We have not found a use for this yet, so excude it from cov report
class TemplateEngine(tenjin.Engine):  # pragma: no cover
    def include(self, template_name, **kwargs):
        """
        Tenjin has an issue with nested includes that use the same local
        variable names, because it uses the same context dict for each level of
        nesting.  The fix is to copy the context.
        """
        frame = sys._getframe(1)
        locals = frame.f_locals
        globals = frame.f_globals
        context = locals["_context"].copy()
        context.update(kwargs)
        template = self.get_template(template_name, context, globals)
        return template.render(context, globals, _buf=locals["_buf"])
