from pydantic import BaseModel
from typing import Dict, List, Optional
from skpy import SkypeMsg
import textwrap
import re


class Alert(BaseModel):
    status: str
    labels: Optional[Dict[str, str]]
    stage: str
    annotations: Optional[Dict[str, str]]
    startsAt: str
    generatorURL: Optional[str]
    fingerprint: Optional[str]
    commitURL: str
    changelogURL: str
    silenceURL: str
    sonarqubeURL: Optional[str]
    app1URL: Optional[str]
    app2URL: Optional[str]
    app3URL: Optional[str]
    app4URL: Optional[str]
    app5URL: Optional[str]
    app6URL: Optional[str]
    app7URL: Optional[str]
    app8URL: Optional[str]
    app9URL: Optional[str]
    app10URL: Optional[str]
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
            f"{time_emote} {SkypeMsg.bold('Pipeline date')}: {self.startsAt}\n"
            f"{SkypeMsg.link(url=self.silenceURL, display='Pipeline URL')}\n"
            f"{SkypeMsg.link(url=self.commitURL, display='Commit URL')}\n"
            f"{SkypeMsg.link(url=self.changelogURL, display='CHANGELOG.md')}\n"
        )

        # Conditional lines based on URL values
        if self.sonarqubeURL:
            representation += f"{SkypeMsg.link(url=self.sonarqubeURL, display='SonarQube')}\n"
        if self.app1URL:
            representation += f"{SkypeMsg.bold('URL #1')}: {self.app1URL}\n"
        if self.app2URL:
            representation += f"{SkypeMsg.bold('URL #2')}: {self.app2URL}\n"
        if self.app3URL:
            representation += f"{SkypeMsg.bold('URL #3')}: {self.app3URL}\n"
        if self.app4URL:
            representation += f"{SkypeMsg.bold('URL #4')}: {self.app4URL}\n"
        if self.app5URL:
            representation += f"{SkypeMsg.bold('URL #5')}: {self.app5URL}\n"
        if self.app6URL:
            representation += f"{SkypeMsg.bold('URL #6')}: {self.app6URL}\n"
        if self.app7URL:
            representation += f"{SkypeMsg.bold('URL #7')}: {self.app7URL}\n"
        if self.app8URL:
            representation += f"{SkypeMsg.bold('URL #8')}: {self.app8URL}\n"
        if self.app9URL:
            representation += f"{SkypeMsg.bold('URL #9')}: {self.app9URL}\n"
        if self.app10URL:
            representation += f"{SkypeMsg.bold('URL #10')}: {self.app10URL}\n"

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
    receiver: Optional[str]
    status: str
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
        if verbose:
            return (
                f"{SkypeMsg.bold('GrafanaAlert')}:\n"
                f"{SkypeMsg.bold('receiver')}: {self.receiver}\n"
                f"{SkypeMsg.bold('status')}: {self.status}\n"
                f"{SkypeMsg.bold('orgId')}: {self.orgId}\n"
                f"{SkypeMsg.bold('alerts')}: {', '.join(str(alert) for alert in self.alerts)}\n"
                f"{SkypeMsg.bold('groupLabels')}: {', '.join(str(label) for label in self.groupLabels)}\n"
                f"{SkypeMsg.bold('commonLabels')}: {self.commonLabels}\n"
                f"{SkypeMsg.bold('commonAnnotations')}: {', '.join(str(annotation) for annotation in self.commonAnnotations)}\n"
                f"{SkypeMsg.bold('externalURL')}: {self.externalURL}\n"
                f"{SkypeMsg.bold('version')}: {self.version}\n"
                f"{SkypeMsg.bold('groupKey')}: {self.groupKey}\n"
                f"{SkypeMsg.bold('truncatedAlerts')}: {self.truncatedAlerts}\n"
                f"{SkypeMsg.bold('title')}: {self.title}\n"
                f"{SkypeMsg.bold('state')}: {self.state}\n"
                f"{SkypeMsg.bold('message')}: {self.message}\n"
            )
        else:
            join_char = "\n\n"
            text_indent = "    "
            alert_name = self.commonLabels.get("alertname", "")
            project_emote = SkypeMsg.emote("bomb")
            checkmark_emote = SkypeMsg.emote("smile")
            pin_emote = SkypeMsg.emote("pushpin")
            status_emoticon_dict = {
                "firing": SkypeMsg.emote("bomb"),
                "resolved": SkypeMsg.emote("smile"),
            }

            emote = status_emoticon_dict.get(self.status, "")
            return (
                f"{project_emote} {SkypeMsg.bold('Project')}: {self.projectName.upper()} {project_emote} \n"
                f"{checkmark_emote} {SkypeMsg.bold('Status')}: {self.status.upper()} \n"
                f"{SkypeMsg.bold('Info:')}\n"
                f"{join_char.join(textwrap.indent(alert.model_representer(), text_indent) for alert in self.alerts)}\n"
            )
