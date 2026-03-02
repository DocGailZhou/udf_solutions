I am going to talk with you on ideas and design first. No code generation until we are ready. I put what I am thinking in a long prompt. 

# What has been done: 

Now we got sales and finance data generation refactored and consolidated as a self-contained data generator. It can generate sales data for three product lines (camping, kitchen, and ski). The generated data in C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output.

The main_generate_sales.py is the main program to complete above tasks. 

# What to do next - First the Ideas and Goals 

### Data input and output 

Now I need to use the data  generated in sales data generated and saved in C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output. We will not use finance data for next step. For example, we use C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\camping\sales, not C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\camping\finance. 

Based on the sales data, we should be able to create demand forecast data. From demand forecast data we should be able to generate optional inventory data (what it should be), we can also have an inventory history table to track on daily basis. 

We need to create a supplier table, with 5 suppliers with 3 active, 2 as backpu.

**Data Modeling** 