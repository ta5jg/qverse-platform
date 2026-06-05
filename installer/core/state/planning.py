"""Planning Engine"""



def build_installation_plan(self, state: SystemState) -> InstallationPlan:
        actions = []

        if not state.redis_status.get('installed'):
            actions.append('install_redis')

        if not state.ssl.get('enabled'):
            actions.append('configure_ssl')

        if not state.admin_panel.get('installed'):
            actions.append('install_admin_panel')

        if not state.api_health.get('reachable'):
            actions.append('deploy_qverse_api')

        if not state.backups:
            actions.append('configure_backup_system')

        return InstallationPlan(actions=actions)

def build_repair_actions(self, state: SystemState) -> List[RepairAction]:
        actions = []

        if not state.redis_status.get('installed'):
            actions.append(
                RepairAction(
                    action='install_redis',
                    command='apt-get install redis-server -y',
                    risk='low',
                )
            )

        if not state.ssl.get('enabled'):
            actions.append(
                RepairAction(
                    action='configure_ssl',
                    command='certbot --nginx',
                    risk='medium',
                )
            )

        if not state.api_health.get('reachable'):
            actions.append(
                RepairAction(
                    action='restart_qverse_api',
                    command='systemctl restart qverse-ai-api',
                    risk='low',
                )
            )

        return actions