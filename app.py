import streamlit as st
import pandas as pd
from parser import DatalogParser
from hypergraph import Hypergraph
from solver import QuerySolver


def main():
    st.title("Query Quantity Calculator")
    st.markdown("Datalog風のクエリからFractional Edge Cover、Packing、AGM Boundを計算します")
    
    st.subheader("📥 クエリ入力")
    st.markdown("**形式例:**")
    st.code("""R(a, b)
S(b, c)
T(a, c)""")
    
    query_input = st.text_area(
        "Datalogクエリを入力してください:",
        value="R(a, b)\nS(b, c)\nT(a, c)",
        height=150
    )
    
    if st.button("計算実行"):
        try:
            parser = DatalogParser()
            relations = parser.parse_query(query_input)
            
            if not relations:
                st.error("有効なクエリが入力されていません")
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
            
            st.subheader("📊 解析結果")
            
            results_df = pd.DataFrame({
                "項目": [
                    "頂点数 (|V|)",
                    "エッジ数 (|E|)",
                    "ハイパーグラフのrank",
                    "Fractional Edge Cover (ρ*)",
                    "Fractional Edge Packing (τ*)",
                    "AGM Bound",
                    "ρ* × τ*"
                ],
                "値": [
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
            
            st.subheader("📈 解釈")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="ρ* × τ* ≤ |V| の確認",
                    value=f"{product:.3f} ≤ {vertex_count}",
                    delta=f"差: {vertex_count - product:.3f}"
                )
            
            with col2:
                ratio = product / vertex_count if vertex_count > 0 else 0
                st.metric(
                    label="比率 (ρ* × τ*) / |V|",
                    value=f"{ratio:.3f}",
                    delta=f"{(1-ratio)*100:.1f}% の余裕"
                )
            
            st.subheader("🎨 ハイパーグラフ可視化")
            visualization = hypergraph.create_visualization()
            if visualization:
                st.plotly_chart(visualization, use_container_width=True)
            else:
                st.warning("ハイパーグラフを表示できません")
            
            st.subheader("🔍 クエリ詳細")
            relations_df = pd.DataFrame({
                "リレーション名": [rel[0] for rel in relations],
                "引数": [", ".join(rel[1]) for rel in relations],
                "アリティ": [len(rel[1]) for rel in relations]
            })
            st.dataframe(relations_df, use_container_width=True)
            
        except ValueError as e:
            st.error(f"パース エラー: {e}")
        except RuntimeError as e:
            st.error(f"計算エラー: {e}")
        except Exception as e:
            st.error(f"予期しないエラー: {e}")


if __name__ == "__main__":
    main()