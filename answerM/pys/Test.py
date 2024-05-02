from Service.qaService import qaServiceImpl
import pandas as pd
instance = qaServiceImpl()
res = instance.getPageQa(600)
print(res)