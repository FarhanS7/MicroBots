import { validateSystemHealth, SystemHealth, AgentDefinition } from '../src/index.js';

function testSystemHealthValidation() {
  const health: SystemHealth = {
    status: 'ok',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
  };
  if (!validateSystemHealth(health)) {
    throw new Error('Health validation failed for valid payload');
  }
}

function testAgentDefinitionShape() {
  const agent: AgentDefinition = {
    agent_id: 'agent-1',
    name: 'Research Bot',
    role: 'Researcher',
    model: 'gpt-4o',
    instructions: ['Perform competitor research'],
    tools_allowed: ['browser', 'terminal'],
    workspace_id: 'ws-1',
    created_at: new Date().toISOString(),
  };
  if (agent.agent_id !== 'agent-1') {
    throw new Error('Agent ID mismatch');
  }
}

testSystemHealthValidation();
testAgentDefinitionShape();
console.log('Protocol consumer tests passed cleanly!');
