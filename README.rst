Django-search-admin-autocomplete
================================

.. image:: https://raw.githubusercontent.com/linevych/django-search-admin-autocomplete/master/doc/demo.gif

**This is a fork of** `django-search-admin-autocomplete <https://github.com/linevich/django-search-admin-autocomplete>`_ **(archived).** The original package is no longer maintained. This fork adds new features, modern Django support, and bug fixes.

Simple Django app that adds autocomplete search to the admin panel changelist view.

What's New
----------

- **Related field search**: Search across ForeignKey relations (e.g., ``client__name``, ``category__title``)
- **Django 4+ / 5+ support**: Fixed deprecated ``url()`` imports
- **Modern build system**: ``pyproject.toml`` with hatchling (no more ``setup.py``)
- **Python 3.8–3.13** support
- **Comprehensive test suite** (18 tests)

Requirements
============

- Python: 3.8+
- Django: 3.2+

Installation
============

.. code-block:: bash

    pip install django-search-admin-autocomplete

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'search_admin_autocomplete',
        ...
    ]

Usage
=====

Basic usage with direct fields:

.. code-block:: python

    from search_admin_autocomplete.admin import SearchAutoCompleteAdmin

    class MyModelAdmin(SearchAutoCompleteAdmin):
        search_fields = ['name', 'description']

    admin.site.register(MyModel, MyModelAdmin)

Related Field Support
=====================

Search across ForeignKey and related model fields using Django's ``__`` lookup syntax:

.. code-block:: python

    from search_admin_autocomplete.admin import SearchAutoCompleteAdmin

    class OrderAdmin(SearchAutoCompleteAdmin):
        search_fields = [
            'order_number',
            'client__name',        # ForeignKey → Client.name
            'client__email',       # ForeignKey → Client.email
            'category__title',     # ForeignKey → Category.title
        ]

    admin.site.register(Order, OrderAdmin)

The autocomplete will search and display values from both the model and its related models.

Configuration Options
=====================

.. code-block:: python

    class MyModelAdmin(SearchAutoCompleteAdmin):
        search_fields = ['name', 'client__name']
        search_prefix = '__icontains'  # Search operator (default: '__contains')
        max_results = 20               # Max autocomplete results (default: 10)

Customization
=============

If you have a custom ``change_list.html``:

**admin.py**

.. code-block:: python

    from search_admin_autocomplete.admin import SearchAutoCompleteAdmin

    class MyModelAdmin(SearchAutoCompleteAdmin):
        change_list_template = 'admin/custom-list.html'
        search_fields = ['name', 'client__title']

    admin.site.register(MyModel, MyModelAdmin)

**admin/custom-list.html**

.. code-block:: html

    {% extends 'search_admin_autocomplete/change_list.html' %}

    {% block object-tools %}
    Your custom html...
    {{ block.super }}
    {% endblock %}

Running Tests
=============

.. code-block:: bash

    cd example
    python manage.py test search_admin_autocomplete

Changelog
=========

0.3.0 (2026)
------------
- **Forked** from archived ``django-search-admin-autocomplete``
- Added support for related field lookups (e.g., ``client__name``)
- Updated for Django 4+ and 5+ compatibility
- Modernized package configuration with ``pyproject.toml``
- Added comprehensive test suite (18 tests)

0.2.1 and earlier
-----------------
- Original release by linevich (see `upstream repo <https://github.com/linevich/django-search-admin-autocomplete>`_)
