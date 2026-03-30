import boto3, csv
from datetime import datetime

def collect(pipeline_name, output_csv):
    client = boto3.client('codepipeline', region_name='eu-west-2')
    response = client.list_pipeline_executions(
        pipelineName=pipeline_name, maxResults=30
    )
    executions = response['pipelineExecutionSummaries']
    rows = []
    for ex in executions:
        start = ex['startTime']
        end   = ex.get('lastUpdateTime', start)
        lead_time = (end - start).total_seconds()
        rows.append({
            'execution_id'     : ex['pipelineExecutionId'],
            'status'           : ex['status'],
            'start_time'       : str(start),
            'end_time'         : str(end),
            'lead_time_seconds': round(lead_time, 1),
            'success'          : 1 if ex['status'] == 'Succeeded' else 0
        })
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    succeeded = sum(r['success'] for r in rows)
    lead_times = [r['lead_time_seconds'] for r in rows
                  if r['success'] == 1]
    print(f'Pipeline: {pipeline_name}')
    print(f'Success rate: {succeeded}/{len(rows)}')
    if lead_times:
        print(f'Mean lead time: {sum(lead_times)/len(lead_times):.1f}s')
    print(f'Saved to: {output_csv}')
    print('---')

collect('baseline-pipeline', 'baseline_metrics.csv')
collect('enhanced-pipeline', 'enhanced_metrics.csv')
