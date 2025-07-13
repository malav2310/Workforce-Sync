from typing import List, Dict, Tuple
from datetime import time
import networkx as nx

class Scheduler:
    def __init__(self):
        # Initialize mocked data
        self.employee_schedules = self._initialize_employee_schedules()
        self.employer_slots = self._initialize_employer_slots()

    def _initialize_employee_schedules(self) -> Dict[str, List[Tuple[str, time, time]]]:
        """Initialize mocked employee schedules with day and time slot."""
        return {
            "bakeryClerk": [
                ("Monday", time(8, 0), time(14, 0)),  # Employee 1: Monday, 8:00 AM - 2:00 PM
                ("Monday", time(12, 0), time(18, 0)),  # Employee 2: Monday, 12:00 PM - 6:00 PM
                ("Tuesday", time(9, 0), time(15, 0))   # Employee 3: Tuesday, 9:00 AM - 3:00 PM
            ],
            "baker": [
                ("Tuesday", time(6, 0), time(12, 0)),  # Employee 1: Tuesday, 6:00 AM - 12:00 PM
                ("Tuesday", time(10, 0), time(16, 0)), # Employee 2: Tuesday, 10:00 AM - 4:00 PM
                ("Wednesday", time(7, 0), time(13, 0)) # Employee 3: Wednesday, 7:00 AM - 1:00 PM
            ]
        }

    def _initialize_employer_slots(self) -> Dict[str, List[Tuple[str, time, time]]]:
        """Initialize mocked employer-desired slots with day and time slot."""
        return {
            "bakeryClerk": [
                ("Monday", time(7, 0), time(15, 0)),  # Slot 1: Monday, 7:00 AM - 3:00 PM
                ("Monday", time(14, 0), time(22, 0)), # Slot 2: Monday, 2:00 PM - 10:00 PM
                ("Tuesday", time(8, 0), time(16, 0))  # Slot 3: Tuesday, 8:00 AM - 4:00 PM
            ],
            "baker": [
                ("Tuesday", time(5, 0), time(13, 0)),  # Slot 1: Tuesday, 5:00 AM - 1:00 PM
                ("Tuesday", time(12, 0), time(20, 0)), # Slot 2: Tuesday, 12:00 PM - 8:00 PM
                ("Wednesday", time(6, 0), time(14, 0)) # Slot 3: Wednesday, 6:00 AM - 2:00 PM
            ]
        }

    def create_bipartite_graph(self) -> Tuple[nx.Graph, List[str]]:
        """
        Create a single bipartite graph for all roles.
        Nodes: Employee schedules and employer slots across all roles.
        Edges: Connect schedules to slots with matching day and time overlap.
        Returns a tuple of (graph, top_nodes), where top_nodes are employee nodes.
        """
        # Initialize single bipartite graph and top_nodes list
        G = nx.Graph()
        top_nodes = []

        # Add nodes for employee schedules (Set 0) for all roles
        for role in self.employee_schedules.keys():
            if role not in self.employer_slots:
                continue
            for i, (day, start, end) in enumerate(self.employee_schedules[role]):
                node_id = f"{role}_emp_{i}"
                G.add_node(node_id, bipartite=0, day=day, start=start, end=end, role=role)
                top_nodes.append(node_id)

        # Add nodes for employer slots (Set 1) for all roles
        for role in self.employer_slots.keys():
            if role not in self.employee_schedules:
                continue
            for j, (day, start, end) in enumerate(self.employer_slots[role]):
                node_id = f"{role}_slot_{j}"
                G.add_node(node_id, bipartite=1, day=day, start=start, end=end, role=role)

        # Add edges where schedules and slots have the same day and overlapping times
        for emp_node in top_nodes:
            emp_data = G.nodes[emp_node]
            emp_day, emp_start, emp_end, emp_role = emp_data["day"], emp_data["start"], emp_data["end"], emp_data["role"]
            for slot_node in [n for n in G.nodes if n.startswith(emp_role + "_slot_")]:
                slot_data = G.nodes[slot_node]
                slot_day, slot_start, slot_end = slot_data["day"], slot_data["start"], slot_data["end"]
                if emp_day == slot_day and emp_start <= slot_end and emp_end >= slot_start:
                    G.add_edge(emp_node, slot_node)

        return G, top_nodes

    def compute_maximum_matching(self, graph: nx.Graph, top_nodes: List[str]) -> Dict[str, str]:
        """
        Compute the maximum bipartite matching for the given graph.
        Args:
            graph: A bipartite graph with employee and slot nodes.
            top_nodes: List of employee nodes (bipartite set 0).
        Returns:
            A dictionary mapping nodes to their matched nodes (employee to slot and vice versa).
        """
        return nx.algorithms.bipartite.maximum_matching(graph, top_nodes=top_nodes)