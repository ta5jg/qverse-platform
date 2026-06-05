"""Deployment Engine"""



def evaluate_deployment_readiness(self, state: SystemState) -> DeploymentReadiness:
        blocking = []

        if not state.api_health.get('reachable'):
            blocking.append('api_unreachable')

        if not state.ssl.get('enabled'):
            blocking.append('ssl_missing')

        if not state.redis_status.get('installed'):
            blocking.append('redis_missing')

        return DeploymentReadiness(
            ready=len(blocking) == 0,
            blocking_issues=blocking,
        )