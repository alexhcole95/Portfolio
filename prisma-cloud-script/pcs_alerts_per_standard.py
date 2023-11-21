""" Retrieves a List of Alerts for a Specific Compliance Standard and Cloud Provider """
import csv
from prismacloud.api import pc_api, pc_utility

# --CONFIG-- #
DEFAULT_FILE_NAME = 'alerts.csv'
DEFAULT_STATUS_TYPE = 'open'
parser = pc_utility.get_arg_parser()
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='(Required) Name of the compliance standard in string format. Case sensitive. Ex: "SOC 2"')
parser.add_argument(
    'provider',
    type=str,
    help='(Required) Name of the cloud provider in string format. Ex: "GCP"')
parser.add_argument(
    '--section',
    type=str,
    help='(Optional) - Name of the compliance section in string format. Ex: "2.2.1"')
parser.add_argument(
    '--severity',
    type=str,
    help='(Optional) - The severity of the alerts to be pulled in string format. Ex: "Critical"')
parser.add_argument(
    '--status',
    type=str,
    default=DEFAULT_STATUS_TYPE,
    help='(Optional) - The status of the alerts to be pulled in string format. Ex: "Closed" (Default %s)' % DEFAULT_STATUS_TYPE)
parser.add_argument(
    '--csv_file_name',
    type=str,
    default=DEFAULT_FILE_NAME,
    help='(Optional) - CSV export to the given file name. Ex: "test.csv" (Default %s)' % DEFAULT_FILE_NAME)
args = parser.parse_args()

# --INIT-- #
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --GET COMPLIANCE STANDARD-- #
compliance_standard_name = args.compliance_standard_name
compliance_standard_policy_list = pc_api.compliance_standard_policy_list_read(compliance_standard_name)

# --LOOP-- #
provider = args.provider
section = args.section
status = args.status
severity = args.severity
alert_list = []
for compliance_policy in compliance_standard_policy_list:
    alert_filter = {'filters': [{'operator': '=', 'name': 'alert.status', 'value': status},
                                {'operator': '=', 'name': 'cloud.type', 'value': provider},
                                {'name': 'policy.id', 'operator': '=', 'value': compliance_policy['policyId']},
                                {'name': 'policy.complianceSection', 'operator': '=', 'value': section},
                                {'name': 'policy.severity', 'operator': '=', 'value': severity}
                                ]}
    filtered_alert_list = pc_api.alert_list_read(body_params=alert_filter)
    alert_list.extend(filtered_alert_list)

# --OUTPUT-- #
fields = ['Alert ID', 'Policy ID', 'Account ID', 'Cloud Provider', 'Resource Name', 'Description']
alertId = ''
policyId = ''
remDesc = ''
resName = ''
accountId = ''
cloudProv = ''

with open(args.csv_file_name, 'w', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(fields)
    for alerts in alert_list:
        for field in alerts:
            if field == 'id':
                alertId = alerts[field]
            if field == 'policyId':
                policyId = alerts[field]
            if field == 'policy':
                for value in alerts[field]:
                    if value == 'remediation':
                        for key in alerts[field][value]:
                            if key == "description":
                                remDesc = alerts[field][value][key]
            if field == 'resource':
                for value in alerts[field]:
                    if value == 'name':
                        resName = alerts[field][value]
                    if value == 'accountId':
                        accountId = alerts[field][value]
                    if value == 'cloudType':
                        cloudProv = alerts[field][value]
        writer.writerow([alertId, policyId, accountId, cloudProv, resName, remDesc])
