from oscar.apps.customer.abstract_models import *


class Email(AbstractEmail):
    pass


class CommunicationEventType(AbstractCommunicationEventType):
    pass


class Notification(AbstractNotification):
    pass


class ProductAlert(AbstractProductAlert):
    pass



from oscar.apps.customer.history import *  # noqa
from oscar.apps.customer.alerts.receivers import *  # noqa
