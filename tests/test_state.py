from nose.tools import eq_, assert_raises

from fabric.state import _AliasDict, _AttributeDict


def test_dict_aliasing():
    """
    Assigning values to aliases updates aliased keys
    """
    ad = _AliasDict(
        {'bar': False, 'biz': True, 'baz': False},
        aliases={'foo': ['bar', 'biz', 'baz']}
    )
    # Before
    eq_(ad['bar'], False)
    eq_(ad['biz'], True)
    eq_(ad['baz'], False)
    # Change
    ad['foo'] = True
    # After
    eq_(ad['bar'], True)
    eq_(ad['biz'], True)
    eq_(ad['baz'], True)


def test_nested_dict_aliasing():
    """
    Aliases can be nested
    """
    ad = _AliasDict(
        {'bar': False, 'biz': True},
        aliases={'foo': ['bar', 'nested'], 'nested': ['biz']}
    )
    # Before
    eq_(ad['bar'], False)
    eq_(ad['biz'], True)
    # Change
    ad['foo'] = True
    # After
    eq_(ad['bar'], True)
    eq_(ad['biz'], True)


def test_dict_alias_expansion():
    """
    Alias expansion
    """
    ad = _AliasDict(
        {'bar': False, 'biz': True},
        aliases={'foo': ['bar', 'nested'], 'nested': ['biz']}
    )
    eq_(ad.expand_aliases(['foo']), ['bar', 'biz'])


def test_resolve_variable():
    """
    Variable expansion
    """
    e = _AttributeDict({
        'a': {
            'b': {
                'c': '$(g.h)bar',
                'd': [
                    [
                        {
                            'e': 'foo$(i)!'
                        }
                    ]
                ],
                'f': '$(j)'
            },

        },
        'g': {
            'h': 'foo'
        },
        'i': 'bar',
        'j': 'ham'
    })

    assert_raises(KeyError, e.__getitem__, 'x.y')  # KeyError
    eq_(e.resolve('a.b.c.x', default='def'), 'def')  # Default
    eq_(e.resolve('a.b.c'), 'foobar')  # Variable
    eq_(e.resolve('a.b.c.f'), 'ham')  # Parent fallback
    eq_(e.resolve('c', prefix='a.b'), 'foobar')  # Prefix
    eq_(e.resolve('a.b'), {  # Resolved dict/list
        'c': 'foobar',
        'd': [[{'e': 'foobar!'}]],
        'f': 'ham'
    })
    assert_raises(KeyError, e.__getitem__, 'x.y')
