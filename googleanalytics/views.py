from django.shortcuts import render
import datetime as DT
import datetime
from .sample import *

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'samplet.json'
VIEW_ID = '216282641'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


# Create your views here.
def google_test(request):
    return render(request, 'googletest.html')


def tracker(request):
    analytics = initialize_analyticsreporting()
    to_date = datetime.datetime.now().date()

    from_date = to_date - DT.timedelta(days=7)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    dimensions_value, metric_value = get_report(analytics, str(from_date), str(to_date))
    datee = []
    users = []

    for report in dimensions_value.get('reports'):

        for row in report.get('data').get('rows'):
            dimensions = row.get('dimensions')
            dateRangeValues = row.get('metrics')
            for dimension in dimensions:
                datee.append(dimension)
            metrics_value = dateRangeValues[0].values()
            for each in metrics_value:
                users.append(each[0])

    context = {
        'datee': datee,
        'users': users,
        'metric_value': metric_value,
        'from_date': from_date,
        'to_date': to_date,

    }

    return render(request, 'tracker.html', context)
