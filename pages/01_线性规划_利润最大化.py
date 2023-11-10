import streamlit as st
from pyomo.environ import *


st.set_page_config(
    page_title="线性规划：利润最大化",
    layout="wide"
)

st.write("""
         假设你正在考虑创办一家生产X产品的企业。你已经确定X的市场每周最多40台，每台270美元。
         每台机组的生产需要100美元的原材料、1小时的A类劳动力和2小时的B类劳动力。您可以无限量地使用原材料，
         但每周只有80小时的劳动力A，成本为50美元/小时，每周只有100小时的劳动力B，成本为40美元/小时。
         忽略所有其他费用，每周最大利润是多少？
         """)

raw_cost = st.number_input('原材料成本', 100)
a_cost = st.number_input('劳动力A 成本', 40)

model = ConcreteModel()

# declare decision variables
model.x = Var(domain=NonNegativeReals)

# declare objective
model.profit = Objective(
    expr = 40*model.x,
    sense = maximize)

# declare constraints
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x <= 80)
model.laborB = Constraint(expr = 2*model.x <= 100)

# solve
SolverFactory('cbc').solve(model).write()