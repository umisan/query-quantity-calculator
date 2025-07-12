import numpy as np
from scipy.optimize import linprog
from typing import List, Tuple
from .hypergraph import Hypergraph


class QuerySolver:
    def __init__(self, hypergraph: Hypergraph):
        self.hypergraph = hypergraph
    
    def solve_fractional_edge_cover(self) -> float:
        n_vertices = self.hypergraph.get_vertex_count()
        n_edges = self.hypergraph.get_edge_count()
        
        if n_vertices == 0 or n_edges == 0:
            return 0.0
        
        vertices = self.hypergraph.get_vertices_list()
        vertex_to_index = {v: i for i, v in enumerate(vertices)}
        
        A_ub = []
        b_ub = []
        
        for vertex in vertices:
            constraint = [0.0] * n_edges
            edges_containing_vertex = self.hypergraph.get_edges_containing_vertex(vertex)
            
            for edge_idx in edges_containing_vertex:
                constraint[edge_idx] = 1.0
            
            A_ub.append([-x for x in constraint])
            b_ub.append(-1.0)
        
        c = [1.0] * n_edges
        bounds = [(0, None) for _ in range(n_edges)]
        
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if result.success:
            return result.fun
        else:
            raise RuntimeError("Failed to solve fractional edge cover")
    
    def solve_fractional_edge_packing(self) -> float:
        n_vertices = self.hypergraph.get_vertex_count()
        n_edges = self.hypergraph.get_edge_count()
        
        if n_vertices == 0 or n_edges == 0:
            return 0.0
        
        vertices = self.hypergraph.get_vertices_list()
        
        A_ub = []
        b_ub = []
        
        for vertex in vertices:
            constraint = [0.0] * n_edges
            edges_containing_vertex = self.hypergraph.get_edges_containing_vertex(vertex)
            
            for edge_idx in edges_containing_vertex:
                constraint[edge_idx] = 1.0
            
            A_ub.append(constraint)
            b_ub.append(1.0)
        
        c = [-1.0] * n_edges
        bounds = [(0, None) for _ in range(n_edges)]
        
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if result.success:
            return -result.fun
        else:
            raise RuntimeError("Failed to solve fractional edge packing")
    
    def compute_agm_bound(self) -> float:
        n_edges = self.hypergraph.get_edge_count()
        
        if n_edges == 0:
            return 1.0
        
        product = 1.0
        for i in range(n_edges):
            edge_size = self.hypergraph.get_edge_size(i)
            product *= (1.0 ** (1.0 / edge_size))
        
        return product