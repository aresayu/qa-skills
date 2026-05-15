"""DAG 验证与拓扑排序测试"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入 dag 模块，避免触发 __init__.py 的依赖问题
import importlib.util
dag_spec = importlib.util.spec_from_file_location("dag", "scripts/dag.py")
dag_module = importlib.util.module_from_spec(dag_spec)
dag_spec.loader.exec_module(dag_module)

validate_dag = dag_module.validate_dag
get_topological_order = dag_module.get_topological_order
get_execution_plan = dag_module.get_execution_plan
get_ready_tasks = dag_module.get_ready_tasks
CycleDetectedError = dag_module.CycleDetectedError
InvalidReferenceError = dag_module.InvalidReferenceError

# 测试用例
def run_tests():
    print("=" * 60)
    print("DAG 验证与拓扑排序测试")
    print("=" * 60)

    # 测试 1: 正常 DAG
    print("\n【测试 1】正常 DAG（线性依赖）")
    subtasks_1 = [
        {"id": "task-1", "depends_on": []},
        {"id": "task-2", "depends_on": ["task-1"]},
        {"id": "task-3", "depends_on": ["task-2"]},
    ]
    is_valid, error = validate_dag(subtasks_1)
    order = get_topological_order(subtasks_1)
    print(f"  验证结果: {'✓ 通过' if is_valid else '✗ 失败'} {error}")
    print(f"  拓扑顺序: {order}")

    # 测试 2: 并行 DAG
    print("\n【测试 2】并行 DAG（task-2 和 task-3 无依赖）")
    subtasks_2 = [
        {"id": "task-1", "depends_on": []},
        {"id": "task-2", "depends_on": ["task-1"]},
        {"id": "task-3", "depends_on": ["task-1"]},
        {"id": "task-4", "depends_on": ["task-2", "task-3"]},
    ]
    is_valid, error = validate_dag(subtasks_2)
    order = get_topological_order(subtasks_2)
    layers = get_execution_plan(subtasks_2)
    print(f"  验证结果: {'✓ 通过' if is_valid else '✗ 失败'} {error}")
    print(f"  拓扑顺序: {order}")
    print(f"  分层执行: {layers}")

    # 测试 3: 循环依赖
    print("\n【测试 3】循环依赖检测")
    subtasks_3 = [
        {"id": "task-1", "depends_on": ["task-3"]},
        {"id": "task-2", "depends_on": ["task-1"]},
        {"id": "task-3", "depends_on": ["task-2"]},
    ]
    is_valid, error = validate_dag(subtasks_3)
    print(f"  验证结果: {'✓ 通过' if is_valid else '✗ 失败'} - {error if not is_valid else ''}")

    # 测试 4: 前向引用
    print("\n【测试 4】前向引用检测")
    subtasks_4 = [
        {"id": "task-1", "depends_on": []},
        {"id": "task-2", "depends_on": ["non-existent"]},
    ]
    is_valid, error = validate_dag(subtasks_4)
    print(f"  验证结果: {'✓ 通过' if is_valid else '✗ 失败'} - {error if not is_valid else ''}")

    # 测试 5: 空列表
    print("\n【测试 5】空列表检测")
    is_valid, error = validate_dag([])
    print(f"  验证结果: {'✓ 通过' if is_valid else '✗ 失败'} - {error if not is_valid else ''}")

    # 测试 6: 复杂 DAG
    print("\n【测试 6】复杂 DAG（真实场景模拟）")
    subtasks_6 = [
        {"id": "setup-env", "depends_on": [], "title": "环境搭建"},
        {"id": "design-db", "depends_on": [], "title": "数据库设计"},
        {"id": "write-backend", "depends_on": ["setup-env", "design-db"], "title": "后端开发"},
        {"id": "write-frontend", "depends_on": ["setup-env"], "title": "前端开发"},
        {"id": "write-tests", "depends_on": ["write-backend"], "title": "编写测试"},
        {"id": "deploy", "depends_on": ["write-backend", "write-frontend", "write-tests"], "title": "部署"},
    ]
    is_valid, error = validate_dag(subtasks_6)
    order = get_topological_order(subtasks_6)
    layers = get_execution_plan(subtasks_6)
    print(f"  验证结果: {'✓ 通过' if is_valid else '✗ 失败'} {error}")
    print(f"  拓扑顺序: {order}")
    print(f"  分层执行:")
    for i, layer in enumerate(layers):
        print(f"    第 {i+1} 层（可并行）: {layer}")

    # 测试 7: get_ready_tasks
    print("\n【测试 7】获取可执行任务")
    completed = {"setup-env", "design-db"}
    ready = get_ready_tasks(completed, subtasks_6)
    print(f"  已完成: {completed}")
    print(f"  可执行: {[t['id'] for t in ready]}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
