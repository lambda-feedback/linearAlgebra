from typing import Any, TypedDict
import numpy as np
from numpy import linalg as LA
#from evaluation_function_utils.errors import EvaluationException

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
    

    #empty set
    if is_empty(response) and is_empty(answer):
        return Result(is_correct=True)
    
    #different dimensions
    if len(response) != len(answer):
        return Result(is_correct=False)

    
    #set empty to zero and convert strings to floats
    response = to_floats(response)
    answer = to_floats(answer)

    #convert to numpy
    try:
        res = np.array(response, dtype=np.float32)
        ans = np.array(answer, dtype=np.float32)
    except Exception as e:
        #raise EvaluationException(f"Failed to parse user response", detail=repr(e))
        raise Exception(f"Failed to parse user response", detail=repr(e))
    
    if res.ndim == 1:
        res = np.array([res])
    if ans.ndim == 1:
        ans = np.array([ans])
    
    #transpose for easier access to columns
    #last column is constant     
    resconst = res[ :,-1]
    ansconst = ans[ :,-1]

    resspan = res[ :, :-1]
    ansspan = ans[ :, :-1]
    

    #check if vector space is equal
    if not equal_vector_space(resspan, ansspan):
        return Result(is_correct=False)

    #check if affine space is equal
    diff = resconst - ansconst

    #np.linalg.solve(ansspan, diff)
    residual = np.linalg.lstsq(ansspan, diff, rcond=None)[1]
    
    return Result(is_correct=np.allclose(residual, 0))



def is_empty(element):
    is_ok = False
    if isinstance(element,list):
        is_ok = all([is_empty(e) for e in element])
    elif element is None:
        is_ok = True
    elif isinstance(element,str):
        element = element.strip()
        if len(element) == 0:
            is_ok = True
    return is_ok

def to_floats(element):
    if isinstance(element,list):
        return [to_floats(e) for e in element]
    else:
        if isinstance(element,str):
            element = element.strip()
            if len(element) == 0 or element == "undefined":
                return 0
            else:
                element = float(element)
    return element

def equal_vector_space(v1, v2):
    m = np.hstack((v1,v2))

    return LA.matrix_rank(v1) == LA.matrix_rank(v2) and LA.matrix_rank(v2) == LA.matrix_rank(m)

