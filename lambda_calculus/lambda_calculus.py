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

    Hash and comparison are implemented, but not considered a common use case,
    so they are not highly optimized. If it turns out that hashing or
    equality is a significant performance issue, we will change the code
    with a trade-off: hash intermediate values will be part of the state
    and all update operations will take slightly more work to also update
    the hash values, and thus the hash method becomes O(1) instead of O(N).
    """
    def __init__(self, state=None):
        """
        Initialize the bindings object with no variables bound.
        If state is given, initializes using it instead.
        """
        import collections
        self.named = collections.ChainMap()
        self.indexed = []
        self._adds = []
        if state is not None:
            self.named, self.indexed, self._adds = state
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
        _adds.append(index)
    def pop(self):
        """
        Remove the most recent entry for a named or indexed variable.
        """
        index = self._adds.pop()
        if isinstance(index, str):
            self.named.maps.pop(0)
        else:
            self.indexed.pop()
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
                 repr([self.named, self.indexed, self._adds]) + ')'
        return result
    def __bool__(self):
        return len(self) != 0
    def __eq__(self, other):
        if self is other:return True
        return isinstance(other, lambda_bind) and \
               self._adds == other._adds and \
               self.named == other.named and \
               self.indexed == other.indexed
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        named_hash = hash(tuple(map(
            (lambda d:tuple(d.items())),
            self.named.maps
            )))
        return hash((
            lambda_bind,
            named_hash,
            tuple(self.indexed),
            tuple(self._adds)
            ))

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
            import itertools
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
    """
    pass # TODO

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
            import itertools
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
