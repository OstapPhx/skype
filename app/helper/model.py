from pydantic import BaseModel
from typing import Dict, List, Optional
from skpy import SkypeMsg
import textwrap
import re


class Alert(BaseModel):
    status: str
    failstatus: Optional[str]
    successtatus: Optional[str]
    labels: Optional[Dict[str, str]]
    stage: str
    annotations: Optional[Dict[str, str]]
    startsAt: str
    generatorURL: Optional[str]
    fingerprint: Optional[str]
    commitURL: str
    changelogURL: Optional[str]
    runBy: Optional[str]
    silenceURL: str
    sonarqubeurl: Optional[str]
    app1url: Optional[str]
    app2url: Optional[str]
    app3url: Optional[str]
    app4url: Optional[str]
    app5url: Optional[str]
    app6url: Optional[str]
    app7url: Optional[str]
    app8url: Optional[str]
    app9url: Optional[str]
    app10url: Optional[str]
    dashboardURL: Optional[str]
    valueString: Optional[str]
    values: Optional[Dict[str, float]]
    imageURL: Optional[str]
   # time_emote = SkypeMsg.emote("watch")

    def model_representer(self):
        time_emote = SkypeMsg.emote("time")
        representation = (
            f"{SkypeMsg.bold('Stage')}: {self.stage}\n"
            f"{SkypeMsg.bold('Values')}: {self.value_string_parser()}\n"
            f"{time_emote} {SkypeMsg.bold('Started by')}: {self.runBy} at {self.startsAt}\n"
        #    f"{time_emote} {SkypeMsg.bold('Pipeline date')}: {self.startsAt}\n"
            f"{SkypeMsg.link(url=self.silenceURL, display='Pipeline URL')}\n"
            f"{SkypeMsg.link(url=self.commitURL, display='Commit URL')}\n"
        )

        # Conditional lines based on URL values
        if self.changelogURL:
            representation += f"{SkypeMsg.link(url=self.changelogURL, display='CHANGELOG.md')}\n"
        if self.sonarqubeurl:
            representation += f"{SkypeMsg.link(url=self.sonarqubeurl, display='SonarQube')}\n"
        if self.app1url:
            representation += f"{SkypeMsg.bold('URL #1')}: {self.app1url}\n"
        if self.app2url:
            representation += f"{SkypeMsg.bold('URL #2')}: {self.app2url}\n"
        if self.app3url:
            representation += f"{SkypeMsg.bold('URL #3')}: {self.app3url}\n"
        if self.app4url:
            representation += f"{SkypeMsg.bold('URL #4')}: {self.app4URL}\n"
        if self.app5url:
            representation += f"{SkypeMsg.bold('URL #5')}: {self.app5url}\n"
        if self.app6url:
            representation += f"{SkypeMsg.bold('URL #6')}: {self.app6url}\n"
        if self.app7url:
            representation += f"{SkypeMsg.bold('URL #7')}: {self.app7url}\n"
        if self.app8url:
            representation += f"{SkypeMsg.bold('URL #8')}: {self.app8url}\n"
        if self.app9url:
            representation += f"{SkypeMsg.bold('URL #9')}: {self.app9url}\n"
        if self.app10url:
            representation += f"{SkypeMsg.bold('URL #10')}: {self.app10url}\n"

        return representation

    def value_string_parser(self):
        # Define the pattern
        pattern = r"'([^']*)'\s*labels=\{([^}]*)\}\s*value=([^\]]*)"

        # Find matches
        matches = re.findall(pattern, self.valueString)

        result = ""
        # Extract the values from the matches
        for match in matches:
            metric = match[0]
            labels = match[1]
            value = match[2]
            result += "{} = {} \t ".format(metric, value)
        return result


class GrafanaAlert(BaseModel):
    # All the fields as you initially specified
    receiver: Optional[str]
    failstatus: Optional[str]
    successtatus: Optional[str]
    status: Optional[str]
    orgId: Optional[int]
    projectName: str
    alerts: Optional[List[Alert]]
    groupLabels: Optional[Dict[str, str]]
    commonLabels: Optional[Dict[str, str]]
    commonAnnotations: Optional[Dict[str, str]]
    externalURL: Optional[str]
    version: Optional[str]
    groupKey: Optional[str]
    truncatedAlerts: Optional[int]
    title: Optional[str]
    state: Optional[str]
    message: Optional[str]

    def model_representer(self, verbose=False):
        success_emote = SkypeMsg.emote("smile")
        fail_emote = SkypeMsg.emote("cry")
        project_emote = SkypeMsg.emote("bomb")
        pin_emote = SkypeMsg.emote("pushpin")

        status_lines = ""
        if self.successtatus:
            status_lines += f"{success_emote} {SkypeMsg.bold('Success Status')}: {self.successtatus.upper()} \n"
        if self.failstatus:
            status_lines += f"{fail_emote} {SkypeMsg.bold('Fail Status')}: {self.failstatus.upper()} \n"

        join_char = "\n\n"
        text_indent = "    "

        alert_details = join_char.join(textwrap.indent(alert.model_representer(), text_indent) for alert in self.alerts) if self.alerts else ""

        details = (
            f"{project_emote} {SkypeMsg.bold('Project')}: {self.projectName.upper()} {project_emote} \n"
            + status_lines
            + f"{SkypeMsg.bold('External URL')}: {self.externalURL}\n"
            + f"{SkypeMsg.bold('Org ID')}: {self.orgId}\n"
            + f"{SkypeMsg.bold('Version')}: {self.version}\n"
            + f"{SkypeMsg.bold('Group Key')}: {self.groupKey}\n"
            + f"{SkypeMsg.bold('Truncated Alerts')}: {self.truncatedAlerts}\n"
            + f"{SkypeMsg.bold('State')}: {self.state}\n"
            + f"{SkypeMsg.bold('Message')}: {self.message}\n"
            + f"{SkypeMsg.bold('Info:')}\n"
            + alert_details
        )

        return details