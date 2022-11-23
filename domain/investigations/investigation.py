from dataclasses import dataclass
from typing import Optional, List

from domain.events.alert_attached import AlertAttached
from domain.events.evidence_attached import EvidenceAttached
from domain.events.investigation_closed import InvestigationClosed
from domain.events.investigation_opened import InvestigationOpened
from domain.events.post_added import PostAdded
from domain.events.subject_linked import SubjectLinked
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass
class Investigation(Aggregate):
    alerts: Optional[List] = None
    posts: Optional[List] = None
    subjects: Optional[List] = None
    evidence: Optional[List] = None

    def getInvestigationId(self) -> str:
        return self.getAggregateId().getUUID()

    @classmethod
    def create(
            cls,
            uuid: UUIDValue,
            startingDate: DateTime
    ):
        investigation = Investigation(AggregateId(uuid.myUuid))
        if investigation.alerts is None:
            investigation.alerts = []
        if investigation.posts is None:
            investigation.posts = []
        if investigation.subjects is None:
            investigation.subjects = []
        if investigation.evidence is None:
            investigation.evidence = []
        investigationOpened = InvestigationOpened(
            investigationId=uuid.myUuid,
            startingDate=startingDate.dateTime
        )
        investigation._publish(investigationOpened)
        return investigation

    def attachAlert(self, alertId, attachedDate):
        if alertId in self.alerts:
            raise ValueError("Alerta ya agregada")
        event = AlertAttached(investigationId=self.getInvestigationId(), attachedDate=attachedDate, alertId=alertId)
        self._publish(event)

    def addPost(self, postId, attachedDate):
        if postId in self.posts:
            raise ValueError("Post ya agregado")
        event = PostAdded(investigationId=self.getInvestigationId(), attachedDate=attachedDate, postId=postId)
        self._publish(event)

    def linkSubject(self, subjectId, attachedDate):
        if subjectId in self.subjects:
            raise ValueError("Sujeto ya agregado")
        event = SubjectLinked(investigationId=self.getInvestigationId(), attachedDate=attachedDate, subjectId=subjectId)
        self._publish(event)

    def attachEvidence(self, evidenceId, attachedDate):
        if evidenceId in self.evidence:
            raise ValueError("Evidencia ya agegada")
        event = EvidenceAttached(investigationId=self.getInvestigationId(), attachedDate=attachedDate,
                                 evidenceId=evidenceId)
        self._publish(event)

    def closeInvestigation(self, closingDate):
        event = InvestigationClosed(investigationId=self.getInvestigationId(), closingDate=closingDate)
        self._publish(event)

    def _applyInvestigationOpened(self, event: InvestigationOpened):
        self.closed = False

    def _applyAlertAttached(self, event: AlertAttached):
        self.alerts.append(event.alertId)

    def _applyPostAdded(self, event: PostAdded):
        self.posts.append(event.postId)

    def _applySubjectLinked(self, event: SubjectLinked):
        self.subjects.append(event.subjectId)

    def _applyEvidenceAttached(self, event: EvidenceAttached):
        self.evidence.append(event.evidenceId)

    def _applyInvestigationClosed(self, event: InvestigationClosed):
        self.closed = True
        self.closingDate = event.closingDate
