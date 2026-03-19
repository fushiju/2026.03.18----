"""
数据库查询工具 - 用于查询分佣记录等数据验证
"""
import logging

import pymysql
from pymysql import cursors

from config import config

logger = logging.getLogger(__name__)


class DBHelper:
    """MySQL 查询工具"""

    def __init__(self, db_config=None):
        self._config = db_config or config.get("database", {})

    def _connect(self):
        return pymysql.connect(
            host=self._config.get("host", "localhost"),
            port=self._config.get("port", 3306),
            user=self._config.get("user", "root"),
            password=self._config.get("password", ""),
            database=self._config.get("database", ""),
            charset=self._config.get("charset", "utf8mb4"),
            cursorclass=cursors.DictCursor,
        )

    def query(self, sql, params=None):
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        finally:
            conn.close()

    def query_one(self, sql, params=None):
        rows = self.query(sql, params)
        return rows[0] if rows else None

    # ---- 分佣业务查询 ----

    def get_order_commission(self, order_id):
        """查询订单分佣记录"""
        sql = """
            SELECT role_type, user_id, amount, bear_from, status
            FROM order_commission
            WHERE order_id = %s
            ORDER BY role_type
        """
        return self.query(sql, (order_id,))

    def get_order_detail(self, order_id):
        """查询订单详情"""
        sql = """
            SELECT id, order_no, service_fee, material_fee, travel_fee,
                   coupon_amount, total_amount, status,
                   technician_id, agent_id
            FROM orders
            WHERE id = %s
        """
        return self.query_one(sql, (order_id,))

    def get_order_refund(self, order_id):
        """查询订单退款记录"""
        sql = """
            SELECT id, order_id, refund_amount, refund_type,
                   refund_status, audit_status
            FROM order_refund
            WHERE order_id = %s
        """
        return self.query(sql, (order_id,))
