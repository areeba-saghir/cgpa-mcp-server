import os

from fastmcp import FastMCP

from tools import (
    calculate_cgpa,
    check_target_reachable,
    get_credit_hours,
    grade_to_points,
    project_cgpa,
    required_semester_gpa,
)

mcp = FastMCP("cgpa")

mcp.tool(get_credit_hours)
mcp.tool(grade_to_points)
mcp.tool(calculate_cgpa)
mcp.tool(project_cgpa)
mcp.tool(required_semester_gpa)
mcp.tool(check_target_reachable)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
    )
