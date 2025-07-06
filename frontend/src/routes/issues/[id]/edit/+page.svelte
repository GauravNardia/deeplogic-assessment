<script lang="ts">
  import { onMount } from 'svelte';
  import { apiFetch } from '$lib/utils/api';
  import { token } from '$lib/store';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { marked } from 'marked';
  import { get } from 'svelte/store';

  let id = '';
  let status = 'OPEN';
  let severity = 'LOW';
  let assigned_to = '';
  let description = '';
  let error = '';

  let users: { id: number; email: string; role: string }[] = [];

  $: id = $page.params.id;

  onMount(async () => {
    try {
      const [issuesData, usersData] = await Promise.all([
        apiFetch('/issues', {
          headers: { Authorization: `Bearer ${get(token)}` }
        }),
        apiFetch('/users', {
          headers: { Authorization: `Bearer ${get(token)}` }
        })
      ]);

      users = usersData;

      const issue = issuesData.find((i: any) => i.id == id);
      if (!issue) throw new Error('Issue not found');

      status = issue.status || 'OPEN';
      severity = issue.severity || 'LOW';
      assigned_to = issue.assigned_to ? String(issue.assigned_to) : '';
      description = issue.description || '';
    } catch (err: any) {
      error = err.message || 'Error loading issue';
    }
  });

  async function handleUpdate() {
    try {
      await apiFetch(`/issues/${id}`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${get(token)}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status,
          severity,
          assigned_to: assigned_to ? +assigned_to : null,
          description
        })
      });
      goto('/issues');
    } catch (err: any) {
      error = err.message;
    }
  }
</script>

<div class="min-h-screen bg-gray-950 text-white px-6 py-12">
  <div class="max-w-3xl mx-auto bg-gray-900 p-8 rounded-2xl shadow-lg border border-gray-800">
    <h1 class="text-3xl font-bold mb-6">Edit Issue</h1>

    <label for="status" class="block mb-2 font-medium">Status</label>
    <select id="status" bind:value={status} class="w-full bg-gray-800 border border-gray-700 rounded p-2 mb-4 text-white focus:outline-none">
      <option value="OPEN">Open</option>
      <option value="TRIAGED">Triaged</option>
      <option value="IN_PROGRESS">In Progress</option>
      <option value="DONE">Done</option>
      <option value="CLOSED">Closed</option>
    </select>

    <label for="severity" class="block mb-2 font-medium">Severity</label>
    <select id="severity" bind:value={severity} class="w-full bg-gray-800 border border-gray-700 rounded p-2 mb-4 text-white focus:outline-none">
      <option value="LOW">Low</option>
      <option value="MEDIUM">Medium</option>
      <option value="HIGH">High</option>
    </select>

    <label for="assigned_to" class="block mb-2 font-medium">Assign to</label>
    <select id="assigned_to" bind:value={assigned_to} class="w-full bg-gray-800 border border-gray-700 rounded p-2 mb-4 text-white focus:outline-none">
      <option value="">Unassigned</option>
      {#each users as user}
        <option value={user.id}>{user.email} ({user.role})</option>
      {/each}
    </select>

    <label for="description" class="block mb-2 font-medium">Description</label>
    <textarea
      id="description"
      placeholder="Edit description (Markdown supported)"
      bind:value={description}
      class="w-full bg-gray-800 border border-gray-700 rounded p-3 h-36 mb-6 text-white focus:outline-none"
    ></textarea>

    <h3 class="text-lg font-semibold mt-6 mb-2">Live Preview</h3>
    <div class="prose prose-invert bg-gray-800 p-4 rounded border border-gray-700 max-w-none mb-6">
      {@html marked(description)}
    </div>

    {#if error}
      <p class="text-red-500 mb-4">{error}</p>
    {/if}

    <button
      on:click={handleUpdate}
      class="bg-green-600 hover:bg-green-700 transition px-6 py-3 rounded-lg font-semibold"
    >
      Update Issue
    </button>
  </div>
</div>
