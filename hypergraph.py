from typing import List, Tuple, Set, Dict
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np
from parser import DatalogParser


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
        
        # NetworkXグラフを作成（バイパータイトグラフとして表現）
        G = nx.Graph()
        
        # 頂点ノードを追加
        vertex_nodes = []
        for vertex in self.vertices:
            vertex_nodes.append(f"v_{vertex}")
            G.add_node(f"v_{vertex}", node_type='vertex', label=vertex)
        
        # エッジノードを追加（ハイパーエッジを表現）
        edge_nodes = []
        for i, (edge_name, edge_vertices) in enumerate(self.edges):
            edge_node = f"e_{i}_{edge_name}"
            edge_nodes.append(edge_node)
            G.add_node(edge_node, node_type='edge', label=edge_name)
            
            # エッジノードと対応する頂点ノードを接続
            for vertex in edge_vertices:
                G.add_edge(f"v_{vertex}", edge_node)
        
        # レイアウトを計算
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # 頂点ノードの座標
        vertex_x = [pos[node][0] for node in vertex_nodes if node in pos]
        vertex_y = [pos[node][1] for node in vertex_nodes if node in pos]
        vertex_labels = [G.nodes[node]['label'] for node in vertex_nodes if node in pos]
        
        # エッジノードの座標
        edge_x = [pos[node][0] for node in edge_nodes if node in pos]
        edge_y = [pos[node][1] for node in edge_nodes if node in pos]
        edge_labels = [G.nodes[node]['label'] for node in edge_nodes if node in pos]
        
        # エッジの線を描画
        edge_trace_x = []
        edge_trace_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace_x.extend([x0, x1, None])
            edge_trace_y.extend([y0, y1, None])
        
        # Plotlyの図を作成
        fig = go.Figure()
        
        # エッジの線を追加
        fig.add_trace(go.Scatter(
            x=edge_trace_x, y=edge_trace_y,
            line=dict(width=2, color='lightgray'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # 頂点ノードを追加
        fig.add_trace(go.Scatter(
            x=vertex_x, y=vertex_y,
            mode='markers+text',
            marker=dict(
                size=20,
                color='lightblue',
                line=dict(width=2, color='darkblue')
            ),
            text=vertex_labels,
            textposition="middle center",
            hoverinfo='text',
            hovertext=[f"頂点: {label}" for label in vertex_labels],
            name="頂点",
            showlegend=True
        ))
        
        # エッジノードを追加
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='markers+text',
            marker=dict(
                size=25,
                color='lightcoral',
                line=dict(width=2, color='darkred'),
                symbol='square'
            ),
            text=edge_labels,
            textposition="middle center",
            hoverinfo='text',
            hovertext=[f"リレーション: {label}" for label in edge_labels],
            name="リレーション",
            showlegend=True
        ))
        
        # レイアウトを設定
        fig.update_layout(
            title="ハイパーグラフ構造",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="円: 頂点（変数）, 四角: リレーション（エッジ）",
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