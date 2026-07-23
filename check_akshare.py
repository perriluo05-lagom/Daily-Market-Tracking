import akshare as ak

print("=== 港股相关函数 ===")
hk_funcs = [x for x in dir(ak) if 'hk' in x.lower()]
print(hk_funcs[:20])

print("\n=== 美股相关函数 ===")
us_funcs = [x for x in dir(ak) if 'us' in x.lower()]
print(us_funcs[:20])

print("\n=== 指数相关函数 ===")
index_funcs = [x for x in dir(ak) if 'index' in x.lower()]
print(index_funcs[:30])
