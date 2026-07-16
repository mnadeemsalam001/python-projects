# Restaurant Orders Analysis

A pandas-based exploratory analysis of restaurant order data, examining sales
performance by menu item and by time of day/week.

## Data

- `order_details.csv` — one row per ordered item: `order_details_id`,
  `order_id`, `order_date`, `order_time`, `item_id`
- `menu_items.csv` — menu catalog: `menu_item_id`, `item_name`, `category`,
  `price`

## What the notebook does

1. **Load & clean** — reads both CSVs and drops order rows with a missing
   `item_id`.
2. **Join** — merges order details with the menu catalog on `item_id` /
   `menu_item_id`.
3. **Derive fields**
   - `sales_tax` = 8% of `price`
   - `total_revenue` = `price` + `sales_tax`
   - `order_timestamp` = combined `order_date` + `order_time`
4. **Best & worst sellers** — total revenue per menu item, overall and
   filtered by category (e.g. Italian), visualized as horizontal bar charts.
5. **Time-based analysis** — daily revenue trend, plus a day-of-week ×
   hour-of-day pivot table visualized as a seaborn heatmap to spot the
   restaurant's busiest times.

## Requirements

- pandas
- matplotlib
- seaborn

## Usage

Open `Restaurant_Orders_Analysis.ipynb` in Jupyter and run all cells. The CSV
data files are expected in the same folder as the notebook.

## Skills / Techniques Demonstrated

- Reading data from CSV files
- Parsing dates
- Profiling data (`.head()`, `.tail()`, `.info()`, `.describe()`)
- Dropping null values
- Joining tables (merge)
- Filtering, sorting, and aggregating data
- Pivot tables
- Visualizing data with bar charts, line charts, and the seaborn library
- Heatmaps
