# -*- coding: utf-8 -*-
from html5lib import sanitizer, serializer, treebuilders, treewalkers
import html5lib


# HACK: somehow the html5lib parses uppercase tags as text elements.
# (see http://code.google.com/p/html5lib/issues/detail?id=47 )
# So we force the tokenizer to lowercase them first.
class BetterSanitizer(sanitizer.HTMLSanitizer):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "lowercaseElementName": True,
            "lowercaseAttrName": True,
        })
        super(BetterSanitizer, self).__init__(*args, **kwargs)


DEFAULT_PARSER = html5lib.HTMLParser(tokenizer=BetterSanitizer,
                                     tree=treebuilders.getTreeBuilder("dom"))


def clean_html(data, full=True, parser=DEFAULT_PARSER):
    """
    Cleans HTML from XSS vulnerabilities using html5lib

    If full is False, only the contents inside <body> will be returned (without
    the <body> tags).
    """
    if full:
        dom_tree = parser.parse(data)
    else:
        dom_tree = parser.parseFragment(data)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False,
                                                 quote_attr_values=True)
    return u''.join(s.serialize(stream))
