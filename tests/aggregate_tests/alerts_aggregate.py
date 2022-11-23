import uuid
from datetime import datetime

from domain.alerts.alert import Alert
from domain.events.alert_fired import RuleParam


def test_alert_fired():
    """
    GIVEN Alert class instantiated by create method
    WHEN create method is called
    THEN version number of aggregate must +1,
     apply event method must be executed
     and update aggregate "dismissed" status to False
    """

    ruleparam1 = RuleParam(name='rule1', value='1')
    ruleparam2 = RuleParam(name='rule2', value='2')
    myUuid = uuid.uuid4()

    newAlert = Alert.create(
        uuid=myUuid,
        accountId=uuid.uuid4(),
        screeningId=uuid.uuid4(),
        creationDateTime=datetime.utcnow(),
        redFlag='amountLimitRule',
        dateFrom='21-05-2020',
        dateTo='22-05-2020',
        params=(ruleparam1, ruleparam2),
        transactions=['id1', 'id2']
    )

    assert newAlert.getAggregateId().getUUID() == myUuid
    assert newAlert.getVersion() == 1
    assert newAlert.dismissed is False


def test_alert_fired_dismissed():
    """
    GIVEN Alert class instantiated by create method
    WHEN dismiss method from Alert instance is called
    THEN version number of aggregate must be 2,
     apply event method must be executed and update aggregate "dismissed" status to True,
     events from aggregate must have length == 2
    """

    ruleparam1 = RuleParam(name='rule1', value='1')
    ruleparam2 = RuleParam(name='rule2', value='2')
    myUuid = uuid.uuid4()

    newAlert = Alert.create(
        uuid=myUuid,
        accountId=uuid.uuid4(),
        screeningId=uuid.uuid4(),
        creationDateTime=datetime.utcnow(),
        redFlag='amountLimitRule',
        dateFrom='21-05-2020',
        dateTo='22-05-2020',
        params=(ruleparam1, ruleparam2),
        transactions=['id1', 'id2']
    )

    newAlert.dismiss(datetime.utcnow())
    assert newAlert.getAggregateId().getUUID() == myUuid
    assert newAlert.getVersion() == 2
    assert newAlert.dismissed is True
    assert newAlert.getPendingEvents().getAmount() == 2

