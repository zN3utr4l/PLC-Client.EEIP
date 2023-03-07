from pycomm3 import LogixDriver, SLCDriver

class _TypeFunctionMap: 
    types = {
        'SINT': int,
        'INT': int,
        'DINT': int,
        'REAL': float,
        'BOOL': bool,
    }

    def __getitem__(self, item):
        return str if 'STRING' in item else self.types[item]


TypeFunctionMap = _TypeFunctionMap()
