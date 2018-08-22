
def add(*args):
    ret = args[0]
    for v in args:
        ret += v
    return v

def add2(v1, v2):
    return v1+v2

def main():
    print( add(1,2,3) )
    print( add([1,2], [3,4]) )
    print( add((1,2), (3,4)) )

    print( add2(1,2) )
    print( add2([1,2], [3,4]) )
    print( add2((1,2), (3,4)) )

if __name__ == '__main__':
    if 1:
        from pyannotate_runtime import collect_types
        collect_types.init_types_collection()
        with collect_types.collect():
            main()
        collect_types.dump_stats('type_info.json') 
    else:
        main()
