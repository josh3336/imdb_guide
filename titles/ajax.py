from django.utils import simplejson
from dajaxice.core import dajaxice_functions, Dajaxice
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register



@dajaxice_register
def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})


def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()