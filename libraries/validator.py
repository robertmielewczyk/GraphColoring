class Validator():
    def __init__(self):
        pass

    def range(self, ground, limit, default=0, message="", error_message="Wrong Value"):
        '''
        Checks if value is in between given range
        '''
        try:
            value = int(input(message))
            while(value <ground or value>limit):
                print("{} | Values has to be between [{}, {}]".format(error_message, ground, limit))
                value = int(input(message))
            return value
        except ValueError:
            print("DEFAULTS!!! {} | Values has to be between [{}, {}]".format(error_message, ground, limit))
            return default

    def exact_string(self, values ,message="", error_message="Wrong Value"):
        '''
        Checks if value is in specified array of strings
        '''
        value = input(message)
        while(value not in values):
            print("{} | Values has to be {}".format(error_message, values))
            value = input(message)
        return value