# author Dobri ( hardc0d3 )
# license: whatever you  want like to do even do with not existing copyright and copyleft notice
# main idea is to make a ultra clean operational interfaces with
# interchangeable implementations
# then use those interfaces to pure abstract implement something

# decorator
def subject_operation(sbj_op):
    def __wrap(func):
        def __f(*a, **kw):
            func(*a, **kw)
            return sbj_op(*a, **kw)
        return __f
    return __wrap


# default dumb stuff
class DefaultSubject(object):
    default_operation_name = 'default_operation_'

    def __init__(self):
        pass

    def default_operation_(self, *args, **kwargs):
        pass


# context storage
class SubjectOperation(object):
    def __init__(self, subject=DefaultSubject(),
                 operation_name=DefaultSubject.default_operation_name,
                 ):
        self.subject = subject
        self.operation_name = operation_name
        self.original_operation_name = operation_name
        self.original_target = DefaultSubject.default_operation_
        self.original_subject = subject

    def attach_subject(self, subject):
        self.original_subject = self.subject
        self.subject = subject

    def detach_subject(self):
        self.subject = self.original_subject

    def attach_operation(self, operation_name):
        self.original_operation_name = self.operation_name
        self.operation_name = operation_name

    def detach_operation(self):
        self.operation_name = self.original_operation_name

    def attach_target(self, target_function_interface):
        self.original_target = target_function_interface
        target_function_interface = subject_operation(self)(target_function_interface)
        return target_function_interface

    def detach_target(self, target_function_interface):
        target_function_interface = self.original_target
        return target_function_interface

    def __call__(self, *args, **kwargs):
        return self.subject.__getattribute__(self.operation_name)(*args, **kwargs)


def Factory(cls, target_map, interface_obj, a, kw):
    ll = cls(*a, **kw)
    for name in target_map:
        interface_obj.__setattr__(
            name,
            SubjectOperation(
                subject=ll,
                operation_name=target_map[name]).attach_target(
                interface_obj.__getattribute__(name)
            ))
    return ll












