from kubernetes import config, client


def get_api_client(kubeconfig_path: str):
    configuration = client.Configuration()
    config.load_kube_config(
        config_file=kubeconfig_path, client_configuration=configuration
    )
    return client.ApiClient(configuration=configuration)