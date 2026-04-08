"""
断言辅助函数 - 提供常用断言封装
"""
from typing import Any, Dict, List, Optional, Union


class APIAssertions:
    """API响应断言辅助类"""

    @staticmethod
    def assert_success(response: Dict[str, Any], msg: str = None):
        """
        断言success=True

        Args:
            response: API响应数据
            msg: 失败时的自定义消息
        """
        assert response.get('success') is True, \
            msg or f"期望success=True，实际: {response}"

    @staticmethod
    def assert_success_code(response: Dict[str, Any], expected_code: Union[str, int] = '200', msg: str = None):
        """
        断言业务状态码

        Args:
            response: API响应数据
            expected_code: 期望的状态码
            msg: 失败时的自定义消息
        """
        actual_code = response.get('code') or response.get('statusCode')
        assert str(actual_code) == str(expected_code), \
            msg or f"期望code={expected_code}，实际: {response.get('code')}"

    @staticmethod
    def assert_fail(response: Dict[str, Any], msg: str = None):
        """
        断言success=False

        Args:
            response: API响应数据
            msg: 失败时的自定义消息
        """
        assert response.get('success') is False, \
            msg or f"期望success=False，实际: {response}"

    @staticmethod
    def assert_contains(response: Dict[str, Any], key: str, msg: str = None):
        """
        断言响应包含指定字段

        Args:
            response: API响应数据
            key: 字段名(支持嵌套如'data.list')
            msg: 失败时的自定义消息
        """
        keys = key.split('.')
        current = response
        for k in keys:
            assert isinstance(current, dict) and k in current, \
                msg or f"响应中不包含字段 '{key}'，实际: {response}"
            current = current[k]

    @staticmethod
    def assert_not_contains(response: Dict[str, Any], key: str, msg: str = None):
        """
        断言响应不包含指定字段或字段为空

        Args:
            response: API响应数据
            key: 字段名(支持嵌套)
            msg: 失败时的自定义消息
        """
        keys = key.split('.')
        current = response
        try:
            for k in keys:
                current = current[k]
            # 能走到这里说明字段存在且有值
            assert False, msg or f"期望不包含字段 '{key}'，但实际存在且值为: {current}"
        except (KeyError, TypeError, IndexError):
            # 字段不存在或为None，符合预期
            pass

    @staticmethod
    def assert_equal(actual: Any, expected: Any, msg: str = None):
        """
        断言相等

        Args:
            actual: 实际值
            expected: 期望值
            msg: 失败时的自定义消息
        """
        assert actual == expected, msg or f"期望 {expected}，实际 {actual}"

    @staticmethod
    def assert_in(actual: Any, expected_list: List[Any], msg: str = None):
        """
        断言值在列表中

        Args:
            actual: 实际值
            expected_list: 期望列表
            msg: 失败时的自定义消息
        """
        assert actual in expected_list, \
            msg or f"期望值在 {expected_list} 中，实际: {actual}"

    @staticmethod
    def assert_not_in(actual: Any, expected_list: List[Any], msg: str = None):
        """
        断言值不在列表中

        Args:
            actual: 实际值
            expected_list: 排除列表
            msg: 失败时的自定义消息
        """
        assert actual not in expected_list, \
            msg or f"期望值不在 {expected_list} 中，实际: {actual}"

    @staticmethod
    def assert_greater(actual: Union[int, float], expected: Union[int, float], msg: str = None):
        """断言actual > expected"""
        assert actual > expected, msg or f"期望 {actual} > {expected}"

    @staticmethod
    def assert_less(actual: Union[int, float], expected: Union[int, float], msg: str = None):
        """断言actual < expected"""
        assert actual < expected, msg or f"期望 {actual} < {expected}"

    @staticmethod
    def assert_between(actual: Union[int, float], min_val: Union[int, float], max_val: Union[int, float], msg: str = None):
        """断言min_val <= actual <= max_val"""
        assert min_val <= actual <= max_val, \
            msg or f"期望 {min_val} <= {actual} <= {max_val}"

    @staticmethod
    def assert_list_not_empty(response: Dict[str, Any], list_key: str = 'data.list', msg: str = None):
        """
        断言列表不为空

        Args:
            response: API响应数据
            list_key: 列表字段路径
            msg: 失败时的自定义消息
        """
        keys = list_key.split('.')
        current = response
        for k in keys:
            current = current[k]
        assert isinstance(current, list) and len(current) > 0, \
            msg or f"期望列表不为空，实际: {current}"

    @staticmethod
    def assert_list_empty(response: Dict[str, Any], list_key: str = 'data.list', msg: str = None):
        """
        断言列表为空

        Args:
            response: API响应数据
            list_key: 列表字段路径
            msg: 失败时的自定义消息
        """
        keys = list_key.split('.')
        current = response
        for k in keys:
            current = current[k]
        assert isinstance(current, list) and len(current) == 0, \
            msg or f"期望列表为空，实际: {current}"

    @staticmethod
    def assert_pagination(response: Dict[str, Any], expected_page: int = None, expected_size: int = None):
        """
        断言分页结构

        Args:
            response: API响应数据
            expected_page: 期望的页码
            expected_size: 期望的页大小
        """
        data = response.get('data', {})
        assert isinstance(data, dict), f"data应为dict，实际: {type(data)}"

        if expected_page is not None:
            assert data.get('pageNum') == expected_page or data.get('page') == expected_page, \
                f"期望pageNum={expected_page}，实际: {data.get('pageNum')}"

        if expected_size is not None:
            assert data.get('pageSize') == expected_size or data.get('size') == expected_size, \
                f"期望pageSize={expected_size}，实际: {data.get('pageSize')}"

        assert 'total' in data or 'totalCount' in data, \
            f"分页响应应包含total字段，实际: {data}"

    @staticmethod
    def assert_total(response: Dict[str, Any], expected_total: int = None, min_total: int = None):
        """
        断言总数

        Args:
            response: API响应数据
            expected_total: 期望的总数
            min_total: 最小总数
        """
        data = response.get('data', {})
        total = data.get('total') or data.get('totalCount')
        assert total is not None, f"响应中未找到total字段: {data}"

        if expected_total is not None:
            assert total == expected_total, f"期望total={expected_total}，实际: {total}"
        if min_total is not None:
            assert total >= min_total, f"期望total>={min_total}，实际: {total}"

    @staticmethod
    def assert_error_message(response: Dict[str, Any], expected_msg: str = None, msg: str = None):
        """
        断言错误消息包含指定内容

        Args:
            response: API响应数据
            expected_msg: 期望的错误消息关键词
            msg: 失败时的自定义消息
        """
        actual_msg = response.get('msg') or response.get('message') or response.get('error')
        if expected_msg:
            assert expected_msg in str(actual_msg), \
                msg or f"期望错误消息包含 '{expected_msg}'，实际: {actual_msg}"
        else:
            assert actual_msg, msg or f"期望有错误消息，实际: {response}"
