#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from query_quantity_calculator.parser import DatalogParser
from query_quantity_calculator.hypergraph import Hypergraph

def test_visualization():
    print("Testing hypergraph visualization...")
    
    # Parse the example query
    parser = DatalogParser()
    query = """R(A, B)
S(B, C)
T(C, A)"""
    
    relations = parser.parse_query(query)
    
    # Create hypergraph
    hypergraph = Hypergraph()
    hypergraph.from_relations(relations)
    
    # Test visualization creation
    try:
        fig = hypergraph.create_visualization()
        if fig is not None:
            print("✓ Visualization created successfully!")
            print(f"Number of traces: {len(fig.data)}")
            print("Trace names:", [trace.name for trace in fig.data if hasattr(trace, 'name')])
        else:
            print("✗ Visualization returned None")
    except Exception as e:
        print(f"✗ Error creating visualization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_visualization()