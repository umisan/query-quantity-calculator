#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from query_quantity_calculator.parser import DatalogParser
from query_quantity_calculator.hypergraph import Hypergraph

def test_hypergraph_structure():
    print("Testing hypergraph structure with R(A, B), S(B, C), T(C, A)")
    
    # Parse the example query
    parser = DatalogParser()
    query = """R(A, B)
S(B, C)
T(C, A)"""
    
    relations = parser.parse_query(query)
    print(f"Parsed relations: {relations}")
    
    # Create hypergraph
    hypergraph = Hypergraph()
    hypergraph.from_relations(relations)
    
    print(f"Vertices: {sorted(hypergraph.vertices)}")
    print(f"Hyperedges: {[(name, sorted(vertices)) for name, vertices in hypergraph.edges]}")
    
    # Verify the structure
    expected_vertices = {'A', 'B', 'C'}
    expected_edges = [
        ('R', {'A', 'B'}),
        ('S', {'B', 'C'}),
        ('T', {'C', 'A'})
    ]
    
    assert hypergraph.vertices == expected_vertices, f"Expected vertices {expected_vertices}, got {hypergraph.vertices}"
    assert len(hypergraph.edges) == 3, f"Expected 3 edges, got {len(hypergraph.edges)}"
    
    for (expected_name, expected_verts), (actual_name, actual_verts) in zip(expected_edges, hypergraph.edges):
        assert expected_name == actual_name, f"Expected edge name {expected_name}, got {actual_name}"
        assert expected_verts == actual_verts, f"Expected edge vertices {expected_verts}, got {actual_verts}"
    
    print("✓ Hypergraph structure is correct!")
    print(f"Vertex count: {hypergraph.get_vertex_count()}")
    print(f"Edge count: {hypergraph.get_edge_count()}")
    print(f"Rank: {hypergraph.get_rank()}")

if __name__ == "__main__":
    test_hypergraph_structure()