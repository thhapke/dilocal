
def toggle() :
    toggle.on = True if toggle.on==False else False
    return toggle.on

toggle.on = False

print(toggle())
print(toggle())
print(toggle())

class forced_exception :
    def __init__(self,max_index, num_crashes) :
        self.max_index = max_index
        self.num_crashes = num_crashes
        self.crash_indices = { i for i in range(0,self.max_index,int(self.max_index/self.num_crashes)) if i >0}
        if len(self.crash_indices) < self.num_crashes :
            self.crash_indices.add(1)
        print(self.crash_indices)

    def raise_exception(self,index) :
        if self.num_crashes == 0 or not index in self.crash_indices :
            return None
        self.crash_indices.remove(index)
        error_code = 1
        error_code = "Forced Crash"
        error_details = "Details"
        #error_details = api.Table([['index', index]])
        #raise api.OperatorException(code,error_text,error_details)
        print(f"{index}: {error_code} - {error_code} - {error_details}")

fe = forced_exception(10,2)

for i in range(0,10) :
    fe.raise_exception(i)