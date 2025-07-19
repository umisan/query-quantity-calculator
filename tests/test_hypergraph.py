import pytest
from src.query_quantity_calculator.hypergraph import Hypergraph


class TestHypergraph:
    def setup_method(self):
        self.hypergraph = Hypergraph()

    def test_from_relations_simple(self):
        relations = [("R", ["a", "b"])]
        self.hypergraph.from_relations(relations)
        
        assert self.hypergraph.get_vertex_count() == 2
        assert self.hypergraph.get_edge_count() == 1
        assert "a" in self.hypergraph.vertices
        assert "b" in self.hypergraph.vertices

    def test_from_relations_triangle(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        
        assert self.hypergraph.get_vertex_count() == 3
        assert self.hypergraph.get_edge_count() == 3
        assert self.hypergraph.vertices == {"a", "b", "c"}

    def test_get_vertex_count(self):
        relations = [("R", ["a", "b", "c"])]
        self.hypergraph.from_relations(relations)
        assert self.hypergraph.get_vertex_count() == 3

    def test_get_edge_count(self):
        relations = [("R", ["a", "b"]), ("S", ["c", "d"])]
        self.hypergraph.from_relations(relations)
        assert self.hypergraph.get_edge_count() == 2

    def test_get_rank_various_sizes(self):
        # Test with edges of different sizes
        relations = [("R", ["a", "b"]), ("S", ["c", "d", "e"]), ("T", ["f"])]
        self.hypergraph.from_relations(relations)
        assert self.hypergraph.get_rank() == 3

    def test_get_rank_empty_edges(self):
        assert self.hypergraph.get_rank() == 0

    def test_get_edges_containing_vertex(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        self.hypergraph.from_relations(relations)
        
        edges_with_a = self.hypergraph.get_edges_containing_vertex("a")
        edges_with_b = self.hypergraph.get_edges_containing_vertex("b")
        edges_with_c = self.hypergraph.get_edges_containing_vertex("c")
        
        assert set(edges_with_a) == {0, 2}  # R and T
        assert set(edges_with_b) == {0, 1}  # R and S
        assert set(edges_with_c) == {1, 2}  # S and T

    def test_get_edges_containing_nonexistent_vertex(self):
        relations = [("R", ["a", "b"])]
        self.hypergraph.from_relations(relations)
        
        edges = self.hypergraph.get_edges_containing_vertex("z")
        assert edges == []

    def test_get_vertices_list_sorted(self):
        relations = [("R", ["c", "a", "b"])]
        self.hypergraph.from_relations(relations)
        
        vertices = self.hypergraph.get_vertices_list()
        assert vertices == ["a", "b", "c"]

    def test_get_edge_size(self):
        relations = [("R", ["a", "b"]), ("S", ["c", "d", "e"])]
        self.hypergraph.from_relations(relations)
        
        assert self.hypergraph.get_edge_size(0) == 2
        assert self.hypergraph.get_edge_size(1) == 3

    def test_get_edge_name(self):
        relations = [("R", ["a", "b"]), ("S", ["c", "d"])]
        self.hypergraph.from_relations(relations)
        
        assert self.hypergraph.get_edge_name(0) == "R"
        assert self.hypergraph.get_edge_name(1) == "S"

    def test_multiple_relations_same_vertices(self):
        relations = [("R", ["a", "b"]), ("S", ["a", "b"])]
        self.hypergraph.from_relations(relations)
        
        assert self.hypergraph.get_vertex_count() == 2
        assert self.hypergraph.get_edge_count() == 2

    def test_empty_relations(self):
        relations = []
        self.hypergraph.from_relations(relations)
        
        assert self.hypergraph.get_vertex_count() == 0
        assert self.hypergraph.get_edge_count() == 0
        assert self.hypergraph.get_rank() == 0

    def test_invalid_edge_index(self):
        relations = [("R", ["a", "b"])]
        self.hypergraph.from_relations(relations)
        
        with pytest.raises(IndexError):
            self.hypergraph.get_edge_size(1)
        
        with pytest.raises(IndexError):
            self.hypergraph.get_edge_name(1)

    def test_create_visualization_simple(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"])]
        self.hypergraph.from_relations(relations)
        
        fig = self.hypergraph.create_visualization()
        assert fig is not None
        assert hasattr(fig, 'data')

    def test_create_visualization_empty(self):
        fig = self.hypergraph.create_visualization()
        assert fig is None

    def test_create_visualization_single_vertex(self):
        # This would be an edge case - single vertex in isolation
        # But our model requires at least one relation
        relations = [("R", ["a"])]
        self.hypergraph.from_relations(relations)
        
        fig = self.hypergraph.create_visualization()
        # Should handle single vertex gracefully
        assert fig is not None

    def test_create_visualization_binary_edges(self):
        relations = [("R", ["a", "b"]), ("S", ["c", "d"])]
        self.hypergraph.from_relations(relations)
        
        fig = self.hypergraph.create_visualization()
        assert fig is not None

    def test_create_visualization_hyperedges(self):
        relations = [("R", ["a", "b", "c"]), ("S", ["b", "c", "d"])]
        self.hypergraph.from_relations(relations)
        
        fig = self.hypergraph.create_visualization()
        assert fig is not None

    def test_from_relations_clears_previous_data(self):
        # First set of relations
        relations1 = [("R", ["a", "b"])]
        self.hypergraph.from_relations(relations1)
        assert self.hypergraph.get_vertex_count() == 2
        
        # Second set of relations should clear the first
        relations2 = [("S", ["c", "d", "e"])]
        self.hypergraph.from_relations(relations2)
        assert self.hypergraph.get_vertex_count() == 3
        assert "a" not in self.hypergraph.vertices
        assert "b" not in self.hypergraph.vertices

    def test_large_hypergraph(self):
        # Test with a larger number of relations
        relations = []
        for i in range(10):
            relations.append((f"R{i}", [f"a{i}", f"b{i}", f"c{i}"]))
        
        self.hypergraph.from_relations(relations)
        assert self.hypergraph.get_vertex_count() == 30
        assert self.hypergraph.get_edge_count() == 10
        assert self.hypergraph.get_rank() == 3