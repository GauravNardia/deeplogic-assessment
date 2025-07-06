<script lang="ts">
  import { apiFetch } from '$lib/utils/api';
  import { goto } from '$app/navigation';

  let title = '';
  let description = '';
  let severity = 'LOW';
  let status = 'OPEN';
  let error = '';

  async function handleSubmit() {
    try {
      await apiFetch('/issues', {
        method: 'POST',
        body: JSON.stringify({ title, description, severity, status }),
      });
      goto('/issues');
    } catch (err: any) {
      error = err.message;
    }
  }
</script>

<div class="min-h-screen bg-gray-950 text-white px-6 py-12">
  <div class="max-w-3xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">🐞 Create New Issue</h1>

    <form on:submit|preventDefault={handleSubmit} class="space-y-6 bg-gray-900 p-8 rounded-2xl shadow-xl border border-gray-800">
      <div>
        <label for="title" class="block text-sm font-medium text-gray-300 mb-1">Title</label>
        <input
          id="title"
          class="w-full p-3 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          bind:value={title}
          placeholder="Enter issue title"
          required
        />
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-gray-300 mb-1">Description</label>
        <textarea
          id="description"
          class="w-full p-3 h-32 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          bind:value={description}
          placeholder="Detailed description (Markdown supported)"
          required
        ></textarea>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="severity" class="block text-sm font-medium text-gray-300 mb-1">Severity</label>
          <select
            id="severity"
            bind:value={severity}
            class="w-full p-3 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none"
          >
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
          </select>
        </div>

        <div>
          <label for="status" class="block text-sm font-medium text-gray-300 mb-1">Status</label>
          <select
            id="status"
            bind:value={status}
            class="w-full p-3 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none"
          >
            <option value="OPEN">Open</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="CLOSED">Closed</option>
          </select>
        </div>
      </div>

      {#if error}
        <p class="text-red-500 text-sm">{error}</p>
      {/if}

      <button
        type="submit"
        class="w-full bg-blue-600 hover:bg-blue-700 transition text-white font-semibold py-3 rounded-lg shadow-md"
      >
        + Submit Issue
      </button>
    </form>
  </div>
</div>
