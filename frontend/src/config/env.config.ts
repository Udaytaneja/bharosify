// Environment & API Configuration abstraction for AgentTrust OS
export const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  useMockServices: import.meta.env.VITE_USE_MOCK_SERVICES !== 'false',
  requestTimeoutMs: Number(import.meta.env.VITE_REQUEST_TIMEOUT_MS) || 15000,
  auditLogCluster: import.meta.env.VITE_AUDIT_LOG_CLUSTER || 'us-east-fips-1',
};
