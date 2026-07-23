import akshare as ak

print("=== A股板块数据 ===")
df = ak.stock_sector_spot()
print("列名:", df.columns.tolist())
print("\n第一行数据:")
print(df.iloc[0].to_dict())

print("\n\n=== 港股指数数据 ===")
df_hk = ak.get_qhkc_index()
print("列名:", df_hk.columns.tolist())
print("\n第一行数据:")
print(df_hk.iloc[0].to_dict())

print("\n\n=== 美股指数数据 ===")
df_us = ak.index_us_stock_sina()
print("列名:", df_us.columns.tolist())
print("\n第一行数据:")
print(df_us.iloc[0].to_dict())
