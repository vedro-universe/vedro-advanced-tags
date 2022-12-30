# Vedro Advanced Tags

[![Codecov](https://img.shields.io/codecov/c/github/vedro-universe/vedro-advanced-tags/master.svg?style=flat-square)](https://codecov.io/gh/vedro-universe/vedro-advanced-tags)
[![PyPI](https://img.shields.io/pypi/v/vedro-advanced-tags.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-advanced-tags?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-advanced-tags.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)

## Installation

### 1. Install package

```shell
$ pip3 install vedro-advanced-tags
```

### 2. Enable plugin

```python
# ./vedro.cfg.py
import vedro
import vedro.plugins.tagger as tagger
import vedro_advanced_tags as adv_tagger

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class Tagger(tagger.Tagger):
            enabled = False  # disable default tagger

        class VedroAdvancedTags(adv_tagger.VedroAdvancedTags):
            enabled = True

```
