# Superchip Optimization

#Overview
This project optimizes Superchip's production and distribution operations across five manufacturing facilities in Virginia, each producing up to 30 types of computer chips. The optimization model aims to minimize costs associated with both production and shipping, providing strategic recommendations for the next fiscal year. It uses Python and the Gurobi optimizer to evaluate cost-effective production and distribution strategies.

#Problem Statement
Superchip faces high costs in both production and distribution due to differing production capacities and equipment across facilities, and variable shipping distances. This optimization model addresses key business questions:
- Recommended production policies for cost savings.
- Facility prioritization for capacity expansion.
- Feasibility of a 10% increase in demand.
- Facility selection for implementing new cost-saving manufacturing technologies.

## Data Sources
- **Production Capacity**: Details each facility's production limits and chip types.
- **Regional Demand**: Shows chip demand across 23 U.S. regions.
- **Shipping Costs**: Varies by chip type, facility, and sales region due to distance and logistical factors.
- **Production Costs**: Facility-dependent, based on equipment and operational overhead.
  
## Methodology
The optimization model:
1. **Data Import**: Data from "SuperChipData.xlsx" is imported into Python using pandas for analysis.
2. **Objective Function**:
   - **Production Costs**: Calculates the cost based on chip type, facility, and production quantity.
   - **Shipping Costs**: Calculates costs based on shipping quantities for each chip, facility, and region.
3. **Constraints**: Ensures all demand is met, production remains within facility capacity, and non-negative decision variables.
4. **Optimization**: Minimizes total cost by balancing production and shipping while meeting demand.
   
## Key Findings
1. **Cost Reduction**: Optimized operations could reduce costs by approximately 8.47%, from $54,024.42 to $49,083.43.
2. **Capacity Expansion**: Richmond is recommended for capacity investment due to potential cost savings based on shadow pricing.
3. **Handling Increased Demand**: Existing facilities can manage a projected 10% demand increase without additional infrastructure.
4. **New Technology**: Alexandria is the best candidate for a new manufacturing technology expected to reduce costs by 15%.
   
## Recommendations
1. **Implement Cost-Efficient Production Allocation**: Allocate chip production to facilities with cost advantages rather than proportional capacity.
2. **Expand Capacity at Richmond**: Richmond's low costs make it ideal for capacity expansion to maximize cost savings.
3. **Introduce New Technology at Alexandria**: To capitalize on potential savings, implement new production technology at Alexandria, where production costs are highest.

## Instructions to Run the Model
1. **Requirements**: Python, Gurobi optimizer, and pandas library.
2. **Setup**: Ensure "SuperChipData.xlsx" and the Python script are in the same directory.
3. **Execution**: Run the Python script sequentially, starting with data loading, optimization, and then analysis of results.
4. **Output**: The script outputs optimized production and shipping allocations and total costs for strategic planning.
   
## Files Included
- **SuperChipData.xlsx**: Contains production capacity, demand, shipping, and production cost data.
- **Python Script**: Performs optimization using Gurobi and pandas.
