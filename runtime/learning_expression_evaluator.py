from __future__ import annotations

import ast
import math


class LearningExpressionEvaluator:
    """Safely evaluate a small, whitelisted mathematical expression language."""

    def evaluate(self, expression: str) -> float:
        expression = expression.strip()

        if not expression:
            raise ValueError("EXPRESSION_CANNOT_BE_EMPTY")

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError("INVALID_EXPRESSION") from exc

        value = self._evaluate_node(tree.body)

        if not math.isfinite(value):
            raise ValueError("NON_FINITE_RESULT")

        return float(value)

    def _evaluate_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("INVALID_CONSTANT")

            if isinstance(node.value, (int, float)):
                return float(node.value)

            raise ValueError("INVALID_CONSTANT")

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -self._evaluate_node(node.operand)

            if isinstance(node.op, ast.UAdd):
                return self._evaluate_node(node.operand)

            raise ValueError("UNSUPPORTED_OPERATOR")

        if isinstance(node, ast.BinOp):
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)

            if isinstance(node.op, ast.Add):
                return left + right

            if isinstance(node.op, ast.Sub):
                return left - right

            if isinstance(node.op, ast.Mult):
                return left * right

            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ValueError("DIVISION_BY_ZERO")
                return left / right

            raise ValueError("UNSUPPORTED_OPERATOR")

        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "exp"
                and len(node.args) == 1
                and not node.keywords
            ):
                argument = self._evaluate_node(node.args[0])
                try:
                    return math.exp(argument)
                except OverflowError as exc:
                    raise ValueError("NUMERICAL_OVERFLOW") from exc

            raise ValueError("UNSUPPORTED_FUNCTION")

        raise ValueError("UNSUPPORTED_EXPRESSION")
