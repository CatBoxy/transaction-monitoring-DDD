import importlib

from domain.events.alert_fired import AlertFired, RuleParam


def test_alert_fired():
    """
    GIVEN AlertFired class instantiated
    WHEN the toMap and fromMap methods are called
    THEN toMap must return a dict and fromMap must return an instantiated event from a dict
    """

    ruleparam1 = RuleParam(name='rule1', value='1')
    ruleparam2 = RuleParam(name='rule2', value='2')

    alert = AlertFired(
        'alertId',
        'accountId',
        'screeningId',
        '20-05-2020',
        'amountLimitRule',
        '21-05-2020',
        '22-05-2020',
        (ruleparam1, ruleparam2),
        ['id1', 'id2']
    )

    alertDict = alert.toMap()
    assert type(alertDict) == dict

    # myDict = json.JSONDecoder().decode(s=dtoString)

    # assert type(myDict) == dict
    #
    className = 'AlertFired'
    my_module = importlib.import_module("domain.events.alert_fired")
    MyClass = getattr(my_module, className)
    fromMap = getattr(MyClass, "fromMap")
    instance = fromMap(alertDict)

    assert type(instance) == AlertFired
    assert instance.alertId == 'alertId'
    assert instance.accountId == 'accountId'
    assert instance.screeningId == 'screeningId'
    assert instance.creationDateTime == '20-05-2020'
    assert instance.redFlag == 'amountLimitRule'
    assert instance.dateFrom == '21-05-2020'
    assert instance.dateTo == '22-05-2020'
    assert type(instance.params) == tuple
    assert instance.params == (RuleParam(name='rule1', value='1'), RuleParam(name='rule2', value='2'))
    assert instance.transactions == ['id1', 'id2']

