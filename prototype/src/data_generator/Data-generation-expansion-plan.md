# Supply Chain Data Gen Initial Prompt 

Now we have the supply chain data models defined (we can still modify if needed later). 

Now we need to define the process to generate data. 

### Data input and output 

Now I need to use the data  generated in sales data generated and saved in: 

- C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\camping\sales

- C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\kitchen\sales

- C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\ski\sales

  

We will not use any finance data for next steps.

If we need to use reference data, we can use customer and product domain data in

C:\Repos\Explore\udf_solutions\prototype\src\data_generator\input

#### What do we need to generate 

we need to generate data for 

- model_inventory.ipynb
- model_suppliers.ipynb

For suppliers, I can give some some sample names 

1. Contoso Camping Equipment, active
2. Contoso Kitchen, active
3. Contoso Ski Equipment, active
4. Worldwide Importers, backup for Camping, Kitchen, and Ski
5. Fabrikam, back up for Ski only



Question for you, can you create an design doc named supplychain_data_gen_design.md? You can include or modify above info I put in. 