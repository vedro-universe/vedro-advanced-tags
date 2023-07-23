# Vedro Advanced Tags

[![Codecov](https://img.shields.io/codecov/c/github/vedro-universe/vedro-advanced-tags/master.svg?style=flat-square)](https://codecov.io/gh/vedro-universe/vedro-advanced-tags)
[![PyPI](https://img.shields.io/pypi/v/vedro-advanced-tags.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-advanced-tags?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-advanced-tags.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)

## Installation

<details open>
<summary>Quick</summary>
<p>

For a quick installation, you can use a plugin manager as follows:

```shell
$ vedro plugin install vedro-advanced-tags
$ vedro plugin disable vedro.plugins.tagger
```

</p>
</details>

<details>
<summary>Manual</summary>
<p>

To install manually, follow these steps:

1. Install the package using pip:

```shell
$ pip3 install vedro-advanced-tags
```

2. Next, activate the plugin in your `vedro.cfg.py` configuration file:

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

</p>
</details>

## Usage

1. Adding tags to scenarios:

```python
import vedro

class Scenario(vedro.Scenario):
    subject = "register user"
    tags = ["P0", "API"]
```

2. Running tests based on the tags:

#### AND

If you want to run scenarios that include both `P0` and `API` tags, use the AND operator:

```shell
$ vedro run --tags "P0 and API"
```

#### OR

If you want to run scenarios containing either `API` or `CLI` tags, use the OR operator:

```shell
$ vedro run --tags "API or CLI"
```

#### NOT

To exclude scenarios with a specific tag, such as `P0`, use the NOT operator:

```shell
$ vedro run --tags "not P0"
```

#### Expressions

To run scenarios that meet complex conditions, you can use expressions. For example, if you want to run scenarios that either have the `API` or `CLI` tag, but do not have the `P0` tag, you can specify:

```shell
$ vedro run --tags "(API or CLI) and (not P0)"
```
