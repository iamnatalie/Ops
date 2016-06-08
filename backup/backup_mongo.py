# use Lib/argparse.py
#
#
import argparse
import json
from subprocess import check_output
from datetime import datetime, timedelta

default_snapshot_retention_days = 5


def main():
    parsed_args = _parse_arguments()

    if not parsed_args.volume_id:
        raise ValueError("--volume_id is missing")

    volume_id = parsed_args.volume_id
    snapshot_description = parsed_args.description
    snapshot_retention_time = timedelta(days=parsed_args.snapshot_retention_days)

    print("taking volume snapshot...")

    current_snapshot = _take_snapshot(volume_id, snapshot_description)

    print("volume snapshot taken: {0}".format(current_snapshot))

    last_snapshot_time = _parse_iso_datetime(current_snapshot['StartTime'])

    snapshots = _get_snapshots(volume_id=volume_id)

    print("there is a total of {0} snapshots for volume: {1}".format(len(snapshots), volume_id))

    print("deleting outdated volume snapshots. snapshot retention time: {0}".format(snapshot_retention_time))

    for snapshot in snapshots:
        snapshot_time = _parse_iso_datetime(snapshot['StartTime'])
        if snapshot_time < (last_snapshot_time - snapshot_retention_time):
            snapshot_id = snapshot['SnapshotId']
            _delete_snapshot(snapshot_id)
            print("deleted outdated snapshot: {0}, taken at: {1}".format(snapshot_id, snapshot_time))

    print("finished.")


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--volume_id', type=str)
    parser.add_argument('--description', type=str, default="")
    parser.add_argument('--snapshot_retention_days', type=int, default=default_snapshot_retention_days)
    parsed_args = parser.parse_args()
    return parsed_args


def _take_snapshot(volume_id, description):
    take_snapshot_cmd = ["aws",
                         "ec2",
                         "create-snapshot",
                         "--volume-id", volume_id,
                         "--description", description]

    cmd_output = check_output(take_snapshot_cmd)

    return json.loads(cmd_output)


def _get_snapshots(volume_id='*'):
    get_snapshots_cmd = ["aws",
                         "ec2",
                         "describe-snapshots",
                         "--filters", ' '.join(["Name=volume-id,Values={0}".format(volume_id)])
                         ]

    cmd_output = check_output(get_snapshots_cmd)

    return json.loads(cmd_output)['Snapshots']


def _delete_snapshot(snapshot_id):
    delete_snapshot_cmd = ["aws",
                           "ec2",
                           "delete-snapshot",
                           "--snapshot-id", snapshot_id]

    check_output(delete_snapshot_cmd)


def _parse_iso_datetime(value):
    return datetime.strptime(value[:19] if len(value) > 19 else value, "%Y-%m-%dT%H:%M:%S")


if __name__ == "__main__":
    main()
