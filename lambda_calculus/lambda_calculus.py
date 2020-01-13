"""
Small library for working with very pure functional systems,
especially within the lambda calculus.

Important usage notes:
- The lambda calculus is Turing complete and capable of arbitrary
  computation, including non-halting programs and wasting all your
  computing resources. If this is being used seriously instead of
  as a playground ie. on a server, ensure you have strict safeguards.
- Lazy evaluation is used for all the lambda objects.
  This behaviour is hidden to the typical user, however, if you are
  diving deeper and working with the lambda objects, know that
  most computation is deferred until you call .evaluate_now()
- The De Bruijn indexed form is the canonical form here.
  It is a useful normal form. Under the current implementation,
  it will always evaluate correctly, unlike the named form,
  where name collisions may sometimes cause functions to behave
  in unexpected ways. For this reason, we strictly forbid
  directly evaluating the named form.
- String forms of lambda expressions are LaTeX-compatible
  (outputs from str) and LaTeX-like (input to parse_lambda).
  Outputs of str will generally reconstruct the object
  exactly when parsed, though strange variable names
  may interfere with the parsing logic and cause
  a different object to be constructed.
"""

# pregenerate some random data which will be used to initialize constants
from random import SystemRandom as sr
random = sr()

# 64-bit hash mask
_hash_mask = 2**64 - 1
# multipliers for Rabin hash
_hash_key = tuple(random.getrandbits(64) for _ in range(2))

# get rid of the random generator now that we don't need it anymore
del sr
del random

# ---
# Internal utilties
# ---

def _hash_combine(hash_state, value):
    """
    Combines a hash state and a single hash value:
    (S, V) --> S'
    Modifies the hash state in-place.

    Algorithm parameters:
    hash state - 128 bits as 2-tuple
    key - 128 bits as 2-tuple
    value - 64 bits as single value

    As currently implemented, uses a 2-round generalized
    Feistel network, backed by Python's built-in hash
    for tuples, which is expected to have sufficient
    mixing and nonlinearity properties.
    The implementation may change at any time.
    """
    hash_state[0] ^= hash((hash_state[1], _hash_key[0], value))
    hash_state[1] ^= hash((hash_state[0], _hash_key[1], value))

def _hash_uncombine(hash_state, value):
    """
    Inverts _hash_combine:
    (S', V) --> S
    """
    hash_state[1] ^= hash((hash_state[0], _hash_key[1], value))
    hash_state[0] ^= hash((hash_state[1], _hash_key[0], value))

def _name_generator():
    """
    The current name generator, which is an iterable.
    Will generate the same sequence every time,
    but may change in future versions.
    In the current implementation,
    uses a counter and writes the variable names as
    x_{n}.
    """
    import itertools
    return map((lambda n:'x_{'+str(n)+'}'), itertools.count())

# ---
# lambda objects, low level API
# ---

class lambda_bind(object):
    """
    Represents a collection of variable bindings.
    Contains both a ChainMap for named bindings
    and a list for indexed bindings.
    Will be modified in-place by lambda function evaluations,
    and should be emptied again when a function evaluation completes.

    It may be confusing why named bindings
    use a ChainMap instead of a regular dict.
    Simply put, we cannot guarantee variable names are unique.
    Even if the original expression has no duplicates,
    a function evaluation which results in recursive evaluations
    will cause a namespace collision,
    and we need the innermost scope to take priority,
    but not discard the outer scope's variable value once the inner scope ends.

    Hash values are kept as part of the state and updated along with the
    update operations. This way, the hash operation can be O(1),
    at O(1) extra cost when updating. More specifically, a 128-bit internal
    hash state is maintained, and this is also used for equality checks.
    """
    def __init__(self, adds=None):
        """
        Initialize the bindings object with no variables bound.
        If state is given, initializes using it instead.
        """
        import collections
        self.named = collections.ChainMap()
        self.indexed = []
        self._adds = []
        self._hash = [0]*2
        self += adds
    def __getitem__(self, index):
        """
        Get the bound value for a named or indexed variable.

        If fails, raises a KeyError.
        """
        try:
            if isinstance(index, str):
                return self.named[index]
            else:
                return self.indexed[-index]
        except IndexError as exc:
            raise KeyError(exc)
    def append(self, index, value):
        """
        Add a new entry for a named or indexed variable.
        """
        if isinstance(index, str):
            self.named.maps = [{index:value}] + self.named.maps
        else:
            self.indexed.append(value)
        self._adds.append(index)
        # update hash
        hash_add = hash((index, value))
        _hash_combine(self._hash, hash_add)
    def pop(self):
        """
        Remove the most recent entry for a named or indexed variable,
        and return the value.
        """
        index = self._adds.pop()
        if isinstance(index, str):
            value = next(iter(
                self.named.maps.pop(0)
                .values()))
        else:
            value = self.indexed.pop()
        # update hash
        hash_add = hash((index, value))
        _hash_uncombine(self._hash, hash_add)
        # return popped value
        return value
    def __len__(self):
        """
        How many variables have been bound?
        Will correctly report variables with the same name as separate.
        """
        return len(self._adds)
    def keep_first(self, n):
        """
        Pop until len(self) <= n
        Effectively trims away inner bindings all at once in a known outer scope.
        """
        while len(self) > n:
            self.pop()
    def flatten(self, destructive=False):
        """
        Get a list of (index, value) tuples which
        can be used to reconstruct this object.
        If destructive flag is set to True, will
        be somewhat faster, and this object will be
        emptied by the end.
        """
        adds = []
        while self:
            index = self._adds[-1]
            value = self.pop()
            adds.append((index, value))
        adds = adds[::-1]
        if not destructive:
            for index, value in adds:
                self.append(index, value)
        return adds
    def __add__(self, other):
        """
        Concatenates this bindings object with another.
        The bindings for the other object (right operand)
        will come after the bindings for this object (left operand),
        so the new newest binding is the newest binding
        of the right operand.
        """
        # make a new bindings object and add in all the data
        result = lambda_bind()
        result += self
        result += other
        return result
    def __iadd__(self, other):
        """
        Concatenates this bindings object with another,
        in place. See docs for __add__ for more details
        on how the concatenation operation behaves.
        """
        # quickly get past zero-like cases
        if not other:
            return self
        # flatten down a bindings object into a substitution list
        if isinstance(other, lambda_bind):
            other = other.flatten()
        # append every substitution
        for index, value in other:
            self.append(index, value)
        return self
    def __str__(self):
        """
        Generates a substitution list.
        By convention, square brackets are used to surround the substitutions,
        and substitutions are written as NAME := VALUE
        Indexed values just use the value instead.
        Note that for named substitutions, there may actually be more
        substitutions with the same variable name,
        but only the most recent/innermost will be shown.
        """
        bits = []
        for k, v in self.named.items():
            bits.append(str(k) + ' := ' + str(v))
        for v in self.indexed:
            bits.append(str(v))
        result = ', '.join(bits)
        result = '[' + result + ']'
        return result
    def __repr__(self):
        result = 'lambda_bind(' + \
                 repr(self.flatten()) + ')'
        return result
    def __bool__(self):
        return len(self) != 0
    def __eq__(self, other):
        """
        Checks for equality.
        Instead of doing a full equality check,
        will check the hash internal state.
        """
        if self is other:return True
        return isinstance(other, lambda_bind) and \
               self._hash == other._hash
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(tuple(self._hash))

class lambda_expr(object):
    """
    Base class for lambda expressions.
    Acts in some ways as an abstract base class
    by declaring functions to be implemented.
    Also provides some common "default" implementations
    of functions and wrappers to simplify child class
    implementations.
    """
    def to_named(self, name_iter=None, name_stack=None):
        """
        Converts this lambda expression to a named form.

        Actually a wrapper around ._to_named(name_iter, name_stack)

        Naming scheme may change unexpectedly;
        current implementation uses a counter and hexadecimal.
        """
        if name_iter is None:
            name_iter = iter(_name_generator())
        if name_stack is None:
            name_stack = []
        return self._to_named(name_iter, name_stack)
    def to_indexed(self, name_stack=None):
        """
        Converts this lambda expression to De Bruijn indexed form.

        Actually a wrapper around ._to_indexed(name_stack)
        """
        if name_stack is None:
            name_stack = []
        return self._to_indexed(name_stack)
    def evaluate_now(self, binds=None):
        """
        Force full evaluation now, and return the evaluated lambda expression.

        Actually a wrapper around ._evaluate_now(binds)
        """
        if binds is None:
            binds = lambda_bind()
        return self._evaluate_now(binds)
    def call(self, arg, binds=None):
        """
        Call this value with some other value.
        """
        result = lambda_call(self, arg)
        if binds:
            result = lambda_subs(result, binds, len(binds))
        return result
    
class lambda_var(lambda_expr):
    """
    Represents an occurence of a single variable.
    Stores the variable name, or an integer if De Bruijn indexing is used
    """
    def __init__(self, var_name):
        """
        Construct the variable by name or De Bruijn index.
        """
        self.var_name = var_name
        self._hash = hash((lambda_var, var_name))
    def __hash__(self):
        return self._hash
    def __eq__(self, other):
        """
        Checks if the other is also a variable with the same name.
        """
        if self is other:return True
        return isinstance(other, lambda_var) and \
               hash(self) == hash(other) and \
               self.var_name == other.var_name
    def __ne__(self, other):
        return not (self == other)
    def __str__(self):
        """
        Returns the variable name.
        """
        return str(self.var_name)
    def __repr__(self):
        return 'lambda_var(' + repr(self.var_name) + ')'
    def _to_named(self, name_iter, name_stack):
        """
        Underlying function for the wrapped .to_named()
        """
        new_name = name_stack[-self.var_name]
        return lambda_var(new_name)
    def _to_indexed(self, name_stack):
        """
        Underlying function for the wrapped .to_indexed()
        """
        if isinstance(self.var_name, int):
            return self
        new_name = len(name_stack) - name_stack.index(self.var_name)
        return lambda_var(new_name)
    def _evaluate_now(self, binds):
        """
        Underlying function for the wrapped .evaluate_now()
        """
        if not binds:
            return self
        try:
            # can we substitute?
            result = binds[self.var_name]
            # prevent infinite recursion from substituting with itself
            if result == self:
                return self
            # we may not be done yet, keep going recursively
            return result.evaluate_now(binds)
        except KeyError:
            # no substitution possible, that's it
            return self

class lambda_call(lambda_expr):
    """
    Represents a function call which was declared but not evaluated.
    The function may or may not be a lambda_func object.

    For example, in this lambda expression:
      \\lambda x. x x
    The sub-expression "x x" would be represented by a lambda_call,
    since it is a yet unevaluated function call.

    One instance will only represent a single function call:
    func(arg) for some func, arg.
    Nesting these is capable of representing any call tree.
    While we could compress the tree, it is currently not
    demanded for performance, so this single pair implementation
    is good enough.
    """
    def __init__(self, func, arg):
        """
        Initialize this object to represent the function call
        func(arg)
        """
        self.func = func
        self.arg = arg
        self._hash = hash((lambda_call, func, arg))
    def __hash__(self):
        return self._hash
    def __eq__(self, other):
        if self is other:return True
        return isinstance(other, lambda_call) and \
               hash(self) == hash(other) and \
               self.func == other.func and \
               self.arg == other.arg
    def __ne__(self, other):
        return not (self == other)
    def __str__(self):
        """
        Returns a LaTeX compatible string unambiguiously
        representing this function call,
        and which may be passed to parse_lambda to reconstruct it.
        """
        return '(' + str(self.func) + ' ' + str(self.arg) + ')'
    def __repr__(self):
        return 'lambda_call(' + repr(self.func) + \
               ', ' + repr(self.arg) + ')'
    def _to_named(self, name_iter, name_stack):
        """
        Underlying function for the wrapped .to_named()
        """
        return lambda_call(
            self.func.to_named(name_iter, name_stack),
            self.arg.to_named(name_iter, name_stack)
            )
    def _to_indexed(self, name_stack):
        """
        Underlying function for the wrapped .to_indexed()
        """
        return lambda_call(
            self.func.to_indexed(name_stack),
            self.arg.to_indexed(name_stack)
            )
    def _evaluate_now(self, binds):
        """
        Underlying function for the wrapped .evaluate_now()
        """
        # immediate evaluation of function and argument
        func = self.func.evaluate_now(binds)
        arg = self.arg.evaluate_now(binds)
        # and then call, but don't evaluate yet
        # if this is unable to evaluate further, it will just
        # wrap in a lambda_call object
        result = func.call(arg)
        # prevent infinite recursion by stopping when nothing changes
        if result == self:
            return self
        # keep going and recursively evaluate
        # bindings were already processed, so no bindings done here
        return result.evaluate_now()

class lambda_subs(lambda_expr):
    """
    Represents an expression with substitutions,
    where the substitutions have yet to be evaluated.
    Behaves like the other types, when needed.
    Simplifies implementation and improves performance.
    """
    def __init__(self, expr, binds, mark=None):
        """
        Represents expr with the given substitutions,
        where the immediately outside scope uses only
        the first <mark> bindings.
        After evaluation, all bindings after the mark
        will be removed.
        """
        if mark is None:
            mark = len(binds)
        self.expr = expr
        self.binds = binds
        self.mark = mark
        self._hash = hash((expr, binds, mark))
    def __hash__(self):
        return self._hash
    def __eq__(self, other):
        if self is other:return True
        return isinstance(other, lambda_subs) and \
               hash(self) == hash(other) and \
               self.mark == other.mark and \
               self.binds == other.binds and \
               self.expr == other.expr
    def __ne__(self, other):
        return not (self == other)
    def __str__(self):
        """
        Returns a LaTeX compatible string representing
        this expression with substitution.
        This is not allowed by the parser.
        Be warned as well that ordered substitutions
        and multiple substitutions are not standard
        in mathematics.
        """
        return str(self.expr) + str(self.binds)
    def __repr__(self):
        return 'lambda_subs(' + repr(self.expr) + \
               ', ' + repr(self.binds) + \
               ', ' + repr(self.mark) + ')'
    def to_named(self, name_iter=None, name_stack=None):
        """
        Converts this expression and all sub-expressions recursively
        to use the named form, and returns the new function.
        If already in named form, does nothing.

        Naming scheme may change unexpectedly;
        current implementation uses a counter and hexadecimal.
        """
        if name_iter is None:
            return iter(_name_generator())
        if name_stack is None:
            name_stack = []
        return lambda_call(
            self.func.to_named(name_iter, name_stack),
            self.arg.to_named(name_iter, name_stack)
            )
    def _to_named(self, name_iter, name_stack):
        """
        Would normally convert to named form,
        but not supported for a substitution object.
        """
        raise TypeError('Cannot refactor a substitution object' \
                        '(of type lambda_subs) to named form')
    def _to_indexed(self, name_stack):
        """
        Would normally convert to indexed form,
        but not supported for a substitution object.
        """
        raise TypeError('Cannot refactor a substitution object' \
                        '(of type lambda_subs) to De Bruijn indexed form')
    def _evaluate_now(self, binds):
        """
        Force full evaluation now, and return the
        evaluated lambda expression.

        Since this object is a substitution object,
        it handles a lot of the hard work.
        """
        # we must append our bindings
        mark = len(binds) + self.mark
        binds += self.binds
        # apply substitutions to the expression
        result = self.expr.evaluate_now(binds)
        # unroll back to the mark to remove
        # substitutions that have gone out of scope
        binds.keep_first(mark)
        # return result
        return result

class lambda_func(lambda_expr):
    """
    Represents a unary function in the lambda calculus.
    The actual data it stores are:
    - the bound variable name, or None if De Bruijn indexing is used
    - the expression to be evaluated
    """
    def __init__(self, var_name, expr):
        """
        Constructs a lambda function,
        given a variable name to bind (or None to use De Bruijn indexing)
        and an expression to be evaluated.
        
        Please do not use this directly,
        as the internal behaviour of this class is somewhat confusing.
        """
        self.var_name = var_name
        self.expr = expr
        self._hash = hash((lambda_func, var_name, expr))
    def __hash__(self):
        return self._hash
    def __eq__(self, other):
        """
        Performs a strict equality check,
        using variable name and expression.
        Will not consider alpha-converted variants to be equal.
        """
        if self is other:return True
        return isinstance(other, lambda_func) and \
               hash(self) == hash(other) and \
               self.var_name == other.var_name and \
               self.expr == other.expr
    def __ne__(self, other):
        return not (self == other)
    def __str__(self):
        """
        Returns a LaTeX compatible string unambiguiously
        representing this lambda function,
        and which may be passed to parse_lambda to reconstruct it.
        """
        bits = ['\\lambda']
        if self.var_name is not None:
            bits.append(self.var_name)
        bits.append('.')
        bits.append(str(self.expr))
        result = ' '.join(bits)
        result = '(' + result + ')'
        return result
    def __repr__(self):
        result = 'lambda_func(' + \
                 repr(self.var_name) + ', ' + \
                 repr(self.expr) + ')'
        return result
    def _to_named(self, name_iter, name_stack):
        """
        Underlying function for the wrapped .to_named()
        """
        if isinstance(self.var_name, str):
            return self
        new_name = next(name_iter)
        name_stack.append(new_name)
        result = lambda_func(new_name, self.expr.to_named(name_iter, name_stack))
        name_stack.pop()
        return result
    def _to_indexed(self, name_stack):
        """
        Underlying function for the wrapped .to_indexed()
        """
        if self.var_name is None:
            return self
        name_stack.append(self.var_name)
        result = lambda_func(None, self.expr.to_indexed(name_stack))
        name_stack.pop()
        return result
    def _evaluate_now(self, binds):
        """
        Underlying function for the wrapped .evaluate_now()
        """
        if not binds:
            return self
        # take advantage of the already existing
        # lambda_subs class to take care of helping
        # to propagate the substitutions
        alt_expr = lambda_subs(self.expr, binds)
        # modify binds in-place
        binds.append(
            self.var_name,
            lambda_var(self.var_name if self.var_name is not None else 1)
            )
        # we expect lambda_subs to also unroll back the binds
        alt_expr = alt_expr.evaluate_now()
        # construct the new altered function
        result = lambda_func(
            self.var_name,
            alt_expr
            )
        return result
    def _require_callable(self):
        """
        Ensures that this function can be called without error.
        If this does any work, will warn, because at call time
        is not when we should be doing conversion work.
        """
        if self.var_name is not None:
            import warnings
            warnings.warn('Function evaluation must first convert to indexed form. ' \
                          'Consider saving the named form to remove the need to convert' \
                          'it again every time the function is called.',
                          category=ResourceWarning)
            self = self.to_indexed()
        return self
    def call(self, arg, binds=None):
        """
        Call this value with some other value.
        """
        if binds is None:
            binds = lambda_bind()
        self = self._require_callable()
        unroll_to = len(binds)
        binds.append(self.var_name, arg)
        return lambda_subs(self.expr, binds, unroll_to)
    def __call__(self, *args):
        """
        For convenience: call the function with some arguments
        and correct currying.
        Does whatever conversions are necessary along the way.
        """
        self = self._require_callable()
        for arg in args:
            self = self.call(arg)
        self = self.evaluate_now()
        return self

# ---
# parsing API and helpers
# ---

# map common left brackets to right brackets
_right_brackets = {
    '(':')',
    '[':']',
    '{':'}',
    }
# regex that matches exactly a lone lambda
_regex_lambda = '^\\\\?(?:lambda|λ|Λ)$'

def _stream_prepend(rem, stream):
    """
    Return an iterator which will first exhaust the
    characters of rem and then iterate from stream.

    Useful for when we accidentally read more characters
    that should actually be handled by other code.
    
    Expected to be implemented efficiently
    such that there is no "dead" overhead,
    as in, if N strings have been prepended
    so far and also exhausted,
    the total overhead for the iterator is O(1)
    more than just the original stream by itself.
    Currently backed by itertools.chain
    """
    import itertools
    return itertools.chain(rem, stream)

def _parse_lambda_var(istr):
    """
    Convert a string to a lambda_var object.
    If possible, makes it an integer.
    """
    try:
        var_name = int(istr)
    except ValueError:
        var_name = istr
    return lambda_var(var_name)

def _parse_latex_raw(stream, pre='', collect_alpha=False, end=None):
    """
    Parse some LaTeX-like term, and return the string exactly.
    More specifically, reads in some substring S,
    and returns (V, R, E),
    where V is what we interpreted as a LaTeX term as a string,
    R is what we consumed but did not use,
    and E is a flag that is True if
    the end is due to reaching the end character
    and False if it is because we found the end of
    this one term.
    Guarantees:
    - V + R = S, unless E is true, in which case the end
        character is not included in R
    - V is not empty
    """
    try:
        # pre whitespace and non-whitespace
        pre_ws = []
        pre_content = list(pre)
        # post tags
        tags = []
        # unconsumed remaining stuff
        rem = []
        # flag for if we never hit the end character
        no_end = True
        # read until the first non-whitespace or end
        while not pre_content:
            c = next(stream)
            if c == end:
                return ''.join(pre_ws), '', True
            if c <= ' ':
                pre_ws.append(c)
            else:
                pre_content.append(c)
        # what was our character?
        fc = pre_content[-1]
        if fc == '\\':
            # started with \
            # parse a full command
            # command uses latin letters
            c = next(stream)
            while 'A' <= c <= 'Z' or 'a' <= c <= 'z':
                pre_content.append(c)
                c = next(stream)
            if c == end:
                return ''.join(pre_ws) + ''.join(pre_content), '', True
            rem.append(c)
        elif '0' <= fc <= '9':
            # started with a digit
            # parse a number
            c = next(stream)
            while '0' <= c <= '9':
                pre_content.append(c)
                c = next(stream)
            if c == end:
                return ''.join(pre_ws) + ''.join(pre_content), '', True
            rem.append(c)
        elif fc in '([{':
            # it's a bracket!
            # match the other bracket
            rb = _right_brackets[fc]
            # parse everything inside the brackets
            sub, subrem, hit_end = _parse_latex_raw(stream, end=rb)
            while not hit_end:
                pre_content.append(sub)
                sub, subrem, hit_end = _parse_latex_raw(stream, pre=subrem, end=rb)
            pre_content.append(rb)
        elif fc in '_^':
            # not normally allowed, but we'll parse it anyway
            # because we can
            rem.append(pre_content.pop())
        else:
            # started with something else, like a letter
            # no further processing to do, unless the flag says so
            if collect_alpha:
                c = next(stream)
                while 'A' <= c <= 'Z' or 'a' <= c <= 'z':
                    pre_content.append(c)
                    c = next(stream)
                if c == end:
                    return ''.join(pre_ws) + ''.join(pre_content), '', True
                rem.append(c)
        # keep going until we hit something we can't handle
        while True:
            exit_now = False
            # load stuff into rem until it has something in it
            while not rem or rem[-1] <= ' ':
                c = next(stream)
                if c == end:
                    no_end = False
                    exit_now = True
                    break
                rem.append(c)
            if exit_now:
                break
            # if we are not meant to handle it, stop here
            if rem[-1] not in '_^':
                break
            # okay, we can actually deal with this
            # push it over to the tags group and parse a single token after
            tags += rem
            sub, subrem, hit_end = _parse_latex_raw(stream, end=end)
            tags.append(sub)
            rem = list(subrem)
            if hit_end:
                no_end = False
                break
    except StopIteration as exc:
        # only ignore the exception if we expected it
        if end is not None:
            raise exc
        no_end = False
    return ''.join(pre_ws) + ''.join(pre_content) + ''.join(tags), \
           ''.join(rem), \
           not no_end

def _parse_lambda_func(stream, end=None):
    """
    Read in a lambda function.
    Assumes we already read the lambda at the start.
    After the function declaration, defers back to
    _parse_lambda_expr.
    """
    c = next(stream)
    while c <= ' ':
        c = next(stream)
    if c == end:
        raise ValueError('Lambda function definition in brackets is empty.')
    first, rem, hit_end = _parse_latex_raw(stream, pre=c, end=end)
    if hit_end:
        raise ValueError('Lambda function definition in brackets is incomplete. ' \
                         'No dot or variable found.')
    stream = _stream_prepend(rem, stream)
    if first == '.':
        # using De Bruijn indexed form, no variable declaration
        var_name = None
    else:
        var_name = first
        # that was the variable declaration, now let's look for the dot
        c = next(stream)
        while c <= ' ':
            c = next(stream)
        if c != '.':
            raise ValueError('Lambda function definition does not have ' \
                             'variable followed by a dot.')
    body = _parse_lambda_expr(stream, end=end)
    return lambda_func(var_name, body)

def _parse_lambda_expr(stream, end=None):
    """
    Parse as much as we can and return a lambda_expr object.
    """
    import functools
    import re
    # try to get the first token to identify the type of expression
    c = ''
    while c <= ' ':
        c = next(stream)
    # if we hit the end, this is an error
    if c == end:
        raise ValueError('Tried to parse an empty sub-expression. ' \
                         'You may have brackets with nothing between them.')
    hit_end = False
    # is it a bracket?
    if c in '([{':
        # okay, we parse stuff in the brackets
        # as a full term
        terms = [_parse_lambda_expr(stream, end=_right_brackets[c])]
    # probably some kind of token then
    else:
        stream = _stream_prepend(c, stream)
        first, rem, hit_end = _parse_latex_raw(stream, collect_alpha=True, end=end)
        # is the first thing exactly lambda?
        if re.match(_regex_lambda, first):
            # okay, we just entered a function
            # pass it over to the function parser
            stream = _stream_prepend(rem, stream)
            return _parse_lambda_func(stream, end=end)
        # treat it as a variable literal then
        # we have to redo the parsing because
        # this interpretation might be wrong
        rem = first + rem
        if hit_end:
            rem += end or ''
        stream = _stream_prepend(rem, stream)
        first, rem, hit_end = _parse_latex_raw(stream, collect_alpha=False, end=end)
        stream = _stream_prepend(rem, stream)
        terms = [_parse_lambda_var(first)]
    # if we hit the end, stop here
    if hit_end:
        return terms[0]
    # parse more terms
    try:
        while True:
            # read until not whitespace
            c = next(stream)
            while c <= ' ':
                c = next(stream)
            # detect end
            if c == end:
                break
            # repeat the term parsing logic, but slightly different
            # is it a bracket?
            if c in '([{':
                # okay, we parse stuff in the brackets
                # as a full term
                terms.append(_parse_lambda_expr(stream, end=_right_brackets[c]))
            # probably some kind of token then
            else:
                stream = _stream_prepend(c, stream)
                first, rem, hit_end = _parse_latex_raw(stream, collect_alpha=True, end=end)
                # is the first thing exactly lambda?
                if re.match(_regex_lambda, first):
                    # okay, we just entered a function
                    # pass it over to the function parser
                    stream = _stream_prepend(rem, stream)
                    terms.append(_parse_lambda_func(stream, end=end))
                    break
                # treat it as a variable literal then
                # we have to redo the parsing because
                # this interpretation might be wrong
                rem = first + rem
                if hit_end:
                    rem += end or ''
                stream = _stream_prepend(rem, stream)
                first, rem, hit_end = _parse_latex_raw(stream, collect_alpha=False, end=end)
                stream = _stream_prepend(rem, stream)
                terms.append(_parse_lambda_var(first))
                # this may be the end
                if hit_end:
                    break
    except StopIteration as exc:
        # only ignore the exception if we expected it
        if end is not None:
            raise exc
    # combine left to right as call
    term = functools.reduce(lambda_call, terms)
    return term

def lambda_parse(stream):
    """
    Given a character iterator, parse a lambda expression
    from it, of type lambda_expr.
    Can also take string inputs.
    
    Compatible with some LaTeX formatted inputs,
    but does not support all of LaTeX, only a subset which
    is generally sufficient for parsing these lambda
    expressions. Mostly behaves LaTeX-like, but will
    treat a number as a single symbol rather than each
    digit as a separate symbol.
    
    Does not actually evaluate the expression.

    Aliased to lambda_parse and parse_lambda.
    """
    if isinstance(stream, str):
        it = iter(stream)
        result = lambda_parse(it)
        # under normal circumstances, all characters are consumed
        return result
    try:
        result = _parse_lambda_expr(stream)
        return result
    except StopIteration:
        raise ValueError('Parser unexpected ran out of characters to parse. ' \
                         'The input string or stream is not a valid lambda expression.')

# make an alias
parse_lambda = lambda_parse
