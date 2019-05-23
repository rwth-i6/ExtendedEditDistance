# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import re
import unicodedata
import sys
import os
import codecs

def preprocess(s):

    s = s.rstrip()  # trail space, tab, newlineの削除
   
    s = s.replace('.', ' .')
    s = s.replace('!', ' !')
    s = s.replace('?', ' ?')
    s = s.replace(',', ' ,')

    s = re.sub(r'\s+', r' ', s)  # スペースの個数正規化
    s = re.sub(r'(\d) ([.,]) (\d)', r'\1\2\3', s)  # 0 . 1 -> 0.1
    s = re.sub(r'(Dr|Jr|Prof|Rev|Gen|Mr|Mt|Mrs|Ms) .', r'\1.', s)  # Mr . -> Mr.
    s = s.replace(u'e . g .', u'e.g.')
    s = s.replace(u'i . e .', u'e.g.')
    s = s.replace(u'U . S .', u'U.S.')
    return s
"""
def preprocess_ja(s):
    s = s.rstrip()  # trail space, tab, newlineの削除
    s = unicodedata.normalize('NFKC', s)  # まず正規化
    return s


def preprocess(s, lang):
    funcname = 'preprocess_{0}'.format(lang)
    return globals()[funcname](s)


def split(s, lang):
    if lang == 'ja':
        return list(s)
    else:
        return s.split()
"""