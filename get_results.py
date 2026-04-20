import boto3
from datetime import datetime, timezone

client = boto3.client('codepipeline', region_name='eu-west-2')

# Your experiment dates
START_DATE = datetime(2026, 4, 13, 0, 0, 0, tzinfo=timezone.utc)
END_DATE   = datetime(2026, 4, 17, 23, 59, 59, tzinfo=timezone.utc)

pipelines = [
    ('baseline-pipeline', 'baseline'),
    ('enhanced-pipeline', 'enhanced')
]

for name, label in pipelines:
    resp = client.list_pipeline_executions(
        pipelineName=name,
        maxResults=50
    )
    execs = resp['pipelineExecutionSummaries']

    # Filter only experiment runs by date
    experiment_runs = []
    for ex in execs:
        start = ex['startTime']
        if START_DATE <= start <= END_DATE:
            experiment_runs.append(ex)

    succeeded = 0
    failed = 0
    lead_times_success = []
    lead_times_failed = []

    for ex in experiment_runs:
        start = ex['startTime']
        end = ex.get('lastUpdateTime', start)
        lt = round((end - start).total_seconds(), 1)
        if ex['status'] == 'Succeeded':
            succeeded += 1
            lead_times_success.append(lt)
        else:
            failed += 1
            lead_times_failed.append(lt)

    total = succeeded + failed
    print(f'Pipeline: {name}')
    print(f'Experiment runs found:  {total}')
    print(f'Succeeded:              {succeeded}')
    print(f'Failed/Stopped:         {failed}')
    if lead_times_success:
        print(f'Mean lead time (success): {sum(lead_times_success)/len(lead_times_success):.1f}s')
        print(f'Min lead time:            {min(lead_times_success):.1f}s')
        print(f'Max lead time:            {max(lead_times_success):.1f}s')
    if lead_times_failed:
        print(f'Mean lead time (failed):  {sum(lead_times_failed)/len(lead_times_failed):.1f}s')
    print('---')