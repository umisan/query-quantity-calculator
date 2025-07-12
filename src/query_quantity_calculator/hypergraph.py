from typing import List, Tuple, Set, Dict
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np
from .parser import DatalogParser


class Hypergraph:
    def __init__(self):
        self.vertices: Set[str] = set()
        self.edges: List[Tuple[str, Set[str]]] = []
    
    def from_relations(self, relations: List[Tuple[str, List[str]]]):
        self.vertices.clear()
        self.edges.clear()
        
        for relation_name, args in relations:
            edge_vertices = set(args)
            self.vertices.update(edge_vertices)
            self.edges.append((relation_name, edge_vertices))
    
    def get_vertex_count(self) -> int:
        return len(self.vertices)
    
    def get_edge_count(self) -> int:
        return len(self.edges)
    
    def get_rank(self) -> int:
        if not self.edges:
            return 0
        return max(len(edge_vertices) for _, edge_vertices in self.edges)
    
    def get_edges_containing_vertex(self, vertex: str) -> List[int]:
        result = []
        for i, (_, edge_vertices) in enumerate(self.edges):
            if vertex in edge_vertices:
                result.append(i)
        return result
    
    def get_vertices_list(self) -> List[str]:
        return sorted(list(self.vertices))
    
    def get_edge_size(self, edge_index: int) -> int:
        return len(self.edges[edge_index][1])
    
    def get_edge_name(self, edge_index: int) -> str:
        return self.edges[edge_index][0]
    
    def create_visualization(self):
        """ハイパーグラフの可視化を作成"""
        if not self.vertices or not self.edges:
            return None
        
        # NetworkXグラフを作成（頂点のみのグラフ）
        G = nx.Graph()
        
        # 頂点のみを追加
        for vertex in self.vertices:
            G.add_node(vertex)
        
        # レイアウトを計算（頂点のみ）
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # 頂点の座標
        vertex_x = [pos[vertex][0] for vertex in self.vertices]
        vertex_y = [pos[vertex][1] for vertex in self.vertices]
        vertex_labels = list(self.vertices)
        
        # Plotlyの図を作成
        fig = go.Figure()
        
        # ハイパーエッジを描画（多角形として）
        colors = px.colors.qualitative.Set3
        for i, (edge_name, edge_vertices) in enumerate(self.edges):
            if len(edge_vertices) < 2:
                continue
                
            # エッジに含まれる頂点の座標を取得
            edge_vertex_list = list(edge_vertices)
            edge_x = [pos[v][0] for v in edge_vertex_list if v in pos]
            edge_y = [pos[v][1] for v in edge_vertex_list if v in pos]
            
            if len(edge_x) < 2:
                continue
            
            # 凸包を計算して多角形を描画
            if len(edge_x) >= 3:
                # 重心を計算
                center_x = sum(edge_x) / len(edge_x)
                center_y = sum(edge_y) / len(edge_y)
                
                # 角度でソート
                def angle_from_center(point_idx):
                    import math
                    return math.atan2(edge_y[point_idx] - center_y, edge_x[point_idx] - center_x)
                
                sorted_indices = sorted(range(len(edge_x)), key=angle_from_center)
                sorted_edge_x = [edge_x[i] for i in sorted_indices]
                sorted_edge_y = [edge_y[i] for i in sorted_indices]
                
                # 多角形を閉じる
                sorted_edge_x.append(sorted_edge_x[0])
                sorted_edge_y.append(sorted_edge_y[0])
                
                # ハイパーエッジを多角形として描画
                fig.add_trace(go.Scatter(
                    x=sorted_edge_x, y=sorted_edge_y,
                    fill="toself",
                    fillcolor=colors[i % len(colors)],
                    opacity=0.3,
                    line=dict(width=2, color=colors[i % len(colors)]),
                    hoverinfo='text',
                    hovertext=f"リレーション: {edge_name}<br>頂点: {', '.join(edge_vertex_list)}",
                    name=f"リレーション {edge_name}",
                    showlegend=True,
                    mode='lines'
                ))
            else:
                # 2頂点の場合は線として描画
                fig.add_trace(go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=4, color=colors[i % len(colors)]),
                    hoverinfo='text',
                    hovertext=f"リレーション: {edge_name}<br>頂点: {', '.join(edge_vertex_list)}",
                    name=f"リレーション {edge_name}",
                    showlegend=True,
                    mode='lines'
                ))
        
        # 頂点を最後に描画（上に表示されるように）
        fig.add_trace(go.Scatter(
            x=vertex_x, y=vertex_y,
            mode='markers+text',
            marker=dict(
                size=25,
                color='white',
                line=dict(width=3, color='darkblue')
            ),
            text=vertex_labels,
            textposition="middle center",
            hoverinfo='text',
            hovertext=[f"頂点: {label}" for label in vertex_labels],
            name="頂点（属性）",
            showlegend=True
        ))
        
        # レイアウトを設定
        fig.update_layout(
            title="ハイパーグラフ構造",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="白い円: 頂点（属性）, 色つき領域: ハイパーエッジ（リレーション）",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white'
        )
        
        return fig