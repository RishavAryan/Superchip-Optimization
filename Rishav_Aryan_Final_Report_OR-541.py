#!/usr/bin/env python
# coding: utf-8

# In[47]:


import gurobipy as gp
from gurobipy import GRB
import pandas as pd

def Rdata(path):
    
    prod_cap = pd.read_excel(path, sheet_name="Production Capacity")
    demand_data = pd.read_excel(path, sheet_name="Sales Region Demand")
    shipp_cost = pd.read_excel(path, sheet_name="Shipping Costs")
    product_cost = pd.read_excel(path, sheet_name="Production Costs")
    return prod_cap,demand_data ,shipp_cost, product_cost

def init_model():
    return gp.Model("SuperChipProduction")

def var(model, chips, facilities, regions):
    x = { (i, j): model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}") for i in chips for j in facilities }
    y = { (i, j, k): model.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}{j}{k}") for i in chips for j in facilities for k in regions }
    model.update()
    return x, y

def const(model, x, y, chips, facilities, regions, demands, capacities):
    for i in chips:
        for k in regions:
            model.addConstr(gp.quicksum(y[i, j, k] for j in facilities) >= demands[(k, i)])

    for i in chips:
        for j in facilities:
            model.addConstr(gp.quicksum(y[i, j, k] for k in regions) - x[i, j] <= 0)

    for j in facilities:
        model.addConstr(gp.quicksum(x[i, j] for i in chips) <= capacities[j], name=f"Capacity_{j}")

def obj(model, x, y, chips, facilities, regions, prod_costs, ship_costs):
    
    tot_prod = gp.quicksum(prod_costs[j, i] * x[i, j] for i in chips for j in facilities)
    tot_shipp = gp.quicksum(ship_costs[j, i, k] * y[i, j, k] for i in chips for j in facilities for k in regions)
    model.setObjective(tot_prod + tot_shipp, GRB.MINIMIZE)

def sol(model):
    model.optimize()
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found!")
    else:
        print("No solution found.")

def superchip_optimize(path):
    prod_cap, demand_data, shipp_cost, product_cost = load_data(path)

    model = init_model()
    chips = demand_df['Computer Chip'].unique()
    facilities = production_capacity_df['Facility'].unique()
    regions = demand_df['Sales Region'].unique()

    capacities = dict(zip(production_capacity_df['Facility'], production_capacity_df['Computer Chip Production Capacity (thousands per year)']))
    demands = demand_df.set_index(['Sales Region', 'Computer Chip'])['Yearly Demand (thousands)'].to_dict()
    prod_costs = production_costs_df.set_index(['Facility', 'Computer Chip'])['Productin Cost ($ per chip)'].to_dict()
    ship_costs = shipping_costs_df.set_index(['Facility', 'Computer Chip', 'Sales Region'])['Shipping Cost ($ per chip)'].to_dict()

    x, y = create_variables(model, chips, facilities, regions)
    set_constraints(model, x, y, chips, facilities, regions, demands, capacities)
    set_objective(model, x, y, chips, facilities, regions, prod_costs, ship_costs)
    solve_model(model)


superchip_optimize("/Users/rishavaryan/Downloads/SuperChipData.xlsx")


# In[46]:


#problem2

def get_capacity_constraint(model, facility):
    capacity_name = f'Capacity_{facility}'
    return model.getConstrByName(capacity_name)

def cal_shadow_prices(model, facilities):

    shadow_prices = {}
    for facility in facilities:
        capacity_constraint = get_capacity_constraint(model, facility)
        if capacity_constraint:
            shadow_prices[facility] = capacity_constraint.Pi
        else:
            shadow_prices[facility] = None
    return shadow_prices

def find_facility(shadow_prices):
    highest_shadow_price = -float('inf')
    facility_for_expansion = None
    for facility, shadow_price in shadow_prices.items():
        if shadow_price and shadow_price > highest_shadow_price:
            highest_shadow = shadow_price
            facility_for_expansion = facility
    return facility_for_expansion, highest_shadow

def evaluate_cost(highest_shadow_price, increase=1000):
    return highest_shadow_price * increase

def evaluate(model, facilities):
    if model.status == gp.GRB.OPTIMAL:
        print("\nSummary per Facility")
        shadow_prices = cal_shadow_prices(model, facilities)
        for facility, shadow_price in shadow_prices.items():
            if shadow_price is not None:
                print(f"\nFacility: {facility}")
                print(f"Shadow Price for Production Capacity at {facility}: {shadow_price}")
            else:
                print(f"\nFacility: {facility}")
                print("No capacity constraint found for this facility.")

        facility_for_expansion, highest_shadow = find_facility(shadow_prices)
        print(f"\nFacility selected for potential capacity expansion: {facility_for_expansion}")
        print(f"Highest Shadow Price: {highest_shadow_price}")

        potential_cost = evaluate_cost(highest_shadow)
        print(f"Potential cost savings from expanding production capacity: ${potential_cost:.2f}")
    else:
        print("No solution found.")


evaluate(model, facilities)


# In[49]:


#problem3

def cal_new_demand(demands, increase=10):
    return {(k, i): value * (1 + increase / 100) for (k, i), value in demands.items()}

def check(new_demand, capacities, chips, facilities, regions):
    return all(sum(new_demand[k, i] for k in regions) <= capacities[j] for i in chips for j in facilities)

def init_new_model(chips, facilities, regions):
    new_model = gp.Model("SuperChipProduction_NewDemand")
    new_x = { (i, j): new_model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}") for i in chips for j in facilities }
    new_y = { (i, j, k): new_model.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}{j}{k}") for i in chips for j in facilities for k in regions }
    new_model.update()
    return new_model, new_x, new_y

def new_objective(new_model, new_x, new_y, chips, facilities, regions, prod_costs, ship_costs):
    total_production_costs = gp.quicksum(prod_costs[j, i] * new_x[i, j] for i in chips for j in facilities)
    total_shipping_costs = gp.quicksum(ship_costs[j, i, k] * new_y[i, j, k] for i in chips for j in facilities for k in regions)
    new_model.setObjective(total_production_costs + total_shipping_costs, GRB.MINIMIZE)

def add_constraints(new_model, new_x, new_y, new_demand, chips, facilities, regions, capacities):
    for i in chips:
        for k in regions:
            new_model.addConstr(gp.quicksum(new_y[i, j, k] for j in facilities) >= new_demand[k, i])

    for i in chips:
        for j in facilities:
            new_model.addConstr(gp.quicksum(new_y[i, j, k] for k in regions) - new_x[i, j] <= 0)

    for j in facilities:
        new_model.addConstr(gp.quicksum(new_x[i, j] for i in chips) <= capacities[j])

def run_scenario(demands, chips, facilities, regions, capacities, prod_costs, ship_costs):
    new_demand = calculate_new_demand(demands)
    if check_capacity(new_demand, capacities, chips, facilities, regions):
        print("\nSuper Chip has sufficient capacity to handle the estimated increase in demand.")
        new_model, new_x, new_y = init_new_model(chips, facilities, regions)
        set_new_objective(new_model, new_x, new_y, chips, facilities, regions, prod_costs, ship_costs)
        add_new_constraints(new_model, new_x, new_y, new_demand, chips, facilities, regions, capacities)
        new_model.optimize()
        
        if new_model.status == GRB.OPTIMAL:
            print(f"\nTotal cost for the new demand: {new_model.objVal:.2f}")
        else:
            print("No solution found.")
    else:
        print("\nSuper Chip does not have sufficient capacity to handle the estimated increase in demand.")


run_scenario(demands, chips, facilities, regions, capacities, prod_costs, ship_costs)


# In[51]:


#problem4
def production_costs_without_tech(prod_costs, x, chips, facilities):
    return {j: sum(prod_costs[j, i] * x[i, j].X for i in chips) for j in facilities}

def production_costs_with_tech(costs_without_tech, reduction_percentage=15):
    reduction_factor = 1 - reduction_percentage / 100
    return {j: reduction_factor * cost for j, cost in costs_without_tech.items()}

def max_cost_reduction(costs_without_tech, costs_with_tech):
    return max(costs_without_tech, key=lambda j: costs_without_tech[j] - costs_with_tech[j])

def eval_tech(prod_costs, x, chips, facilities):
    costs_without_tech = production_costs_without_tech(prod_costs, x, chips, facilities)
    costs_with_tech = production_costs_with_tech(costs_without_tech)
    
    max_reduction = max_cost_reduction(costs_without_tech, costs_with_tech)
    
    print(f"\nThe facility that should receive the new technology is: {max_reduction}")


eval_tech(prod_costs, x, chips, facilities)


# In[ ]:




