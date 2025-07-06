<script lang="ts">
  import { onMount } from 'svelte';
  import { apiFetch } from '$lib/utils/api';
  import { token, userRole } from '$lib/store';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { marked } from 'marked';

  interface Issue {
    id: number;
    title: string;
    description: string;
    severity: string;
    status: string;
  }

  let issues: Issue[] = [];
  let role = get(userRole);

  onMount(async () => {
    try {
      const data = await apiFetch('/issues', {
        headers: {
          Authorization: `Bearer ${get(token)}`
        }
      });
      issues = data;
    } catch (err: any) {
      alert(err.message);
      goto('/login');
    }
  });
</script>

<div class="min-h-screen bg-gray-950 text-white px-6 py-12">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-white">📋 Your Reported Issues</h1>

    {#if issues.length === 0}
      <p class="text-gray-400">No issues found.</p>
    {:else}
      <ul class="space-y-6">
        {#each issues as issue}
          <li class="bg-gray-900 border border-gray-800 p-6 rounded-2xl shadow-lg transition hover:shadow-xl">
            <h2 class="text-xl font-semibold mb-2 text-blue-400">{issue.title}</h2>
            <div class="prose prose-invert text-gray-300 mb-4">
              {@html marked(issue.description)}
            </div>
            <p class="text-sm text-gray-400 mb-2">
              <span class="font-medium">Severity:</span> {issue.severity} | 
              <span class="font-medium ml-2">Status:</span> {issue.status}
            </p>
            {#if role === 'ADMIN' || role === 'MAINTAINER'}
              <a
                href={`/issues/${issue.id}/edit`}
                class="inline-block mt-2 text-sm text-blue-500 hover:text-blue-400 underline transition"
              >
                ✏️ Edit
              </a>
            {/if}
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
