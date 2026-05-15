"""DAG 验证与拓扑排序 - task-decomposition"""

from collections import defaultdict, deque
from typing import List, Dict, Set, Tuple


class DAGValidationError(Exception):
    """DAG 验证错误"""
    pass


class CycleDetectedError(DAGValidationError):
    """检测到循环依赖"""
    pass


class InvalidReferenceError(DAGValidationError):
    """无效的依赖引用（前向引用）"""
    pass


def validate_dag(subtasks: List[Dict]) -> Tuple[bool, str]:
    """
    验证子任务列表是否为有效的 DAG
    
    Args:
        subtasks: 子任务列表，每个子任务包含 id 和 depends_on
        
    Returns:
        (是否有效, 错误信息)
    """
    if not subtasks:
        return False, "子任务列表为空"
    
    # 构建节点集合
    node_ids: Set[str] = {s["id"] for s in subtasks}
    
    # 验证所有依赖引用是否有效
    for subtask in subtasks:
        for dep_id in subtask.get("depends_on", []):
            if dep_id not in node_ids:
                return False, f"子任务 '{subtask['id']}' 引用了不存在的依赖 '{dep_id}'"
    
    # Kahn's algorithm 拓扑排序
    # 计算入度
    in_degree = defaultdict(int)
    for subtask in subtasks:
        if subtask["id"] not in in_degree:
            in_degree[subtask["id"]] = 0
        for dep_id in subtask.get("depends_on", []):
            in_degree[dep_id]  # 确保所有节点都在 in_degree 中
            in_degree[subtask["id"]] += 1
    
    # 拓扑排序
    queue = deque([node for node in node_ids if in_degree[node] == 0])
    sorted_nodes = []
    
    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        
        # 找到所有以 node 为依赖的节点
        for subtask in subtasks:
            if node in subtask.get("depends_on", []):
                in_degree[subtask["id"]] -= 1
                if in_degree[subtask["id"]] == 0:
                    queue.append(subtask["id"])
    
    # 检查是否有环（拓扑排序后节点数 < 总节点数）
    if len(sorted_nodes) != len(node_ids):
        return False, "子任务存在循环依赖"
    
    return True, ""


def get_topological_order(subtasks: List[Dict]) -> List[str]:
    """
    获取拓扑排序后的节点顺序（Kahn's algorithm）
    
    Args:
        subtasks: 子任务列表
        
    Returns:
        拓扑排序后的节点 ID 列表
        
    Raises:
        CycleDetectedError: 如果存在循环依赖
        InvalidReferenceError: 如果存在无效引用
    """
    if not subtasks:
        return []
    
    # 构建节点集合
    node_ids: Set[str] = {s["id"] for s in subtasks}
    
    # 构建邻接表和入度
    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {node: 0 for node in node_ids}
    
    for subtask in subtasks:
        task_id = subtask["id"]
        for dep_id in subtask.get("depends_on", []):
            if dep_id not in node_ids:
                raise InvalidReferenceError(f"子任务 '{task_id}' 引用了不存在的依赖 '{dep_id}'")
            adjacency[dep_id].append(task_id)
            in_degree[task_id] += 1
    
    # Kahn's algorithm
    queue = deque([node for node in node_ids if in_degree[node] == 0])
    sorted_nodes = []
    
    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        
        for neighbor in adjacency[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(sorted_nodes) != len(node_ids):
        raise CycleDetectedError("子任务存在循环依赖")
    
    return sorted_nodes


def get_ready_tasks(
    completed_ids: Set[str],
    subtasks: List[Dict]
) -> List[Dict]:
    """
    获取当前可执行的任务（所有依赖都已完成）
    
    Args:
        completed_ids: 已完成的子任务 ID 集合
        subtasks: 所有子任务列表
        
    Returns:
        可执行的子任务列表
    """
    ready = []
    pending_ids = {s["id"] for s in subtasks if s.get("status") == "pending"}
    
    for subtask in subtasks:
        if subtask["id"] in pending_ids:
            deps = set(subtask.get("depends_on", []))
            if deps.issubset(completed_ids):
                ready.append(subtask)
    
    return ready


def get_execution_plan(subtasks: List[Dict]) -> List[List[str]]:
    """
    生成分层执行计划（同一层的任务可以并行执行）
    
    Args:
        subtasks: 子任务列表
        
    Returns:
        分层任务 ID 列表，例如 [["task-1"], ["task-2", "task-3"], ["task-4"]]
        表示 task-1 先执行，然后 task-2 和 task-3 可以并行，最后 task-4
    """
    if not subtasks:
        return []
    
    topological_order = get_topological_order(subtasks)
    
    # 反向构建：找到每个节点的后继
    node_ids = {s["id"] for s in subtasks}
    successors: Dict[str, Set[str]] = {node: set() for node in node_ids}
    
    for subtask in subtasks:
        task_id = subtask["id"]
        for dep_id in subtask.get("depends_on", []):
            successors[dep_id].add(task_id)
    
    # 分层
    layers: List[List[str]] = []
    remaining = set(node_ids)
    
    while remaining:
        # 找到没有前驱的节点（在 remaining 中）
        layer = []
        for node in remaining:
            deps = set()
            for subtask in subtasks:
                if subtask["id"] == node:
                    deps = set(subtask.get("depends_on", []))
                    break
            if deps.isdisjoint(remaining):
                layer.append(node)
        
        if not layer:
            # 不应该发生，因为上面已验证无环
            break
        
        layers.append(layer)
        remaining -= set(layer)
    
    return layers
