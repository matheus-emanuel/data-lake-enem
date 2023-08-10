from google.cloud import dataproc_v1 as dataproc

region = 'us-east1'

dataproc_client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )


cluster_dict = {
    'project_id': 'lambda-architeture-on-gcp',
    'cluster_name':'cluster-spark-processing-enem2',
    "config": {
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n2-highmem-2",
                "disk_config": {"boot_disk_size_gb": 100},
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n2-highmem-2",
                "disk_config": {"boot_disk_size_gb": 100},
            },
        },
}

cluster = dataproc_client.create_cluster(
    request= {'project_id':'lambda-architeture-on-gcp', 'region':'us-east1', 'cluster': cluster_dict}
)


result = cluster.result()

print("Cluster created successfully: {}".format(result.cluster_name))
    