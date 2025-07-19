# Query Quantity Calculator

## 📌 Overview

Query Quantity Calculator is a web application that computes the following characteristics for conjunctive queries given in Datalog-style list format:

- **Fractional Edge Cover** (`ρ*`)
- **Fractional Edge Packing** (`τ*`)
- **AGM Bound** (assuming each relation size is 1)

It aims to quickly evaluate the theoretical properties of query structures in research and educational settings.

## ✨ Features

- Parse Datalog-style queries and build hypergraph structures
- Solve linear programming problems to compute fractional edge cover and packing
- Calculate AGM Bound
- Interactive hypergraph visualization
- Detailed analysis and display of results

## 📋 Requirements

- Python 3.8+
- Streamlit
- NumPy
- SciPy
- Plotly
- NetworkX
- Pandas

## 🚀 Installation

### 🐳 Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/umisan/query-quantity-calculator.git
   cd query-quantity-calculator
   ```

2. **Build Docker image**
   ```bash
   docker build -t query-quantity-calculator .
   ```

3. **Run container**
   ```bash
   docker run -p 8501:8501 query-quantity-calculator
   ```

### 🐍 Local Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/umisan/query-quantity-calculator.git
   cd query-quantity-calculator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Starting the Web Application

**Using Docker:**
```bash
docker run -p 8501:8501 query-quantity-calculator
```

**Local environment:**
```bash
streamlit run run_app.py
```

Either method will automatically open `http://localhost:8501` in your browser.

### Query Input Example

In the application, enter Datalog-style queries in the following format:

```
R(a, b)
S(b, c)
T(a, c)
```

### Output Results

The calculation results display the following information:

- **Number of Vertices (|V|)**: Number of vertices in the hypergraph
- **Number of Edges (|E|)**: Number of edges in the hypergraph
- **Hypergraph Rank**: Maximum edge size
- **Fractional Edge Cover (ρ*)**: Minimum edge cover
- **Fractional Edge Packing (τ*)**: Maximum edge packing
- **AGM Bound**: Theoretical limit with all relation sizes = 1
- **ρ* × τ***: Product value (verification that it's ≤ |V|)

### Visualization

The hypergraph structure is displayed as an interactive graph, allowing visual understanding of the query structure.

## 📁 Project Structure

```
query-quantity-calculator/
├── src/
│   └── query_quantity_calculator/
│       ├── __init__.py
│       ├── app.py                # Streamlit application
│       ├── hypergraph.py          # Hypergraph structure and operations
│       ├── parser.py              # Datalog query parser
│       └── solver.py              # Linear programming solver
├── tests/
│   └── __init__.py
├── run_app.py                     # Application startup script
├── requirements.txt               # Dependencies
├── CLAUDE.md                      # Detailed project specifications
├── README.md                      # This file
└── LICENSE
```

## 🧮 Theoretical Background

This tool is based on the following theories:

- **Fractional Edge Cover**: Minimum edge weight needed to cover each vertex in a hypergraph
- **Fractional Edge Packing**: Maximum weight of non-overlapping edges
- **AGM Bound**: Theoretical limit for optimal execution time of join queries

## 📚 References

- Atserias, A., Grohe, M., & Marx, D. (2008). "Size bounds and query plans for relational joins"
- Research on join queries and hypergraph theory

## 📄 License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions to the project are welcome. Please feel free to submit bug reports, feature requests, pull requests, etc.
