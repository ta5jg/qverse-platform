"""Security Engine"""



def evaluate_security_score(self, state: SystemState) -> SecurityScore:
        score = 100
        findings = []

        if not state.ssl.get('enabled'):
            score -= 30
            findings.append('ssl_missing')

        if not state.firewall.get('ufw_installed'):
            score -= 15
            findings.append('firewall_missing')

        if not state.backups:
            score -= 15
            findings.append('backup_missing')

        return SecurityScore(max(0, score), findings)