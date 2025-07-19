import pytest
from src.query_quantity_calculator.parser import DatalogParser
from src.query_quantity_calculator.hypergraph import Hypergraph
from src.query_quantity_calculator.solver import QuerySolver


class TestIntegration:
    """End-to-end integration tests for the complete pipeline"""

    def test_end_to_end_triangle_query(self):
        """Test complete pipeline with triangle query"""
        query = "R(a, b)\nS(b, c)\nT(a, c)"
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify results
        assert hypergraph.get_vertex_count() == 3
        assert hypergraph.get_edge_count() == 3
        assert hypergraph.get_rank() == 2
        assert abs(rho_star - 1.5) < 1e-6
        assert abs(tau_star - 1.5) < 1e-6
        assert abs(agm_bound - 1.0) < 1e-6
        assert abs(rho_star * tau_star - 2.25) < 1e-6

    def test_end_to_end_star_query(self):
        """Test complete pipeline with star query"""
        query = "R(a, b)\nS(a, c)\nT(a, d)"
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify results
        assert hypergraph.get_vertex_count() == 4
        assert hypergraph.get_edge_count() == 3
        assert hypergraph.get_rank() == 2
        assert abs(rho_star - 3.0) < 1e-6
        assert abs(tau_star - 1.0) < 1e-6
        assert abs(agm_bound - 1.0) < 1e-6
        assert abs(rho_star * tau_star - 3.0) < 1e-6

    def test_end_to_end_path_query(self):
        """Test complete pipeline with path query"""
        query = "R(a, b)\nS(b, c)\nT(c, d)"
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify results
        assert hypergraph.get_vertex_count() == 4
        assert hypergraph.get_edge_count() == 3
        assert hypergraph.get_rank() == 2
        assert rho_star >= 1.5  # Path query should have this minimum
        assert tau_star <= 2.0  # Limited by internal vertices b and c
        assert abs(agm_bound - 1.0) < 1e-6

    def test_end_to_end_complex_query(self):
        """Test complete pipeline with a more complex query"""
        query = """R(a, b, c)
S(b, d)
T(c, e)
U(d, e, f)
V(a, f)"""
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify basic properties
        assert hypergraph.get_vertex_count() == 6  # a, b, c, d, e, f
        assert hypergraph.get_edge_count() == 5
        assert hypergraph.get_rank() == 3  # R and U have 3 vertices
        assert rho_star > 0
        assert tau_star > 0
        assert agm_bound > 0
        
        # Verify duality property
        vertex_count = hypergraph.get_vertex_count()
        assert rho_star * tau_star <= vertex_count + 1e-6

    def test_end_to_end_single_relation(self):
        """Test complete pipeline with single relation"""
        query = "R(a, b, c, d)"
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify results
        assert hypergraph.get_vertex_count() == 4
        assert hypergraph.get_edge_count() == 1
        assert hypergraph.get_rank() == 4
        assert abs(rho_star - 1.0) < 1e-6
        assert abs(tau_star - 1.0) < 1e-6
        assert abs(agm_bound - 1.0) < 1e-6

    def test_end_to_end_disconnected_query(self):
        """Test complete pipeline with disconnected components"""
        query = "R(a, b)\nS(c, d)\nT(e, f)"
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify results
        assert hypergraph.get_vertex_count() == 6
        assert hypergraph.get_edge_count() == 3
        assert hypergraph.get_rank() == 2
        assert abs(rho_star - 3.0) < 1e-6  # Each edge needs full weight
        assert abs(tau_star - 3.0) < 1e-6  # No conflicts, can pack all
        assert abs(agm_bound - 1.0) < 1e-6

    def test_end_to_end_hyperedge_query(self):
        """Test complete pipeline with higher arity relations"""
        query = "R(a, b, c, d, e)\nS(a, f)\nT(b, g)\nU(c, h)"
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify basic properties
        assert hypergraph.get_vertex_count() == 8  # a,b,c,d,e,f,g,h
        assert hypergraph.get_edge_count() == 4
        assert hypergraph.get_rank() == 5  # R has 5 vertices
        assert rho_star > 0
        assert tau_star > 0
        assert agm_bound > 0

    def test_end_to_end_error_handling(self):
        """Test error handling in complete pipeline"""
        # Invalid query should raise ValueError during parsing
        invalid_query = "R(a, b\nS(invalid"
        
        parser = DatalogParser()
        with pytest.raises(ValueError):
            parser.parse_query(invalid_query)

    def test_end_to_end_empty_query(self):
        """Test complete pipeline with empty query"""
        query = ""
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify results
        assert hypergraph.get_vertex_count() == 0
        assert hypergraph.get_edge_count() == 0
        assert hypergraph.get_rank() == 0
        assert rho_star == 0.0
        assert tau_star == 0.0
        assert agm_bound == 1.0

    def test_end_to_end_performance(self):
        """Test performance with a larger query"""
        # Create a query with many relations
        relations_text = []
        for i in range(20):
            relations_text.append(f"R{i}(x{i}, x{i+1})")
        query = "\n".join(relations_text)
        
        # Parse
        parser = DatalogParser()
        relations = parser.parse_query(query)
        
        # Build hypergraph
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Solve
        solver = QuerySolver(hypergraph)
        rho_star = solver.solve_fractional_edge_cover()
        tau_star = solver.solve_fractional_edge_packing()
        agm_bound = solver.compute_agm_bound()
        
        # Verify it completes successfully
        assert hypergraph.get_vertex_count() == 21  # x0 to x20
        assert hypergraph.get_edge_count() == 20
        assert rho_star > 0
        assert tau_star > 0

    def test_variable_extraction_integration(self):
        """Test variable extraction with the complete pipeline"""
        query = "R(x, y)\nS(y, z)\nT(x, z)"
        
        parser = DatalogParser()
        relations = parser.parse_query(query)
        all_variables = parser.get_all_variables(relations)
        
        hypergraph = Hypergraph()
        hypergraph.from_relations(relations)
        
        # Variables from parser should match vertices in hypergraph
        assert all_variables == hypergraph.vertices
        assert len(all_variables) == hypergraph.get_vertex_count()