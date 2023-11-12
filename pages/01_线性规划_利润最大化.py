
import pyomo.environ as pyo
import streamlit as st

st.set_page_config(
    page_title="线性规划：利润最大化",
    layout="wide"
)

st.write("""
         假设你正在考虑创办一家生产 X 产品的企业。你已经确定X的市场每周最多40台，每台270 元。
         每台机组的生产需要100元的原材料、1小时的A类劳动力和2小时的B类劳动力。您可以无限量地使用原材料，
         但每周只有80小时的劳动力A，成本为50元/小时，每周只有100小时的劳动力B，成本为40元/小时。
         忽略所有其他费用，每周最大利润是多少？
         """)

demand_x = st.number_input('X 市场需求',value= 40, min_value=0)
price_x = st.number_input('X 销售价格', value=270, min_value=0)
raw_cost_x = st.number_input('X 原材料成本', value=100, min_value=0)
a_cost = st.number_input('劳动力A 成本', value=50, min_value=0)
a_limit = st.number_input('劳动力A 工时', value=80, min_value=0)
b_cost = st.number_input('劳动力B 成本', value=40, min_value=0)
b_limit = st.number_input('劳动力B 工时', value=100, min_value=0)

# 
model = pyo.ConcreteModel()

# declare decision variables
model.x = pyo.Var(domain=pyo.NonNegativeIntegers)

# declare objective
model.profit = pyo.Objective(
    expr = (price_x - raw_cost_x - a_cost - 2 * b_cost)  * model.x,
    sense = pyo.maximize)

# declare constraints
model.demand = pyo.Constraint(expr = model.x <= demand_x )
model.laborA = pyo.Constraint(expr = model.x <= a_limit )
model.laborB = pyo.Constraint(expr = 2*model.x <= b_limit )

# solve
pyo.SolverFactory('ipopt').solve(model)

st.write(f"每周生产 { int(model.x()) } 个产品 X ，获得最大利润 { int(model.profit())} 元")


st.write("""
    您的营销部门已制定了名为 Y 的新产品的计划。该产品的售价为 210 元/个，他们希望您能卖掉所有能生产的产品。
    它的制造成本也更低，仅需要 90 元的原材料，1 小时的 A 类劳动力每小时 50 元，1 小时的 B 类劳动力每小时 40 元。每周潜在利润是多少？
""")

price_y = st.number_input('Y 销售价格', value=210, min_value=0)
raw_cost_y = st.number_input('Y 原材料成本', value=90, min_value=0)

model = pyo.ConcreteModel()
model.y = pyo.Var(domain=pyo.NonNegativeIntegers)
model.profit = pyo.Objective(
    expr = (price_y - raw_cost_y - a_cost - b_cost) * model.y,
    sense = pyo.maximize
)
model.laborA = pyo.Constraint(expr = model.y <= a_limit )
model.laborB = pyo.Constraint(expr = model.y <= b_limit )
pyo.SolverFactory('ipopt').solve(model)

st.write(f"每周生产 { int(model.y()) } 个产品 Y ，获得最大利润 { int(model.profit())} 元")

st.write("假如同时生产 X 和 Y，则最大利润是多少？")
model = pyo.ConcreteModel()
model.x = pyo.Var(domain=pyo.NonNegativeIntegers)
model.y = pyo.Var(domain=pyo.NonNegativeIntegers)
model.profit = pyo.Objective(
    expr = (price_y - raw_cost_y - a_cost - b_cost) * model.y +  (price_x - raw_cost_x - a_cost - 2 * b_cost)  * model.x,
    sense = pyo.maximize
)
model.demand = pyo.Constraint(expr = model.x <= demand_x )
model.laborA = pyo.Constraint(expr = (model.x + model.y) <= a_limit )
model.laborB = pyo.Constraint(expr = (2*model.x + model.y) <= b_limit )
pyo.SolverFactory('ipopt').solve(model)

st.write(f"每周生产 {int(model.x())} 个 X 产品， {int(model.y())} 个 Y 产品，获得最大利润 {int(model.profit())}")

# import matplotlib.pyplot as plt
# import numpy as np

# fig, ax = plt.subplots(1, 1, figsize=(6, 6))
# ax.set_aspect('equal')
# ax.axis([0, 100, 0, 100])

# ax.set_xlabel('X Production')
# ax.set_ylabel('Y Production')

# # Labor A constraint
# x = np.array([0, a_limit])
# ax.plot(x, a_limit - x, 'r', lw=2)

# # Labor B constraint
# x = np.array([0, b_limit])
# ax.plot(x, b_limit - 2*x, 'b', lw=2)

# # Demand constraint
# ax.plot([demand_x, demand_x], [0, 100], 'g', lw=2)

# ax.legend(['Labor A Constraint', 'Labor B Constraint', 'Demand Constraint'])
# ax.fill_between([0, a_limit, 100], [a_limit, 0,0 ], [100, 100, 100], color='r', alpha=0.15)
# ax.fill_between([0, b_limit, 100], [2*b_limit, 0, 0], [100, 100, 100], color='b', alpha=0.15)
# ax.fill_between([demand_x, 100], [0, 0], [100, 100], color='g', alpha=0.15)

# # Contours of constant profit
# x = np.array([0, 100])
# for p in np.linspace(0, 3600, 10):
#     y = (p - 40*x)/30
#     ax.plot(x, y, 'y--')
    
# arrowprops = dict(shrink=.1, width=1, headwidth=5)

# # Optimum
# ax.plot(20, 60, 'r.', ms=20)
# ax.annotate('Mixed Product Strategy', xy=(20, 60), xytext=(50, 70), arrowprops=arrowprops)

# ax.plot(0, 80, 'b.', ms=20)
# ax.annotate('Y Only', xy=(0, 80), xytext=(20, 90), arrowprops=arrowprops)

# ax.plot(40, 0, 'b.', ms=20)
# ax.annotate('X Only', xy=(40, 0), xytext=(70, 20), arrowprops=arrowprops)

# ax.text(4, 23, 'Increasing Profit')
# ax.annotate('', xy=(20, 15), xytext=(0,0), arrowprops=arrowprops)
# st.pyplot(fig)
