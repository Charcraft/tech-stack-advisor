// k6 load test script
// Uso: k6 run scripts/load-test.js
// Requiere: k6 instalado (https://k6.io/docs/getting-started/installation/)

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Configuración
export const options = {
  stages: [
    { duration: '30s', target: 100 },   // Ramp up
    { duration: '1m', target: 500 },    // Stress
    { duration: '30s', target: 1000 },  // Spike
    { duration: '1m', target: 500 },    // Sustained
    { duration: '30s', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

// Métricas personalizadas
const errorRate = new Rate('errors');
const latency = new Trend('latency');

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  // Health check
  const healthRes = http.get(`${BASE_URL}/healthz`);
  check(healthRes, {
    'healthz status 200': (r) => r.status === 200,
    'healthz has checks': (r) => r.json().checks !== undefined,
  }) || errorRate.add(1);

  // Ready check
  const readyRes = http.get(`${BASE_URL}/readyz`);
  check(readyRes, {
    'readyz status 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  // API: List users
  const listRes = http.get(`${BASE_URL}/api/v1/users`);
  check(listRes, {
    'list users status 200': (r) => r.status === 200,
    'list users is array': (r) => Array.isArray(r.json()),
  }) || errorRate.add(1);

  // API: Create user (10% de requests)
  if (Math.random() < 0.1) {
    const payload = JSON.stringify({
      email: `user${Date.now()}${Math.random()}@example.com`,
      name: `Test User ${Math.random()}`,
    });
    const headers = { 'Content-Type': 'application/json' };
    const createRes = http.post(`${BASE_URL}/api/v1/users`, payload, { headers });
    check(createRes, {
      'create user status 201': (r) => r.status === 201,
      'create user returns id': (r) => r.json().id !== undefined,
    }) || errorRate.add(1);
  }

  // Métricas de latencia
  latency.add(healthRes.timings.duration);
  latency.add(listRes.timings.duration);

  sleep(Math.random() * 0.5); // 0-500ms think time
}

export function handleSummary(data) {
  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'summary.json': JSON.stringify(data, null, 2),
  };
}

function textSummary(data, options) {
  // Simplified summary for console
  const lines = [
    '',
    '===== k6 Load Test Summary =====',
    `Duration: ${(data.state.testRunDurationMs / 1000).toFixed(1)}s`,
    `VUs: ${data.metrics.vus.max.value}`,
    `Iterations: ${data.metrics.iterations.values.count}`,
    '',
    'HTTP Requests:',
    `  Total: ${data.metrics.http_reqs.values.count}`,
    `  Failed: ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%`,
    '',
    'Latency (ms):',
    `  avg: ${data.metrics.http_req_duration.values.avg.toFixed(1)}`,
    `  p90: ${data.metrics.http_req_duration.values['p(90)'].toFixed(1)}`,
    `  p95: ${data.metrics.http_req_duration.values['p(95)'].toFixed(1)}`,
    `  p99: ${data.metrics.http_req_duration.values['p(99)'].toFixed(1)}`,
    `  max: ${data.metrics.http_req_duration.values.max.toFixed(1)}`,
    '',
    'Checks:',
    `  Passed: ${data.metrics.checks.values.passes}`,
    `  Failed: ${data.metrics.checks.values.fails}`,
    `  Rate: ${(data.metrics.checks.values.rate * 100).toFixed(2)}%`,
    '',
    '===============================',
  ];
  return lines.join('\n');
}