# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import types
from copy import deepcopy
from collections import Mapping

from exceptions import TagError


class Attrs(dict):
    MULTI_VALUES_ATTRS = ('klass', 'typ')

    def __init__(self):
        self['style'] = {}

    def __setitem__(self, key, value):
        if key in self.MULTI_VALUES_ATTRS:
            if key not in self:
                super(Attrs, self).__setitem__(key, [])
            self[key].append(value)
        else:
            super(Attrs, self).__setitem__(key, value)

    def update(self, other=None, **kwargs):
        if other is not None:
            for k, v in other.iteritems() if isinstance(other, Mapping) else other:
                self[k] = v
        for k, v in kwargs.iteritems():
            self[k] = v


class TagContainer(object):
    _void = False

    def __init__(self):
        self.childs = []
        self.parent = None

    def __call__(self, *args, prepend=False):
        for arg in args:
            if type(arg) in (
                types.ListType,
                types.TupleType,
                types.GeneratorType,
            ):
                for tag in arg:
                    self.__call__(tag)
            elif isinstance(arg, Tag):
                self._add_to_childs(arg, prepend=prepend)
            else:
                if not prepend:
                    self.childs.append(arg)
                else:
                    self.childs.insert(0, arg)
        return self

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def _add_to_childs(self, tag, prepend=False):
        if not prepend:
            self.childs.append(tag)
        else:
            self.childs.insert(0, tag)
        tag.parent = self
        tag._tab_count = self._tab_count + 1
        tag._own_index = self.childs.index(tag)

    def after(self, other):
        self.parent.childs.insert(self._own_index + 1, other)
        return self

    def before(self, other):
        self.parent.childs.insert(self._own_index - 1, other)
        return self

    def prepend(self, *childs):
        return self(*childs, prepend=True)

    def prepend_to(self, father):
        return father.prepend(self)

    def append(self, *childs):
        return self(*childs)

    def append_to(self, father):
        return father.append(self)

    def remove(self):
        self.parent.childs.pop(self._own_index)
        return self

    def pop(self, i=0):
        self.childs.pop(i).parent = None
        return self

    def empty(self):
        for child in self.childs:
            self.childs.remove()
        return self

    def children(self):
        return filter(lambda x: isinstance(x, Tag), self.childs)

    def filter(self, pattern):
        # TODO
        pass

    def find(self, pattern):
        # TODO
        pass

    def first(self):
        return self.childs[0]

    def last(self):
        return self.childs[-1]

    @property
    def length(self):
        return len(self.childs)

    def has(self, pattern):
        # TODO
        # return pattern or tag in self.childs
        pass

    def next(self):
        return self.parent.child[self._own_index + 1]

    def prev(self):
        return self.parent.child[self._own_index - 1]

    def prev_all(self):
        return self.parent.child[:self._own_index - 1]

    def parent(self):
        return self.parent

    def siblings(self):
        return filter(lambda x: isinstance(x, Tag), self.parent.childs)

    def slice(self, start, end):
        return self.childs[start:end]


class Tag(TagContainer):
    _template = '<{tag}{attrs}>{inner}</{tag}>'
    _needed = None

    SPECIAL_ATTRS = {
        'klass': 'class',
        'typ': 'type'
    }

    def __init__(self, **kwargs):
        self._own_index = None
        self.attrs = Attrs()
        self.data = {}
        self.style = {}
        if self._needed and not set(self._needed).issubset(set(kwargs)):
            raise TagError()
        self.attr(**kwargs)
        self._tab_count = 0
        super(Tag, self).__init__()

    def index(self):
        return self._own_index

    def attr(self, other=None, **kwargs):
        self.attrs.update(other or kwargs)
        return self

    def prop(self, other=None, **kwargs):
        return self.attr(other, **kwargs)

    def remove_attr(self, attr):
        self.attrs.pop(attr, None)
        return self

    def remove_prop(self, attr):
        self.attrs.pop(attr, None)
        return self

    def add_class(self, cssclass):
        self.attrs['klass'].append(cssclass)
        return self

    def remove_class(self, cssclass):
        self.attrs['klass'].remove(cssclass)
        return self

    def clone(self):
        return deepcopy(self)

    def remove(self):
        del self

    def contents(self):
        return self.childs

    def css(self):
        #TODO
        pass

    def hide(self):
        self.attrs['style']['display'] = None
        return self

    def show(self):
        self.attrs['style'].pop('display')
        return self

    def toggle(self):
        return self.show() if self.attrs['style']['display'] == None else self.hide()

    def data(self, key, value=None):
        if value:
            self.data[key] = value
            return self
        else:
            return self.data[key]

    def has_class(self, cssclass):
        return cssclass in self.attrs['klass']

    def toggleClass(self, cssclass):
        return self.remove_class(cssclass) if self.has_class(cssclass) else self.add_class(cssclass)

    def html(self):
        return self._render_childs()

    def is_a(self, pattern):
        #TODO
        # return true if self == pattern
        pass

    def replace_all():
        #TODO
        pass

    def replace_with(self, other):
        if isinstance(other, Tag):
            self = other
        else:
            raise TagError()
        return self

    def wrap(self, other):
        return self.before(other.append(self)).parent.pop(self._own_index)

    def wrap_inner(self, other):
        self.childs

    def text(self):
        return ''.join(child.text() for child in self.childs if isinstance(child, Tag) else child)

    def render(self, pretty=False):
        prettying = '\t' * self._tab_count + '\n'
        tag_data = {
            'tag': getattr(self, '_{}__tag'.format(self.__class__.__name__)),
            'attrs': ''.join(' {}="{}"'.format(self.SPECIAL_ATTRS.get(k, k), v) for k, v in self.attrs.iteritems())
        }
        if not self._void:
            tag_data['inner'] = self._render_childs(pretty)
        template = self._template + prettying if pretty else self._template
        return template.format(**tag_data)

    def _render_childs(self, pretty):
        return ''.join(child.render(pretty) if isinstance(child, Tag) else str(child) for child in self.childs)


class VoidTag(Tag):
    _void = True
    _template = '<{tag}{attrs}/>'
