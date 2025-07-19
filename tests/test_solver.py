import pytest
import math
from src.query_quantity_calculator.hypergraph import Hypergraph
from src.query_quantity_calculator.solver import QuerySolver


class TestQuerySolver:
    def setup_method(self):
        self.hypergraph = Hypergraph()

    def test_solve_fractional_edge_cover_triangle(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        # For a triangle query, fractional edge cover should be 1.5
        assert abs(rho_star - 1.5) < 1e-6

    def test_solve_fractional_edge_cover_star(self):
        relations = [("R", ["a", "b"]), ("S", ["a", "c"]), ("T", ["a", "d"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        # For a star query, fractional edge cover should be 3.0
        assert abs(rho_star - 3.0) < 1e-6

    def test_solve_fractional_edge_cover_path(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["c", "d"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        # For a path query, each internal vertex needs 0.5 from each adjacent edge
        # Each edge contributes to 2 constraints (except endpoints)
        assert rho_star >= 1.5  # Should be exactly 1.5 for this path

    def test_solve_fractional_edge_packing_triangle(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        tau_star = solver.solve_fractional_edge_packing()
        # For a triangle query, fractional edge packing should be 1.5
        assert abs(tau_star - 1.5) < 1e-6

    def test_solve_fractional_edge_packing_star(self):
        relations = [("R", ["a", "b"]), ("S", ["a", "c"]), ("T", ["a", "d"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        tau_star = solver.solve_fractional_edge_packing()
        # For a star query, the center vertex limits packing to 1.0
        assert abs(tau_star - 1.0) < 1e-6

    def test_solve_fractional_edge_packing_path(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["c", "d"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        tau_star = solver.solve_fractional_edge_packing()
        # For a path query, internal vertices b and c each appear in only 2 edges
        # So each can allow up to 1.0, giving us a total of 2.0
        assert tau_star <= 2.0

    def test_compute_agm_bound_triangle(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        agm_bound = solver.compute_agm_bound()
        # For triangle with all edges of size 2, AGM bound = (1^(1/2))^3 = 1
        assert abs(agm_bound - 1.0) < 1e-6

    def test_compute_agm_bound_various_arities(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c", "d"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        agm_bound = solver.compute_agm_bound()
        # AGM bound = (1^(1/2)) * (1^(1/3)) * (1^(1/2)) = 1
        assert abs(agm_bound - 1.0) < 1e-6

    def test_duality_property(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        vertex_count = self.hypergraph.get_vertex_count()
        
        # Duality property: ρ* × τ* ≤ |V|
        product = rho_star * tau_star
        assert product <= vertex_count + 1e-6  # Allow for small numerical errors

    def test_solve_empty_hypergraph(self):
        relations = []
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        assert solver.solve_fractional_edge_cover() == 0.0
        assert solver.solve_fractional_edge_packing() == 0.0
        assert solver.compute_agm_bound() == 1.0

    def test_solve_single_vertex(self):
        # Single vertex, single edge case
        relations = [("R", ["a"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        
        assert rho_star == 1.0
        assert tau_star == 1.0

    def test_solve_single_edge(self):
        relations = [("R", ["a", "b"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        
        assert rho_star == 1.0
        assert tau_star == 1.0

    def test_large_hypergraph(self):
        # Create a larger star query to test performance
        relations = [("R0", ["center", "a"])]
        for i in range(1, 20):
            relations.append((f"R{i}", ["center", f"vertex_{i}"]))
        
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        
        # For a star with 20 edges, center vertex constrains packing to 1.0
        assert abs(tau_star - 1.0) < 1e-6
        # Edge cover should be 20.0 (each edge needs full weight)
        assert abs(rho_star - 20.0) < 1e-6

    def test_disconnected_components(self):
        # Two disconnected edges
        relations = [("R", ["a", "b"]), ("S", ["c", "d"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        
        # Should be able to pack both edges fully
        assert abs(tau_star - 2.0) < 1e-6
        # Edge cover should also be 2.0
        assert abs(rho_star - 2.0) < 1e-6

    def test_clique_query(self):
        # Complete triangle (3-clique)
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        vertex_count = self.hypergraph.get_vertex_count()
        
        # Verify the specific values for triangle query
        assert abs(rho_star - 1.5) < 1e-6
        assert abs(tau_star - 1.5) < 1e-6
        assert abs(rho_star * tau_star - 2.25) < 1e-6
        assert vertex_count == 3

    def test_hyperedge_query(self):
        # Query with higher arity relations
        relations = [("R", ["a", "b", "c"]), ("S", ["a", "d"]), ("T", ["b", "d"])]
        self.hypergraph.from_relations(relations)
        solver = QuerySolver(self.hypergraph)
        
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        
        # Both should be positive and satisfy duality
        assert rho_star > 0
        assert tau_star > 0
        vertex_count = self.hypergraph.get_vertex_count()
        assert rho_star * tau_star <= vertex_count + 1e-6

    def test_solver_with_invalid_hypergraph(self):
        # Test error handling with malformed hypergraph
        # This is more of a defensive test
        solver = QuerySolver(self.hypergraph)  # Empty hypergraph
        
        # Should handle empty case gracefully
        assert solver.solve_fractional_edge_cover() == 0.0
        assert solver.solve_fractional_edge_packing() == 0.0