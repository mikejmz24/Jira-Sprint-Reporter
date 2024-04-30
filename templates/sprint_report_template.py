from entities.sprint_report_api import SprintReport, get_active_developers


def sprint_report_template(sprint: SprintReport) -> str:
    res = f"""
    This document presents the goals and details of this sprint, aligned to the commitments defined in the 
    Team Agreement document, to serve as a sprint tracking tool.<br />
    {sprint_date_table(sprint)}
    {sprint_goal_table(sprint)}
    """
    return res


def sprint_goal_info(sprint: SprintReport) -> str:
    return f"""
    {info_macro("info", sprint_goal_table(sprint))}
    """


def sprint_goal_table(sprint: SprintReport) -> str:
    return f"""
    <h2>Sprint Goal</h2>
    <table>
        <tbody>
            <tr>
                <td style="text-align: center">{sprint.goal}</td>
                <td style="text-align: center">{status_macro("ACHIEVED")}</td>
                <td style="text-align: center">-- reason in case sprint goal not achieved --</td>
            </tr>
        </tbody>
    </table>
    """


def sprint_date_table(sprint: SprintReport) -> str:
    return f"""
    <table>
        <tbody>
            <tr>
                <th style="text-align: center">Start Date</th>
                <th style="text-align: center">End Date</th>
                <th style="text-align: center">Status</th>
                <th style="text-align: center">Team members with assigned issues</th>
            </tr>
            <tr>
                <td style="text-align: center"><time datetime="
                {sprint.start_date.strftime("%Y-%m-%d")}">
                {sprint.start_date.strftime("%d %b %Y")}</time></td>
                <td style="text-align: center"><time datetime="
                {sprint.end_date.strftime("%Y-%m-%d")}">
                {sprint.end_date.strftime("%d %b %Y")}</time></td>
                <td style="text-align: center">{status_macro("COMPLETED")}</td>
                <td style="text-align: center">{len(get_active_developers(sprint))}</td>
            </tr>
        </tbody>
    </table>
    """


def info_macro(type_name: str, msg: str, title: str = "") -> str:
    return f"""
    <ac:structured-macro ac:name={type_name}>
    <ac:parameter ac:name="title">{title}</ac:parameter>
    <ac:rich-text-body>
        {msg}
    </ac:rich-text-body>
    </ac:structured-macro>
    """


def status_macro(msg: str, color: str = "Green", subtle: bool = False) -> str:
    return f"""
    <ac:structured-macro ac:name="status">
    <ac:parameter ac:name="colour">{color}</ac:parameter>
    <ac:parameter ac:name="title">{msg}</ac:parameter>
    <ac:parameter ac:name="subtle">{subtle}</ac:parameter>
    </ac:structured-macro>
    """
