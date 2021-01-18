"""Hello Analytics Reporting API V4."""
from googleapiclient.discovery import build

from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '/home/sunil/Desktop/repos/GenieAli/genieali/samplet.json'
# Please Add the simplet.json location
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


def get_report(analytics, from_date, to_date):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    metrics_value = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': from_date, 'endDate': to_date}],
                    'metrics': [{'expression': 'ga:sessions'}, {'expression': 'ga:bounceRate'},
                                {'expression': 'ga:avgSessionDuration'}, {'expression': 'ga:users'},
                                {'expression': 'ga:newUsers'}, {'expression': 'ga:pageviews'},
                                {'expression': 'ga:pageviewsPerSession'}, {'expression': 'ga:sessionsPerUser'}],

                }]
        }
    ).execute()

    dimensions_value = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': from_date, 'endDate': to_date}],
                    'metrics':
                        {'expression': 'ga:users'},

                    "dimensions":
                        {"name": "ga:day"}
                }]
        }
    ).execute()
    metric_value = ''
    for report in metrics_value.get('reports'):

        for row in report.get('data').get('rows'):

            dateRangeValues = row.get('metrics')

            metrics_value = dateRangeValues[0].values()
            for each in metrics_value:
                metric_value = each

    return dimensions_value, metric_value


import datetime
#
#
# def main():
#     to_date = datetime.datetime.now().date()
#
#     from_date = to_date - datetime.timedelta(days=7)
#
#     analytics = initialize_analyticsreporting()
#
#     response = get_report(analytics,str(from_date), str(to_date))
#     print(response)
#
#
# if __name__ == '__main__':
#     main()
