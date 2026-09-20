export interface AgentDefinition {
  agent_id: string;
  name: string;
  role: string;
  model: string;
  instructions: string[];
  tools_allowed: string[];
  workspace_id: string;
  created_at: string;
}

export interface TaskSubmissionInput {
  task_id: string;
  prompt: string;
  agent_id: string;
  workspace_id: string;
  context_urls?: string[];
  budget_limit_usd?: number;
}

export interface TaskSubmissionOutput {
  task_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'requires_approval';
  created_at: string;
}

export interface ApprovalRequest {
  approval_id: string;
  task_id: string;
  action_type: string;
  proposed_command: string;
  reason: string;
  status: 'pending' | 'approved' | 'denied' | 'consumed';
  requested_at: string;
  expires_at: string;
}

export interface ApprovalConsumption {
  approval_id: string;
  actor_id: string;
  consumed_at: string;
  success: boolean;
}

export interface SystemHealth {
  status: 'ok' | 'degraded' | 'down';
  version: string;
  timestamp: string;
}

export function validateSystemHealth(health: SystemHealth): boolean {
  return Boolean(health.status && health.version && health.timestamp);
}
