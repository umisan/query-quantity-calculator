import streamlit as st
import pandas as pd
from .parser import DatalogParser
from .hypergraph import Hypergraph
from .solver import QuerySolver


def main():
    st.title("Query Quantity Calculator")
    st.markdown("Calculate Fractional Edge Cover, Packing, and AGM Bound from Datalog-style queries")
    
    st.subheader("📥 Query Input")
    st.markdown("**Format Example:**")
    st.code("""R(a, b)
S(b, c)
T(a, c)""")
    
    query_input = st.text_area(
        "Enter your Datalog query:",
        value="R(a, b)\nS(b, c)\nT(a, c)",
        height=150
    )
    
    if st.button("Execute Calculation"):
        try:
            parser = DatalogParser()
            relations = parser.parse_query(query_input)
            
            if not relations:
                st.error("No valid query has been entered")
                return
            
            hypergraph = Hypergraph()
            hypergraph.from_relations(relations)
            
            solver = QuerySolver(hypergraph)
            
            rho_star = solver.solve_fractional_edge_cover()
            tau_star = solver.solve_fractional_edge_packing()
            agm_bound = solver.compute_agm_bound()
            
            vertex_count = hypergraph.get_vertex_count()
            edge_count = hypergraph.get_edge_count()
            rank = hypergraph.get_rank()
            product = rho_star * tau_star
            
            st.subheader("📊 Analysis Results")
            
            results_df = pd.DataFrame({
                "Item": [
                    "Number of Vertices (|V|)",
                    "Number of Edges (|E|)",
                    "Hypergraph Rank",
                    "Fractional Edge Cover (ρ*)",
                    "Fractional Edge Packing (τ*)",
                    "AGM Bound",
                    "ρ* × τ*"
                ],
                "Value": [
                    vertex_count,
                    edge_count,
                    rank,
                    f"{rho_star:.6f}",
                    f"{tau_star:.6f}",
                    f"{agm_bound:.6f}",
                    f"{product:.6f}"
                ]
            })
            
            st.dataframe(results_df, use_container_width=True)
            
            st.subheader("📈 Interpretation")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Verification: ρ* × τ* ≤ |V|",
                    value=f"{product:.3f} ≤ {vertex_count}",
                    delta=f"Difference: {vertex_count - product:.3f}"
                )
            
            with col2:
                ratio = product / vertex_count if vertex_count > 0 else 0
                st.metric(
                    label="Ratio (ρ* × τ*) / |V|",
                    value=f"{ratio:.3f}",
                    delta=f"{(1-ratio)*100:.1f}% margin"
                )
            
            st.subheader("🎨 Hypergraph Visualization")
            visualization = hypergraph.create_visualization()
            if visualization:
                st.plotly_chart(visualization, use_container_width=True)
            else:
                st.warning("Unable to display hypergraph")
            
            st.subheader("🔍 Query Details")
            relations_df = pd.DataFrame({
                "Relation Name": [rel[0] for rel in relations],
                "Arguments": [", ".join(rel[1]) for rel in relations],
                "Arity": [len(rel[1]) for rel in relations]
            })
            st.dataframe(relations_df, use_container_width=True)
            
        except ValueError as e:
            st.error(f"Parse Error: {e}")
        except RuntimeError as e:
            st.error(f"Calculation Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()