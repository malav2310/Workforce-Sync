from fastapi import APIRouter, HTTPException
from app.services.scheduler import Scheduler
import networkx as nx
from typing import Dict, List

router = APIRouter(prefix="/scheduler", tags=["scheduler"])
scheduler = Scheduler()

@router.get("/assigned-schedules")
async def get_all_assigned_schedules() -> Dict[str, Dict[str, Dict[str, List[Dict]]]]:
    """
    Get assigned employee schedules for all roles, grouped by role and day, based on maximum bipartite matching.
    Returns a JSON response with roles as top-level keys, then days, each containing a list of employees with their shift times.
    """
    # Create single bipartite graph for all roles
    graph, top_nodes = scheduler.create_bipartite_graph()
    
    # Compute maximum bipartite matching
    matching = scheduler.compute_maximum_matching(graph, top_nodes)
    
    # Initialize response structure
    response = {}
    
    # Process matching to group by role and day
    for emp_node, slot_node in matching.items():
        if emp_node in top_nodes:  # Only process employee-to-slot matches
            emp_data = graph.nodes[emp_node]
            role, day = emp_data["role"], emp_data["day"]
            
            # Initialize role and day in response if not present
            if role not in response:
                response[role] = {}
            if day not in response[role]:
                response[role][day] = {"employees": []}
            
            # Add employee schedule to the day's employees list
            response[role][day]["employees"].append({
                "id": emp_node,
                "shift": {
                    "start": emp_data["start"].strftime("%H:%M"),
                    "end": emp_data["end"].strftime("%H:%M")
                }
            })
    
    return response