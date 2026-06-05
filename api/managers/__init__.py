"""Q-Verse Managers Layer V9."""

from api.managers.system_manager import system_manager, SystemManager
from api.managers.project_manager import project_manager, ProjectManager
from api.managers.agent_manager import agent_manager, AgentManager
from api.managers.workflow_manager import workflow_manager, WorkflowManager
from api.managers.task_manager import task_manager, TaskManager
from api.managers.deployment_manager import deployment_manager, DeploymentManager
from api.managers.model_manager import model_manager, ModelManager
from api.managers.integration_manager import integration_manager, IntegrationManager
from api.managers.notification_manager import notification_manager, NotificationManager
from api.managers.marketplace_manager import marketplace_manager, MarketplaceManager

__version__ = "V9"
