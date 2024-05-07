from typing import Optional

from entities.sprint_report_api import (
    JiraIssueSprintReport,
    SprintReport,
    get_active_developers,
    get_added_issues,
    get_all_jira_issues_from_sprint_report,
    get_total_commited_pbis,
)


def sprint_report_template(sprint: SprintReport, board: str) -> str:
    res = f"""
    This document presents the goals and details of this sprint, aligned to the commitments defined in the 
    Team Agreement document, to serve as a sprint tracking tool.<br />
    {sprint_date_table(sprint)}<br />
    {sprint_goal_info(sprint)}
    {all_pbis(sprint)}<br />
    {removed_pbis(sprint)}<br />
    {added_pbis(sprint)}<br />
    {total_items_table(sprint)}<br />
    {qppi_link(board)}<br /><br />
    {spillover_incomplete_pbis(sprint)}<br />
    {bugs_details(sprint)}
    {upcoming_releases(sprint)}<br /><br />
    {happiness_score()}
    {actions_suggestions()}
    """
    res = res.replace("&", "&amp;")
    return res


def generate_explanation_message(
    title: str, issues: Optional[list[JiraIssueSprintReport]]
) -> str:
    explanation_message: str = ""
    if issues:
        explanation_message = f"<h5>{title}</h5>"
    return explanation_message


def all_pbis(sprint: SprintReport) -> str:
    all_issues: list[JiraIssueSprintReport] = get_all_jira_issues_from_sprint_report(
        sprint
    )
    res: str = """
    <h2>Sprint Work Items</h2>
    <strong style="color: rgb(255,102,0)">All PBIs</strong><br />
    """
    return f"{res}{print_pbis(all_issues)}"


def removed_pbis(sprint: SprintReport) -> str:
    explanation_message: str = generate_explanation_message(
        f"Reasons for being removed from {sprint.name}", sprint.removed_issues
    )
    return f"""
    <strong style="color: rgb(255,102,0)">Issues Removed From Sprint</strong><br />
    {print_pbis(sprint.removed_issues)}
    {explanation_message}
    """


def added_pbis(sprint: SprintReport) -> str:
    added_issue_list: Optional[list[JiraIssueSprintReport]] = get_added_issues(
        sprint.added_issues, get_all_jira_issues_from_sprint_report(sprint)
    )
    explanation_message: str = generate_explanation_message(
        f"Reasons for being added to {sprint.name}", added_issue_list
    )
    return f"""
    <strong style="color: rgb(255,102,0)">Issues Added to Sprint</strong><br />
    {print_pbis(added_issue_list)}
    {explanation_message}
    """


def spillover_incomplete_pbis(sprint: SprintReport) -> str:
    explanation_message: str = generate_explanation_message(
        f"Reasons for not being completed during Sprint {sprint.name}",
        sprint.not_completed_issues,
    )
    return f"""
    <strong style="color: rgb(255,102,0)">Spillover / Incomplete PBIs</strong><br />
    {print_pbis(sprint.not_completed_issues)}
    {explanation_message}
    """


def bugs_details(sprint: SprintReport) -> str:
    all_items = get_all_jira_issues_from_sprint_report(sprint)
    bug_list: list[JiraIssueSprintReport] = [
        issue for issue in all_items if issue.issue_type == "Bug"
    ]
    res: str = """<strong style="color: rgb(255,102,0)">Bug Details</strong><br />"""
    explanation_message: str = generate_explanation_message(
        f"No Bugs encountered during {sprint.name}", bug_list
    )
    return f"{res}{print_pbis(bug_list)}{explanation_message}"


def upcoming_releases(sprint: SprintReport) -> str:
    all_issues: list[JiraIssueSprintReport] = get_all_jira_issues_from_sprint_report(
        sprint
    )
    project_key: str = "FDA1"
    if all_issues:
        project_key: str = all_issues[0].key.split("-")[0]
    return f"""
    <h2>Upcoming Releases</h2>
    please review the <a href="https://jira.amer.thermo.com/projects/{project_key}?selectedItem=com.atlassian.jira.jira-projects-plugin%3Arelease-page&status=unreleased">release calendar page</a> for current and upcoming releases
    """


def happiness_score() -> str:
    message: str = """
    Happiness Score is 1-5, with five being the highest. The team can choose how happy they were with and during the sprint.
    """
    return f"""
    {info_macro("info", message ,"Happiness Index")}
    <table>
        <tbody>
            <tr>
                <th style="text-align: left" class="highlight-green confluenceTh">happiness Score</th>
                <th style="text-align: left" class="highlight-green confluenceTh">Votes</th>
                <th style="text-align: center" class="highlight-green confluenceTh">Average Happiness</th>
            </tr>
            <tr>
                <td style="text-align: left"><p>Great = 5 😁</p><p>Good = 4 😀</p><p>Just Okay = 3 😐</p><p>Not so good = 2 🙁</p><p>Not great at all = 1 😢</p></td>
                <td style="text-align: left"></td>
                <td style="text-align: center"></td>
            </tr>
        </tbody>
    </table>
    """


def actions_suggestions() -> str:
    return """
    <h2>Ideas and Suggestions</h2>
    <table>
        <tbody>
            <tr>
                <th style="text-align: left">Topic</th>
                <th style="text-align: left">Suggestion</th>
            </tr>
            <tr>
                <td style="text-align: left"></td>
                <td style="text-align: left"></td>
            </tr>
        </tbody>
    </table>
    """


def total_items_table(sprint: SprintReport) -> str:
    return f"""
        <table>
            <tbody>
                <tr>
                    <th style="text-align: center">Total PBIs Commited</th>
                    <th style="text-align: center">Commited Story Points</th>
                    <th style="text-align: center">Completed Story Points</th>
                    <th style="text-align: center">Completion %</th>
                    <th style="text-align: center">BV Covered (Optional)</th>
                    <th style="text-align: center">Overall Reason</th>
                </tr>
                <tr>
                    <td style="text-align: center">{get_total_commited_pbis(sprint)}</td>
                    <td style="text-align: center">{sprint.commited_story_points}</td>
                    <td style="text-align: center">{sprint.delivered_story_points}</td>
                    <td style="text-align: center">{calculate_completion(sprint)} %</td>
                    <td style="text-align: center">N/A</td>
                    <td style="text-align: center">N/A</td>
                </tr>
            </tbody>
        </table>
    """


def calculate_completion(sprint: SprintReport) -> str:
    delivered = sprint.delivered_story_points or 0
    committed = sprint.commited_story_points or 0

    if delivered or committed:
        return f"{delivered / committed * 100:.0f}"
    return "N/A"


def qppi_link(board: str) -> str:
    return f"""
    <a href="http://victoria.invitrogen.com/tools/qppi?team={board}">Refer to QPPI to find accurate and automated values (click here).</a>
    """


def print_pbis(table_rows: Optional[list[JiraIssueSprintReport]]) -> str:
    res: str = "No issues during the Sprint.<br />"
    if table_rows:
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
                </tr>{print_pbis_tr(table_rows)}
            </tbody>
        </table>
        """
    return res


def print_pbis_tr(issues: list[JiraIssueSprintReport]) -> str:
    res: str = ""
    for issue in issues:
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
