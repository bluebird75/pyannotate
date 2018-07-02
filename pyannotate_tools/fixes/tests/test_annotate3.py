# flake8: noqa
# Our flake extension misfires on type comments in strings below.

from lib2to3.tests.test_fixers import FixerTestCase
import unittest

# deadcode: fix_annotate is used as part of the fixer_pkg for this test
from pyannotate_tools.fixes import fix_annotate3


class TestFixAnnotate3(FixerTestCase):

    def setUp(self):
        super(TestFixAnnotate3, self).setUp(
            fix_list=["annotate3"],
            fixer_pkg="pyannotate_tools",
        )

    def test_no_arg(self) :
        a = """\
            def nop():
                return 42
            """
        b = """\
            from typing import Any
            def nop() -> Any:
                return 42
            """
        self.check(a, b)

        ### Check many variations of the base syntax
        a2 = """\
            def nop(): return 42
            """
        b2 = """\
            from typing import Any
            def nop() -> Any: return 42
            """
        self.check(a2, b2)

        a3 = """\
            def nop(
                    ): 
                return 42
            """
        b3 = """\
            from typing import Any
            def nop(
                    ) -> Any: 
                return 42
            """
        self.check(a3, b3)

        a4 = """\
            def nop(
                    )   \
                    : 
                return 42
            """
        b4 = """\
            from typing import Any
            def nop(
                    ) -> Any   \
                    : 
                return 42
            """
        self.check(a4, b4)

        a5 = """\
            def nop(    # blah
                    ):  # blah
                return 42 # blah
            """
        b5 = """\
            from typing import Any
            def nop(    # blah
                    ) -> Any:  # blah
                return 42 # blah
            """
        self.check(a5, b5)

        a6 = """\
            def nop(    # blah
                    )   \
                    :   # blah
                return 42 # blah
            """
        b6 = """\
            from typing import Any
            def nop(    # blah
                    ) -> Any   \
                    :   # blah
                return 42 # blah
            """
        self.check(a6, b6)


    def test_one_arg(self):
        a = """\
            def incr(arg):
                return arg+1
            """
        b = """\
            from typing import Any
            def incr(arg: Any) -> Any:
                return arg+1
            """
        self.check(a, b)


        a2 = """\
            def incr(arg=0):
                return arg+1
            """
        b2 = """\
            from typing import Any
            def incr(arg: int=0) -> Any:
                return arg+1
            """
        self.check(a2, b2)

    def test_two_args(self):
        a = """\
            def add(arg1, arg2):
                return arg1+arg2
            """
        b = """\
            from typing import Any
            def add(arg1: Any, arg2: Any) -> Any:
                return arg1+arg2
            """
        self.check(a, b)

        a2 = """\
            def add(arg1=0, arg2=0.1):
                return arg1+arg2
            """
        b2 = """\
            from typing import Any
            def add(arg1: int=0, arg2: float=0.1) -> Any:
                return arg1+arg2
            """
        self.check(a2, b2)

        a3 = """\
            def add(arg1, arg2=0.1):
                return arg1+arg2
            """
        b3 = """\
            from typing import Any
            def add(arg1: Any, arg2: float=0.1) -> Any:
                return arg1+arg2
            """
        self.check(a3, b3)

    def test_defaults(self):
        a = """\
            def foo(iarg=0, farg=0.0, sarg='', uarg=u'', barg=False):
                return 42
            """
        b = """\
            from typing import Any
            def foo(iarg: int=0, farg: float=0.0, sarg: str='', uarg: unicode=u'', barg: bool=False) -> Any:
                return 42
            """
        self.check(a, b)

        a2 = """\
            def foo(iarg=0, farg=0.0, sarg='', uarg=u'', barg=False, targ=(1,2,3)):
                return 42
            """
        b2 = """\
            from typing import Any
            def foo(iarg: int=0, farg: float=0.0, sarg: str='', uarg: unicode=u'', barg: bool=False, targ: Any=(1,2,3)) -> Any:
                return 42
            """
        self.check(a2, b2)

        a3 = """\
            def foo(iarg=0, farg, sarg='', uarg, barg=False, targ=(1,2,3)):
                return 42
            """
        b3 = """\
            from typing import Any
            def foo(iarg: int=0, farg: Any, sarg: str='', uarg: Any, barg: bool=False, targ: Any=(1,2,3)) -> Any:
                return 42
            """
        self.check(a3, b3)

    def test_staticmethod(self):
        a = """\
            class C:
                @staticmethod
                def incr(self):
                    return 42
            """
        b = """\
            from typing import Any
            class C:
                @staticmethod
                def incr(self: Any) -> Any:
                    return 42
            """
        self.check(a, b)

    def test_classmethod(self):
        a = """\
            class C:
                @classmethod
                def incr(cls, arg):
                    return 42
            """
        b = """\
            from typing import Any
            class C:
                @classmethod
                def incr(cls, arg: Any) -> Any:
                    return 42
            """
        self.check(a, b)

    def test_instancemethod(self):
        a = """\
            class C:
                def incr(self, arg):
                    return 42
            """
        b = """\
            from typing import Any
            class C:
                def incr(self, arg: Any) -> Any:
                    return 42
            """
        self.check(a, b)

    def test_fake_self(self):
        a = """\
            def incr(self, arg):
                return 42
            """
        b = """\
            from typing import Any
            def incr(self: Any, arg: Any) -> Any:
                return 42
            """
        self.check(a, b)

    def test_nested_fake_self(self):
        a = """\
            class C:
                def outer(self):
                    def inner(self, arg):
                        return 42
            """
        b = """\
            from typing import Any
            class C:
                def outer(self) -> None:
                    def inner(self: Any, arg: Any) -> Any:
                        return 42
            """
        self.check(a, b)

    def test_multiple_decorators(self):
        a = """\
            class C:
                @contextmanager
                @classmethod
                @wrapped('func')
                def incr(cls, arg):
                    return 42
            """
        b = """\
            from typing import Any
            class C:
                @contextmanager
                @classmethod
                @wrapped('func')
                def incr(cls, arg: Any) -> Any:
                    return 42
            """
        self.check(a, b)

    def test_stars(self):
        a = """\
            def stuff(*a):
                return 4, 2
            """
        b = """\
            from typing import Any
            def stuff(*a: Any) -> Any:
                return 4, 2
            """
        self.check(a, b)

        a1 = """\
            def stuff(a, *b):
                return 4, 2
            """
        b1 = """\
            from typing import Any
            def stuff(a: Any, *b: Any) -> Any:
                return 4, 2
            """
        self.check(a1, b1)


        
    def test_keywords(self):
        a = """\
            def stuff(**kw):
                return 4, 2
            """
        b = """\
            from typing import Any
            def stuff(**kw: Any) -> Any:
                return 4, 2
            """
        self.check(a, b)

        a1 = """\
            def stuff(a, **kw):
                return 4, 2
            """
        b1 = """\
            from typing import Any
            def stuff(a: Any, **kw: Any) -> Any:
                return 4, 2
            """
        self.check(a1, b1)

        a2 = """\
            def stuff(a, *b, **kw):
                return 4, 2
            """
        b2 = """\
            from typing import Any
            def stuff(a: Any, *b: Any, **kw: Any) -> Any:
                return 4, 2
            """
        self.check(a2, b2)

        a3 = """\
            def stuff(*b, **kw):
                return 4, 2
            """
        b3 = """\
            from typing import Any
            def stuff(*b: Any, **kw: Any) -> Any:
                return 4, 2
            """
        self.check(a3, b3)

    def test_no_return_expr(self):
        a = """\
            def proc1(arg):
                return
            def proc2(arg):
                pass
            """
        b = """\
            from typing import Any
            def proc1(arg: Any) -> None:
                return
            def proc2(arg: Any) -> None:
                pass
            """
        self.check(a, b)

    def test_nested_return_expr(self):
        # The 'return expr' in inner() shouldn't affect the return type of outer().
        a = """\
            def outer(arg):
                def inner():
                    return 42
                return
            """
        b = """\
            from typing import Any
            def outer(arg: Any) -> None:
                def inner() -> Any:
                    return 42
                return
            """
        self.check(a, b)

    def test_nested_class_return_expr(self):
        # The 'return expr' in class Inner shouldn't affect the return type of outer().
        a = """\
            def outer(arg):
                class Inner:
                    return 42
                return
            """
        b = """\
            from typing import Any
            def outer(arg: Any) -> None:
                class Inner:
                    return 42
                return
            """
        self.check(a, b)

    def test_add_import(self):
        a = """\
            import typing
            from typing import Callable

            def incr(arg):
                return 42
            """
        b = """\
            import typing
            from typing import Callable
            from typing import Any

            def incr(arg: Any) -> Any:
                return 42
            """
        self.check(a, b)

    def test_dont_add_import(self):
        a = """\
            def nop(arg=0):
                return
            """
        b = """\
            def nop(arg: int=0) -> None:
                return
            """
        self.check(a, b)

    def test_long_form(self):
        self.maxDiff = None
        a = """\
            def nop(arg0, arg1, arg2, arg3, arg4,
                    arg5, arg6, arg7, arg8=0, arg9='',
                    *args, **kwds):
                return
            """
        b = """\
            from typing import Any
            def nop(arg0: Any, arg1: Any, arg2: Any, arg3: Any, arg4: Any,
                    arg5: Any, arg6: Any, arg7: Any, arg8: int=0, arg9: str='',
                    *args: Any, **kwds: Any) -> None:
                return
            """
        self.check(a, b)

    def test_long_form_trailing_comma(self):
        self.maxDiff = None
        a = """\
            def nop(arg0, arg1, arg2, arg3, arg4, arg5, arg6,
                    arg7=None, arg8=0, arg9='', arg10=False,):
                return
            """
        b = """\
            from typing import Any
            def nop(arg0: Any, arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any, arg6: Any,
                    arg7: Any=None, arg8: int=0, arg9: str='', arg10: bool=False,) -> None:
                return
            """
        self.check(a, b)

    def test_one_liner(self):
        a = """\
            class C:
                def nop(self, a): a = a; return a
                # Something
            # More
            pass
            """
        b = """\
            from typing import Any
            class C:
                def nop(self, a: Any) -> Any: a = a; return a
                # Something
            # More
            pass
            """
        self.check(a, b)

    def test_idempotency_long_1arg(self):
        a = """\
            def nop(a  # type: int
                    ):
                pass
            """
        self.unchanged(a)

    def test_idempotency_long_1arg_comma(self):
        a = """\
            def nop(a,  # type: int
                    ):
                pass
            """
        self.unchanged(a)

    def test_idempotency_long_2args_first(self):
        a = """\
            def nop(a,  # type: int
                    b):
                pass
            """
        self.unchanged(a)

    def test_idempotency_long_2args_last(self):
        a = """\
            def nop(a,
                    b  # type: int
                    ):
                pass
            """
        self.unchanged(a)

    def test_idempotency_long_varargs(self):
        a = """\
            def nop(*a  # type: int
                    ):
                pass
            """
        self.unchanged(a)

    def test_idempotency_long_kwargs(self):
        a = """\
            def nop(**a  # type: int
                    ):
                pass
            """
        self.unchanged(a)
