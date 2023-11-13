import pyomo.environ as pyo
import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="线性规划：混合原料",
    layout="wide"
)
solver = st.selectbox(
    label='求解器',
    options=('ipopt','cbc','glpk'))

tab1, tab2 = st.tabs(["最小成本勾兑问题","酒精灯燃料混合问题"])

with tab1:
    st.write("""
一家啤酒厂收到了100加仑4% ABV(酒精含量)啤酒的订单。
             这家啤酒厂现有的啤酒A酒精含量为4.5%，每加仑成本为0.32美元，
             啤酒B酒精含量为3.7%，每加仑成本为0.25美元。
             水也可以作为混合剂，每加仑成本为0.05美元。找到满足客户需求的最低成本组合。
""")
    
    order_vol = st.number_input("订单（加仑）", value=100, min_value=0)
    order_abv = st.number_input("订单（酒精含量）", value=0.04, min_value=0.0, max_value=0.1, format='%f')
    df = pd.DataFrame([
        {'原料':'A', '酒精含量': 0.045, '成本': 0.32},
        {'原料':'B', '酒精含量': 0.037, '成本': 0.25},
        {'原料':'水','酒精含量': 0.000, '成本': 0.05},
    ])
    st.write("原料数据")
    edited_df = st.data_editor(df, num_rows="dynamic")
    materials ={}
    for r in edited_df.to_dict(orient='records'):
        if r['原料'] is not None and not math.isnan(r['酒精含量']) and not math.isnan(r['成本']):
            materials[r['原料']] = r
        
    
    model = pyo.ConcreteModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

    # 原料名称作为 x
    C = materials.keys()
    model.x = pyo.Var(C, domain=pyo.NonNegativeReals)
    model.cost = pyo.Objective(expr = sum(model.x[c]*materials[c]['成本'] for c in C))
    model.vol = pyo.Constraint(expr = order_vol == sum(model.x[c] for c in C))
    model.abv = pyo.Constraint(expr = 0 == sum(model.x[c]*(materials[c]['酒精含量'] - order_abv) for c in C))
    solver = pyo.SolverFactory(solver)
    solver.solve(model)

    st.write('最小成本混合方案')
    for c in materials.keys():
        st.write('  ', c, ':', round(model.x[c](), 2), '加仑')
    
    st.write('容积 = ', round(model.vol(), 2), ' 加仑')
    st.write('成本 = $', round(model.cost(), 2))
    

with tab2:
    st.write("酒精炉通常以工业酒精为燃料，通常是乙醇和其他酒精和化合物的混合物，不适合人类饮用。")
    st.write("酒精炉的问题是在冰点以下的天气很难点燃。使用以下原料混合，设计一种适合寒冷天气的燃料。")