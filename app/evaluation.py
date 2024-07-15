from typing import Any, TypedDict


class Params(TypedDict):
    pass


class Result(TypedDict):
    is_correct: bool



def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """

    """
    Comments specific to working with linear algebra and the MATRIX response type
    ---
    If the matrix response type is used the response and answer parameters will be
    a list of lists where the inner list corresponds to a row in the matrix.
    It is also likely that it would be useful to have an input that only uses text,
    i.e. that can be used with the EXPRESSION type, but accepts a more varied and
    less clumsy syntax for defining matrices and vectors than sympy does, i.e.
    the input needs to be translated to convenient sympy syntax, and assumes that
    symbols are matrices or vectors rather than real numbers (though deciding how
    to let the user define the dimensions of the objects will require some thought).
    For different ways to define matrices in sympy, see 
    https://docs.sympy.org/latest/modules/matrices/matrices.html
    It is not necessary to implement both types of input if you only need one for
    the module you are puttin content in, it might even be better to make sure one
    type is supported robustly rather being able to handle both poorly.
    """

    return Result(is_correct=True)