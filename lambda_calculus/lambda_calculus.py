"""
Small library for working with very pure functional systems,
especially within the lambda calculus.

Note: it is recommended to convert all lambda expressions
to De Bruijn indexed form because
- it is a normal form that does not need alpha-conversion,
    and intensionally equivalent functions are guaranteed
    to be reported as equal
- the integer indexing scheme is much more efficient in
    this implementation, and the performance benefit may
    show for very deep evaluations
"""

owns_global_namespace = __name__ == '__main__'
module_prefix = '' if owns_global_namespace else __name__ + '.'

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
    """
    def __init__(self):
        """
        Initialize the bindings object with no variables bound.
        """
        import collections
        self.named = collections.ChainMap()
        self.indexed = []
    def __getitem__(self, index):
        """
        Get the bound value for a named or indexed variable.
        """
        if isinstance(index, str):
            return self.named[index]
        else:
            return self.indexed[-index]
    def append(self, index, value):
        """
        Add a new entry for a named or indexed variable.
        """
        if isinstance(index, str):
            self.named.maps = [{index:value}] + self.named.maps
        else:
            self.indexed.append(value)
    def pop(self, index):
        """
        Remove the most recent entry for a named or indexed variable.
        """
        if isinstance(index, str):
            self.named.maps.pop(0)
        else:
            self.indexed.pop()

class lambda_var(object):
    """
    Represents an occurence of a single variable.
    Stores the variable name, or an integer if De Bruijn indexing is used
    """
    pass # TODO

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
    def __eq__(self, other):
        """
        Performs a strict equality check,
        using variable name and expression.
        Will not consider alpha-converted variants to be equal.
        """
        if self is other:return True
        return hasattr(other, 'var_name') and \
               hasattr(other, 'expr') and \
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
        result = module_prefix + 'lambda_func(' + \
                 repr(self.var_name) + ', ' + \
                 repr(self.expr) + ')'
        return result
