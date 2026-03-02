# AI-Assisted Sample Data Generation

**Author:** Gaiye Zhou  
**Date:** February 2026

## Background

When building the Unified Data Foundation with Fabric Solution Accelerator, the project scope was extensive: Fabric, Databricks, and Purview platforms needed to be established with comprehensive business processes. The original assumption was that sample data would be available from existing sources. However, after exploring available data sources, none were suitable for our project.

As a data-centric project, all team members needed data flowing through the system to build and test architectural components. The situation was urgent. I quickly created domain models and developed a sample generation process to produce e-commerce sales and financial data for multiple channels. This required foundational domain data including customers, relationships, tiers, and product catalogs to generate 5.5 years of historical data from January 1, 2020, to June 30, 2025.

Working with GitHub Copilot over several evenings, I successfully created a comprehensive dataset. The results exceeded expectations, and the datasets were successfully deployed. However, time constraints prevented me from making the data generation process reusable and expandable. 

This project provided the opportunity to address those limitations while documenting the process with user guides and customizable datasets. GitHub Copilot's recent advances enable it to generate complete working systems through iterative prompting. 

## Collaboration Approach with AI

The development process involved extensive iterative prompting with GitHub Copilot. Rather than immediately requesting code generation, I established a deliberate approach:

1. **Intent Communication**: Clearly articulated desired outcomes and requirements before any code generation
2. **Design-First Mindset**: Emphasized planning and architecture discussions to ensure quality code from the first attempt, avoiding time-intensive refactoring cycles
3. **Domain Context Sharing**: Provided comprehensive information about existing customer domain data from previous UDF projects, primarily structured as CSV files
4. **Iterative Refinement**: Engaged in continuous back-and-forth dialogue to refine requirements and validate approach

## Deliverables

The collaboration produced comprehensive results:

1. **Fully Functional Codebase**: Complete working solution with configurable options and robust error handling
2. **Documentation Suite**: 
   - Comprehensive user guide for the sample generation process
   - Dynamic data guide documenting the actual datasets produced
3. **Sample Datasets**: E-commerce sales and financial data for three distinct channels:
   - Camping gear merchandise
   - Kitchen supplies
   - Skiing equipment
4. **Reusable Architecture**: Well-structured and documented source code designed for maintainability
5. **Extensible Framework**: Foundation for continued development and customization

## Key Benefits

- **Dramatic Time Savings and Rapid Results**: While I have the experience and technical capability to build data generation systems manually—having done so in previous projects—the time investment would typically span weeks of dedicated development. With GitHub Copilot, this comprehensive solution was completed as a side project. What would traditionally require extensive manual coding, debugging, testing, and documentation was accomplished in a fraction of the time. 

- **Code Reusability**: Modular architecture enables easy adaptation for different use cases

- **Dataset Customization**: Flexible parameters allow tailoring to specific business requirements  

- **Significant Productivity Gains**: Estimated 100-200% improvement in development speed compared to manual coding

- **Enhanced Development Experience**: Interactive AI collaboration proved both efficient and engaging

- **Quality Assurance**: Real-time code testing and debugging capabilities through AI assistance 

   

