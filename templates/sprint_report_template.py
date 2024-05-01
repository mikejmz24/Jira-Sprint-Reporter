from entities.sprint_report_api import (
    JiraIssueSprintReport,
    SprintReport,
    get_active_developers,
    get_all_jira_issues_from_sprint_report,
    set_issue_type,
)


def sprint_report_template(sprint: SprintReport) -> str:
    res = f"""
    This document presents the goals and details of this sprint, aligned to the commitments defined in the 
    Team Agreement document, to serve as a sprint tracking tool.<br />
    {sprint_date_table(sprint)}<br />
    {sprint_goal_info(sprint)}
    {all_pbis(sprint)}
    """
    res = res.replace("&", "&amp;")
    return res


def all_pbis(sprint: SprintReport) -> str:
    return f"""
    <h2>Sprint Work Items</h2>
    <strong style="color: rgb(255,102,0)">All PBIs</strong><br />
    {print_all_pbis(sprint)}
    """


def print_all_pbis(sprint: SprintReport) -> str:
    res: str = f"""
    <table>
        <tbody>
            <tr>
                <th style="text-align: center">Issue</th>
                <th style="text-align: center">Type</th>
                <th style="text-align: center">Assignee</th>
                <th style="text-align: center">Priority</th>
                <th style="text-align: center">Status</th>
                <th style="text-align: center">Resolution</th>
            </tr>{print_all_pbis_tr(sprint)}
        </tbody>
    </table>
    """
    return res


def print_all_pbis_tr(sprint: SprintReport) -> str:
    all_issues: list[JiraIssueSprintReport] = get_all_jira_issues_from_sprint_report(
        sprint
    )
    res: str = ""
    for issue in all_issues:
        issue = set_issue_type(issue, sprint.issue_types, "issue_type")
        issue = set_issue_type(issue, sprint.priority_types, "issue_priority")
        issue = set_issue_type(issue, sprint.status_types, "issue_status")
        res += f"""
            <tr>
                <td style="text-align: left"><a href="https://jira.amer.thermo.com/browse/{issue.key}">{issue.key}: {issue.summary}</a></td>
                <td style="text-align: left">{issue.issue_type}</td>
                <td style="text-align: left">{issue.assignee}</td>
                <td style="text-align: left">{issue.issue_priority}</td>
                <td style="text-align: left">{issue.issue_status}</td>
                <td style="text-align: center">{issue.resolution}</td>
            </tr>"""
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
    <ac:structured-macro ac:name="{type_name}">
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
