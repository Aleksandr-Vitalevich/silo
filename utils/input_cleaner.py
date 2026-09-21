from functools import wraps

def clean_inputs(func) :
    '''Декоратор принимает функцию и выполняет чистку полей от пробелов с начала и конца строки'''
    @wraps(func)
    def wrapper(*args,**kwargs) :
        '''Функция обертка'''
        try :
            cleaned_args = tuple(arg.strip() if isinstance(arg,str) else arg for arg in args)
            cleaned_kwargs = {}
            for key,value in kwargs.items() :
                if isinstance(value,str) :
                    cleaned_kwargs[key] = value.strip()
                elif isinstance(value,dict) :
                    cleaned_kwargs[key] = {k :(v.strip()) if isinstance(v,str) else v for k,v in value.items()}
                else :
                    cleaned_kwargs[key] = value
            return func(*cleaned_args,**cleaned_kwargs)
        except Exception as e :
            raise e
    return wrapper