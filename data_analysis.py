import os
import pandas as pd

# =====================================================================
# 1. SETUP: GENERATE COMPATIBLE SAMPLE DATA AUTOMATICALLY
# =====================================================================
def generate_sample_csv():
    """Generates a sample sales dataset CSV with intentional missing values for cleaning."""
    csv_filename = "store_sales_data.csv"
    
    # We create raw data with a duplicate row and a couple of missing values intentionally
    raw_data = {
        "Transaction_ID": [101, 102, 103, 104, 105, 106, 107, 108, 108, 109, 110],
        "Product_Category": ["Electronics", "Clothing", "Home", "Electronics", "Clothing", "Home", "Electronics", "Home", "Home", "Clothing", "Electronics"],
        "Units_Sold": [2, 1, 5, None, 3, 2, 1, 4, 4, None, 3],
        "Unit_Price": [150.0, 45.0, 20.0, 300.0, 50.0, 15.0, 1200.0, 35.0, 35.0, 60.0, 80.0],
        "Region": ["North", "East", "West", "South", "North", "East", "West", "South", "South", "North", "East"]
    }
    
    df = pd.DataFrame(raw_data)
    df.to_csv(csv_filename, index=False)
    print(f"[Setup] Local sample file '{csv_filename}' created successfully for analysis.\n")
    return csv_filename


# =====================================================================
# MAIN AUTOMATION RUNNER
# =====================================================================
def main():
    print("=========================================")
    print("        DATA ANALYSIS DASHBOARD          ")
    print("=========================================")
    
    # Generate the dataset automatically
    target_csv = generate_sample_csv()
    
    try:
        # STEP 1: LOAD CSV USING PANDAS
        print("--- Step 1: Loading Dataset ---")
        df = pd.read_csv(target_csv)
        print("Original Dataset Preview:")
        print(df)
        print("-" * 50)
        
        # STEP 2: PERFORM CLEANING OPERATIONS
        print("\n--- Step 2: Data Cleaning ---")
        
        # Check for duplicate rows and drop them safely
        duplicates_count = df.duplicated().sum()
        if duplicates_count > 0:
            df = df.drop_duplicates()
            print(f"-> Removed {duplicates_count} duplicate transaction row(s).")
            
        # Check for missing values and fill them with reasonable fallbacks (median value)
        print("Checking for missing values:")
        print(df.isnull().sum())
        
        # Fill missing values in Units_Sold with the median number of units sold
        median_units = df["Units_Sold"].median()
        df["Units_Sold"] = df["Units_Sold"].fillna(median_units)
        print(f"-> Filled missing 'Units_Sold' values using calculated median: {median_units}")
        print("-" * 50)
        
        # STEP 3: PERFORM FILTERING & TRANSFORMATION
        print("\n--- Step 3: Feature Transformation & Filtering ---")
        
        # Create a calculated metrics column: Total_Revenue = Units_Sold * Unit_Price
        df["Total_Revenue"] = df["Units_Sold"] * df["Unit_Price"]
        print("Added 'Total_Revenue' calculated metric column successfully.")
        
        # Isolate high-value transactions (where revenue > $100) using Pandas filtration
        high_value_sales = df[df["Total_Revenue"] > 100]
        print("\nFiltered High-Value Transactions (Revenue > $100):")
        print(high_value_sales[["Transaction_ID", "Product_Category", "Total_Revenue"]])
        print("-" * 50)
        
        # STEP 4: GROUPING & AGGREGATION
        print("\n--- Step 4: Grouping & Aggregations ---")
        
        # Group calculations by Product_Category to identify summary metrics
        category_summary = df.groupby("Product_Category").agg(
            Total_Units_Sold=('Units_Sold', 'sum'),
            Gross_Revenue=('Total_Revenue', 'sum'),
            Average_Unit_Cost=('Unit_Price', 'mean')
        ).reset_index()
        
        print("Summary Metrics Grouped By Product Category:")
        print(category_summary.to_string(index=False))
        print("-" * 50)
        
        # STEP 5: GENERATE MEANINGFUL INSIGHTS SUMMARY
        print("\n--- Step 5: Final Generated Data Insights ---")
        total_store_revenue = df["Total_Revenue"].sum()
        top_category_row = category_summary.loc[category_summary["Gross_Revenue"].idxmax()]
        
        print(f"1. Overall Gross Store Revenue generated: ${total_store_revenue:,.2f}")
        print(f"2. Highest earning category: '{top_category_row['Product_Category']}' pulling in ${top_category_row['Gross_Revenue']:,.2f}")
        print(f"3. Most volume units distributed: {category_summary.loc[category_summary['Total_Units_Sold'].idxmax()]['Product_Category']}")
        print("=========================================")
        
        # Save clean dataset summary analysis to file path cleanly
        output_filename = "cleaned_sales_summary.csv"
        category_summary.to_csv(output_filename, index=False)
        print(f"\n[Success] Summary dataset generated and stored cleanly inside '{output_filename}'.")

    except FileNotFoundError:
        print("[Error] Target dataset CSV file was not found. Please verify placement paths.")
    except Exception as e:
        print(f"[Runtime Exception] Something went wrong while running analytical tasks: {e}")


if __name__ == "__main__":
    main()