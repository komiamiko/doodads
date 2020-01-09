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
- While the De Bruijn indexed form is a useful normal form,
  we do not currently support direct evaluation of the De Bruijn forms.
"""

# pregenerate some random data which will be used to initialize constants
from random import SystemRandom as sr
random = sr()

# 64-bit hash mask
_hash_mask = 2**64 - 1
# multipliers for Rabin hash
_hash_mul = [random.getrandbits(64) & ~4 | 1 for _ in range(2)]
# multiplicative inverses mod 2^64
_hash_mul_inv = [pow(v,2**62-1,2**64) for v in _hash_mul]

# get rid of the random generator now that we don't need it anymore
del sr
del random

def _name_generator():
    """
    The current name generator, which is an iterable.
    Will generate the same sequence every time,
    but may change in future versions.
    In the current implementation, uses a counter and converts
    the numbers to hexadecimal.
    """
    return map((lambda n:format(n,'X')), itertools.count())

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
        self._hash = [hash((v, lambda_bind)) for v in _hash_mul]
        if adds is not None:
            for index, value in adds:
                self.append(index, value)
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
        for i in range(len(self._hash)):
            self._hash[i] = (self._hash[i] * _hash_mul[i] + hash_add) & _hash_mask
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
        for i in range(len(self._hash)):
            self._hash[i] = ((self._hash[i] - hash_add) * _hash_mul_inv[i]) & _hash_mask
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
        
    def __add__(self, other):
        """
        Concatenates this bindings object with another.
        The bindings for the other object (right operand)
        will come after the bindings for this object (left operand),
        so the new newest binding is the newest binding
        of the right operand.
        """
        import collections
        named = collections.ChainMap(*other.named.maps, *self.named.maps)
        indexed = self.indexed + other.indexed
        _adds = self._adds + other._adds
        return lambda_bind([named, indexed, _adds])
    def __str__(self):
        """
        Generates a substitution list.
        By convention, square brackets are used to surround the substitutions,
        and substitutions are written as NAME := VALUE
        Indexed values just use the value instead.
        """
        bits = []
        for k, v in self.named:
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

class lambda_var(object):
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
        return self.var_name
    def __repr__(self):
        return 'lambda_var(' + repr(var_name) + ')'
    def to_named(self, name_iter=None, name_stack=None):
        """
        Converts this variable to a named form.

        Naming scheme may change unexpectedly;
        current implementation uses a counter and hexadecimal.
        """
        if isinstance(self.var_name, str):
            return self
        if name_iter is None:
            return iter(_name_generator())
        if name_stack is None:
            name_stack = []
        new_name = name_stack[-self.var_name]
        return lambda_var(new_name)
    def to_indexed(self, name_stack=None):
        """
        Converts this variable to De Bruijn indexed form.
        """
        if isinstance(self.var_name, int):
            return self
        if name_stack is None:
            name_stack = []
        new_name = len(name_stack) - name_stack.index(self.var_name)
        return lambda_var(new_name)
    def evaluate_now(self, binds=None):
        """
        Force full evaluation now, and return the evaluated lambda expression.
        """
        if not binds:
            return self
        try:
            # can we substitute?
            result = binds[self.var_name]
            # we may not be done yet, keep going recursively
            return result.evaluate_now(binds)
        except KeyError:
            # no substitution possible, that's it
            return self
    def call(self, arg, binds):
        """
        Call this value with some other value.
        Substitutions are deferred.
        """
        result = self
        result = lambda_call(result, arg)
        if binds:
            result = lambda_subs(result, binds, len(binds))
        return result

class lambda_call(object):
    """
    Represents a function call which was declared but not evaluated.
    The function may or may not be a lambda_func object.

    For example, in this lambda expression:
      \lambda x. x x
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
    def __eq__(self):
        if self is other:return True
        return isinstance(other, lambda_call) and \
               hash(self) == hash(other) and \
               self.func == other.func and \
               self.arg == other.arg
    def __ne__(self):
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
    def to_indexed(self, name_stack=None):
        """
        Converts this expression and all sub-expressions recursively
        to use De Bruijn indexing, and returns the new function.
        If already in De Bruijn indexed form, does nothing.
        """
        if name_stack is None:
            name_stack = []
        return lambda_call(
            self.func.to_indexed(name_stack),
            self.arg.to_indexed(name_stack)
            )
    def evaluate_now(self, binds=None):
        """
        Force full evaluation now, and return the evaluated lambda expression.
        """
        # immediate evaluation of function and argument
        func = self.func.evaluate_now(binds)
        arg = self.arg.evaluate_now(binds)
        # and then call, but don't evaluate yet
        # if this is unable to evaluate further, it will just
        # wrap in a lambda_call object
        result = func.call(arg, binds)
        # prevent infinite recursion by stopping when nothing changes
        if result == self:
            return self
        # keep going and recursively evaluate
        # bindings were already processed, so no bindings done here
        return result.evaluate_now()
    def call(self, arg, binds):
        """
        Call this value with some other value.
        """
        result = lambda_call(self, arg)
        if binds:
            result = lambda_subs(result, binds, len(binds))
        return result

class lambda_subs(object):
    """
    Represents an expression with substitutions,
    where the substitutions have yet to be evaluated.
    Behaves like the other types, when needed.
    Simplifies implementation and improves performance.
    """
    pass # TODO

class lambda_func(object):
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
    def to_named(self, name_iter=None, name_stack=None):
        """
        Converts this function and all sub-expressions recursively
        to use the named form, and returns the new function.
        If already in named form, does nothing.

        Naming scheme may change unexpectedly;
        current implementation uses a counter and hexadecimal.
        """
        if isinstance(self.var_name, str):
            return self
        if name_iter is None:
            return iter(_name_generator())
        if name_stack is None:
            name_stack = []
        new_name = next(name_iter)
        name_stack.append(new_name)
        result = lambda_func(new_name, expr.to_named(name_iter, name_stack))
        name_stack.pop()
        return result
    def to_indexed(self, name_stack=None):
        """
        Converts this function and all sub-expressions recursively
        to use De Bruijn indexing, and returns the new function.
        If already in De Bruijn indexed form, does nothing.
        """
        if self.var_name is None:
            return self
        if name_stack is None:
            name_stack = []
        name_stack.append(self.var_name)
        result = lambda_func(None, expr.to_indexed(name_iter, name_stack))
        name_stack.pop()
        return result
    def evaluate_now(self, binds=None):
        """
        Force full evaluation now, and return the evaluated lambda expression.
        """
        if not binds:
            return self
        return lambda_func(
            self.var_name,
            self.call(lambda_var(self.var_name), binds).evaluate_now()
            )
    def call(self, arg, binds):
        """
        Call this value with some other value.
        """
        if self.var_name is None:
            raise TypeError('Direct call with De Bruijn indexing is not supported. Please convert to named first.')
        unroll_to = len(binds)
        binds.append(self.var_name, args)
        return lambda_lazy(self.expr, binds, unroll_to)
    def __call__(self, *args):
        """
        For convenience: call the function with some arguments
        and correct currying.
        Does whatever conversions are necessary along the way.
        """
        if self.var_name is None:
            import warnings
            warnings.warn('Function evaluation must first convert to named form. ' \
                          'Consider saving the named form to remove the need to convert it again every time the function is called.')
            self = self.to_named()
        for arg in args:
            self = self.call(arg, lambda_bind())
        self = self.evaluate_now()
        return self
