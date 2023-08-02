# Vedro Advanced Tags

[![Codecov](https://img.shields.io/codecov/c/github/vedro-universe/vedro-advanced-tags/master.svg?style=flat-square)](https://codecov.io/gh/vedro-universe/vedro-advanced-tags)
[![PyPI](https://img.shields.io/pypi/v/vedro-advanced-tags.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-advanced-tags?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-advanced-tags.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-advanced-tags/)

(!) Starting from [Vedro v1.10](https://vedro.io/blog/whats-new-vedro-v1.10), the default Tagger plugin supports boolean logic in tags. Therefore, you don't need to install `vedro-advanced-tags` if you're using Vedro version 1.10 or later. You can use the boolean logic in tags in the same way as in `vedro-advanced-tags`.

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

First, add tags to your scenarios:

```python
import vedro

class Scenario(vedro.Scenario):
    subject = "register user"
    tags = ["P0", "API"]
```

Then, you can run scenarios with specific tags.

#### AND

To run scenarios that include both specified tags, use the **and** operator:

```shell
$ vedro run --tags "P0 and API"
```

#### OR

To run scenarios that contain either of the specified tags, use the **or** operator:

```shell
$ vedro run --tags "API or CLI"
```

#### NOT

To run scenarios that do not include a specific tag, use the **not** operator:

```shell
$ vedro run --tags "not P0"
```

#### EXPR

To run scenarios that meet multiple conditions, use expressions.

For instance, to execute scenarios that either include the `API` or `CLI` tag, and do not include the `P0` tag, you can use:

```shell
$ vedro run --tags "(API or CLI) and (not P0)"
```
