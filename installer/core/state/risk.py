"""Risk Engine"""



def assess_risks(self, state: SystemState) -> List[RiskItem]:
        risks = []

        if not state.ssl.get('enabled'):
            risks.append(RiskItem('critical', 'ssl', 'Traffic is not encrypted'))

        if not state.redis_status.get('installed'):
            risks.append(RiskItem('medium', 'redis', 'Caching and memory acceleration unavailable'))

        if not state.backups:
            risks.append(RiskItem('high', 'backup', 'No recovery point available'))

        if not state.api_health.get('reachable'):
            risks.append(RiskItem('critical', 'api', 'Core API unavailable'))

        return risks

def dependency_impacts(self, state: SystemState) -> Dict:
        impacts = {}

        if not state.redis_status.get('installed'):
            impacts['redis'] = [
                'memory_engine',
                'agent_context_cache',
                'performance_layer',
            ]

        if not state.api_health.get('reachable'):
            impacts['api'] = [
                'admin_panel',
                'agents',
                'integrations',
            ]

        return impacts